#coding=utf-8

'''
convert excel to protobuf data
author: cowboyyang
date: 2016-03-10
'''

import xlrd
import os
import sys
from xml.dom import minidom
import convert_xml_to_protobuf
from loghelper import LOG_ERR
from loghelper import LOG_DBG

import StringIO

PROTOC_PATH="..\googledep\protoc"

proto_type_convert_map = {}
proto_type_convert_map["uint32"] = long
proto_type_convert_map["int32"] = long
proto_type_convert_map["int64"] = long
proto_type_convert_map["uint64"] = long
proto_type_convert_map["sint32"] = long
proto_type_convert_map["sint64"] = long
proto_type_convert_map["sint32"] = long
proto_type_convert_map["fixed32"] = long
proto_type_convert_map["fixed64"] = long
proto_type_convert_map["sfixed32"] = long
proto_type_convert_map["sfixed64"] = long
proto_type_convert_map["bool"] = bool
proto_type_convert_map["string"] = type(u'')
proto_type_convert_map["bytes"] = str
proto_type_convert_map["double"] = float
proto_type_convert_map["float"] = float



class Excel2ProtobufDataConverter:

    def __init__(self, excelname, excelsheet, outdir, targetfilename, messagemeta, xmlfile):
        self.excelname = excelname
        self.sheetname = excelsheet
        self.targetdir = outdir
        self.targetfile = targetfilename
        self.metaname = messagemeta
        self.xmlfile = xmlfile
        self.xmldict = {}


    def __mkprototmpdir(self, dirname):
        if not os.path.exists(dirname):
            os.mkdir(dirname)

    def __genproto(self, xmlfile):
        self.__append_selfpython_path("../googledep")
        tmppath=os.path.join(os.path.curdir, "tmp")
        self.__mkprototmpdir(tmppath)
        protoconverter = convert_xml_to_protobuf.Xml2ProtobuffConverter(xmlfile, tmppath)
        protoconverter.convert_xml()
        pb_file_name = protoconverter.writ_to_proto_file()
        pb_file_name = os.path.join(tmppath, pb_file_name)
        commandstr = PROTOC_PATH + " --python_out=." + " " + pb_file_name
        print commandstr
        LOG_DBG("%s", commandstr)
        os.system(commandstr)

    def __append_selfpython_path(self, path):
        for dirpath, dirnames, files in os.walk(path):
            sys.path.append(dirpath)

    def convert_excel_to_protobufdata(self):
        # 首先生成protobuf元文件
        self.__genproto(self.xmlfile)
        # 生成元数据字典
        self.build_xml_dict()
        # 增加搜索路径
        self.__append_selfpython_path("./tmp")
        protomod = __import__("%s_pb2" % os.path.splitext( os.path.basename(self.xmlfile ) )[0] )
        rows_array_msg = protomod.__dict__["%s_array" % self.metaname]()
        # 读取EXCLE数据
        workbook = xlrd.open_workbook(self.excelname)
        sheet = workbook.sheet_by_name(self.sheetname)

        #生成protobuf格式数据
        for row in xrange(1, sheet.nrows):
            itemmsg = rows_array_msg.rows.add()
            self.fill_excel_item_msg(sheet, row, itemmsg)

        # 存储可视化数据
        self.write_visualize_file(rows_array_msg)

        # 存储protobuf格式数据
        self.write_protobuf_file(rows_array_msg)

    def write_visualize_file(self, arraymsg):
        datavisualbuff = StringIO.StringIO()
        tmpout = sys.stdout
        sys.stdout = datavisualbuff
        print arraymsg
        sys.stdout = tmpout
        visualfile = self.targetfile.split('.')[0] + ".txt"
        targetvisualfile = os.path.join(self.targetdir, visualfile)
        if os.path.exists(targetvisualfile):
            # 如果有旧文件，先删除
            os.remove(targetvisualfile)
        protohandle = open(targetvisualfile, 'w')
        protohandle.writelines(str(arraymsg))
        protohandle.flush()
        protohandle.close()

    def write_protobuf_file(self, arraymsg):
        data = arraymsg.SerializeToString()
        targetfile = os.path.join(self.targetdir, self.targetfile)
        if os.path.exists(targetfile):
            # 如果有旧文件，先删除
            os.remove(targetfile)
        protohandle = open(targetfile, "wb")
        protohandle.write(data)
        protohandle.flush()
        protohandle.close()

    def parse_raw_filed(self, sheet, row, meta, key, extrakey, itemmsg):
        keytype = meta[key].get("type")
        keyname = meta[key].get("name")
        pType = proto_type_convert_map.get(keytype)
        properkey=extrakey+key
        bFound = False
        bSetValue = False
        for col in xrange(0, sheet.ncols):
            cname=sheet.cell_value(0, col)
            if cname == properkey:
                bFound = True
                value = sheet.cell_value(row, col)
                vlen = 0
                if keytype == "bytes":
                    # value读取后是unicode类型，bytes类型需要是str数据，所以对bytes类型的采用utf-8进行编码
                    value = value.encode('utf-8')
                    vlen = len(str(value))
                elif keytype == "string":
                    vlen = len(value)
                else:
                    if str(value) == "":
                        vlen = 0
                    else:
                        vlen = len(str(pType(value)))

                # 只有当excel中数据不为空的时候，才写入
                if vlen > 0:
                    itemmsg.__setattr__(keyname, pType(value))
                    bSetValue = True
                # 只有找到了一个对应的数据列，就返回
                break

        if bFound is False:
            # 说明没有找到对应key字段
            return -1
        elif bSetValue is False:
            # 说明对应key数据为空
            return 1
        else:
            # 说明写入了对应key的数据
            return 0

    def fill_excel_item_msg(self, sheet, row, itemmsg):
        ctxdata = self.xmldict.get(self.metaname)
        # 找不到直接抛异常
        for key in ctxdata:
            keytype = ctxdata[key].get("type")
            keyname = ctxdata[key].get("name")
            count = ctxdata[key].get("count")
            option = ctxdata[key].get("option")
            #如果是非结构数据类型，直接取EXCLE数据
            pType = proto_type_convert_map.get(keytype)
            if ( pType is not None ):
                # 说明是非结构数据类型,解析原始数据
                ret = self.parse_raw_filed(sheet, row, ctxdata, key, "", itemmsg)
                if ret < 0:
                    LOG_ERR(u"字段：%s 没有找到" % key)
            else:
                # 说明是结构化数据类型，需要进一步处理
                structmeta=self.xmldict.get(keytype)
                # count为0说明是一个结构体
                if option == "optional":
                    structitem = itemmsg.__getattribute__(keyname)
                    # 组装excle中的结构体字段，读取相关数据
                    for structkey in structmeta:
                        ret = self.parse_raw_filed(sheet, row, structmeta, structkey, key, structitem)
                        if ret < 0:
                            LOG_ERR(u"字段：%s 没有找到" % (structkey+key) )
                elif option == "repeated":
                    seq=1
                    while True:
                        structitem = itemmsg.__getattribute__(keyname).add()
                        ret = 0
                        bHaveSetAnyValue = False # 整个结构体是否有设置一个数据
                        for structkey in structmeta:
                            ret = self.parse_raw_filed(sheet, row, structmeta, structkey, key+str(seq), structitem)
                            if ret < 0:
                                # 说明没有对应的数值数据，需要删除已经添加的数组元素
                                itemmsg.__getattribute__(keyname).__delitem__(-1)
                                return
                            elif 0 == ret:
                                # 说明设置了一个数据
                                bHaveSetAnyValue = True

                        # 如果整个结构体一个数据也没有设置，删除已添加的数组元素
                        if bHaveSetAnyValue is False:
                            itemmsg.__getattribute__(keyname).__delitem__(-1)

                        # 继续处理数组下一个元素
                        seq += 1

    def build_xml_dict(self):
        # 构造一个元数据字典
        domtree=minidom.parse(self.xmlfile)
        value = domtree.documentElement
        for node in value.childNodes:
            if node.nodeName == "struct":
                structname = node.getAttribute("name")
                self.xmldict[structname] = {}
                for child in node.childNodes:
                    if child.nodeName == "entry":
                        cname = child.getAttribute("cname")
                        self.xmldict[structname][cname] = {}
                        self.xmldict[structname][cname]["name"]=child.getAttribute("name")
                        self.xmldict[structname][cname]["type"]=child.getAttribute("type")
                        self.xmldict[structname][cname]["option"]=child.getAttribute("option")
