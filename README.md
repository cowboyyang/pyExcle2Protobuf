1��˵����
1.1 ֧�ֽ�XMLת����protobuf��ʽ�ļ���֧�ֽ�EXCEL���ݵ�����protobuf��ʽ����
1.2 example�����ŵ�������ת����ʾ��excel�Ͷ�Ӧ��excel����xml�ļ�
1.3 googledep�����ŵ���google protobuf��Pythonģ���ļ��ͽ�protoԪ�ļ����ɸ������ԽӿڵĹ���

2����XMLת����protobuf��ʽ�ļ�
2.1 ����scriptĿ¼��ִ���������
python convert_excle_tool.py --xmlfile=../example/Person.xml --proto  --outdir=../data
�����dataĿ¼������һ��proto�ļ�

3����excel������protobuf��ʽ����
3.1 ����scriptĿ¼��ִ���������
python convert_excle_tool.py --xmlfile=../example/Person.xml --excel --outdir=../data --messagemeta=Person --dataname=person.data --excelfile=../example/hero.xlsx --sheetname=commondata
�����dataĿ¼�����ɶ�Ӧexcel��protobuf��ʽ�����ݣ���������һ�����ӻ���ʽ���ļ������ı�����򿪣����Բ鿴ת���������Ƿ���ȷ

