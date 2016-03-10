#encoding=utf-8
'''
 convert excel to protobuf data
 author : cowboyyang
 date : 2016-03-10
'''

import sys
import os
import optparse
import convert_xml_to_protobuf
import convert_excel_to_protobuf
from loghelper import LOG_ERR
from loghelper import LOG_DBG

if __name__ == "__main__":

    # cmdline config info
    parser = optparse.OptionParser()
    parser.add_option("--xmlfile",  dest="xmlfile", help="process target xml files")
    parser.add_option("--proto", dest="proto", action="store_true", help="convert xml to protobuf proto")
    parser.add_option("--excel", dest="excel", action="store_true", help="convert excle data to protobuf format data")
    parser.add_option("--outdir", dest="outdir", help="target file store dir")
    parser.add_option("--excelfile", dest="excelfile", help="excel file name")
    parser.add_option("--sheetname", dest="sheetname", help="excel sheet name")
    parser.add_option("--dataname", dest="dataname", help="convert protobuf data name")
    parser.add_option("--messagemeta", dest="messagemeta", help="message meta data")

    (options, args) = parser.parse_args()

    procxmlfilelist = []
    if options.xmlfile is None:
        print "no input xml file"
        parser.print_help()
        exit(1)
    else:
        procxmlfilelist = options.xmlfile.split(" ")

    if options.outdir is None:
        print "need store target dir"
        parser.print_help()
        exit(1)

    outdir = os.path.abspath(options.outdir)

    if options.proto:
         # 转换proto文件
        for procxmlfile in procxmlfilelist:
            convert = convert_xml_to_protobuf.Xml2ProtobuffConverter(procxmlfile, outdir)
            convert.convert_xml()
            convert.writ_to_proto_file()
    elif options.excel:
            # 转换EXCLE数据为protobuf格式数据
            excelfile = str(options.excelfile).strip()
            excelsheetname = str(options.sheetname).strip().decode("utf-8")
            targetfilename = str(options.dataname).strip().decode("utf-8")
            messagemeta = str(options.messagemeta).strip()
            msgxmlfile = procxmlfilelist[0]
            excelconvert = convert_excel_to_protobuf.Excel2ProtobufDataConverter(excelfile,
                                                                                 excelsheetname,
                                                                                 outdir,
                                                                                 targetfilename,
                                                                                 messagemeta,
                                                                                 msgxmlfile)
            excelconvert.convert_excel_to_protobufdata()
    else:
        print "no operation!"
        parser.print_help()
        exit(1)



