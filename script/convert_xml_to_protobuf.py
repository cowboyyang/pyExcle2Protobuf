#encoding=utf-8

'''
convert xml to protobuf protocol
author : cowboyyang
date : 2016-03-10
'''


from xml.dom import minidom
import os
import sys
import datetime

class Xml2ProtobuffConverter:
    def __init__(self, filename, targetdir):
        self.file = filename
        self.tdir = targetdir
        self.lines = ""

    def convert_xml(self):
        domtree=minidom.parse(self.file)
        value = domtree.documentElement
        self.lines += self.gen_header_desc()
        self.lines += self.gen_package(value.getAttribute("name"))
        for node in value.childNodes:
            if node.nodeName == "struct":
                #生成message头
                self.lines += "\n\n"
                self.lines += self.gen_comment( node.getAttribute("desc") )
                self.lines += self.gen_message_start(node.getAttribute("name") )

                tag = 0
                for child in node.childNodes:
                    if child.nodeName == "entry":
                        tag += 1
                        self.lines += self.gen_message_filed( child.getAttribute("name"),
                                   child.getAttribute("type") ,
                                   child.getAttribute("option"),
                                   child.getAttribute("desc"),
                                   tag)
                # 生成message尾部
                self.lines += self.gen_message_end(node.getAttribute("name") )
                # 生成一个message array
                self.lines += self.gen_message_array_message(node.getAttribute("name"))

    def writ_to_proto_file(self):
        # 写入proto文件
        filebasename=os.path.basename(self.file)
        protobasename=os.path.splitext(filebasename)[0] + ".proto"
        protoname=os.path.join(self.tdir, protobasename)
        protohadle=open(protoname, 'w')
        protohadle.writelines(self.lines.encode("utf-8"))
        protohadle.flush()
        protohadle.close()
        return protobasename

    def gen_header_desc(self):
        line = "// this file auto gen, do not modify it"
        timestr=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line += "\n// generate time: " + timestr
        line += "\n// magic : 20151112"
        return line

    def gen_package(self, name):
        line="\n" + "package " + name + ";"
        return line

    def gen_comment(self, name):
        line= "\n" + "// " + name
        return line

    def gen_message_start(self, message):
        line= "\n" + "message  " + message + "\n{"
        return line

    def gen_message_end(self, message):
        line= "\n" + "}"
        return line

    def gen_message_filed(self, name, type, option, desc, tag):
        line = "\n" + option + " " + type + " "  + name + " = " + str(tag) + ";" + "  //  " + desc
        return line

    def gen_message_array_message(self, message):
        arraymsg = str(message) + "_array"
        line = "\n\n"
        line += self.gen_message_start(arraymsg)
        line += self.gen_message_filed("rows", message, "repeated", "", 1)
        line += self.gen_message_end(arraymsg)
        return line