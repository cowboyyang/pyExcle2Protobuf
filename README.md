1、说明：
1.1 支持将XML转换成protobuf格式文件，支持将EXCEL数据导出成protobuf格式数据
1.2 example下面存放的是用于转换的示例excel和对应的excel描述xml文件
1.3 googledep下面存放的是google protobuf的Python模块文件和将proto元文件生成各种语言接口的工具

2、将XML转换成protobuf格式文件
2.1 进入script目录，执行如下命令：
python convert_excle_tool.py --xmlfile=../example/Person.xml --proto  --outdir=../data
则会在data目录下生成一个proto文件

3、将excel导出成protobuf格式数据
3.1 进入script目录，执行如下命令：
python convert_excle_tool.py --xmlfile=../example/Person.xml --excel --outdir=../data --messagemeta=Person --dataname=person.data --excelfile=../example/hero.xlsx --sheetname=commondata
则会在data目录下生成对应excel的protobuf格式的数据，还会生成一个可视化格式的文件，用文本软件打开，可以查看转换的数据是否正确

