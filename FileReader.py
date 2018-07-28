import logging, re
import os
import DataModel, DBConnector

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

files = os.listdir(r'汇总/')
print(files)
null_count = 0
for filename in files:
    if '.txt' in filename:
        reader = open(r'汇总/{0}'.format(filename), errors='ignore', encoding='gbk')
        model_list = []
        while True:
            line = reader.readline()
            if not line:
                break
            items = line.split('\t')
            # SrcDatabase Title Author Organ Source Keyword Summary PubTime FirstDuty Fund Year Period Volume Period
            # PageCount
            if items[2] == '':
                null_count = null_count + 1
                continue
            if items[0] == 'SrcDatabase-来源库':
                continue
            model = DataModel.CNKIContent()
            model.SrcDatabase = items[0]
            model.Title = items[1]
            model.Author = items[2]
            organ = items[3].replace('"', '')
            model.Organ = organ.split('!')[0]
            model.Organ = model.Organ.split(';')[0]
            model.Organ = model.Organ.split(',')[0]
            model.Organ = model.Organ.split(' ')[0]
            model.Source = items[4]
            model.Keyword = items[5]
            model.Summary = items[6]
            model.PubTime = items[7]
            model.FirstDuty = items[8]
            model.Fund = items[9]
            if items[10] != '':
                model.Year = int(items[10])
            model_list.append(model)
        DBConnector.db_list_writer(model_list)
        print('{0}已完成导入，共{1}条记录!'.format(filename, str(len(model_list))))

writer = open('log.txt', 'w')
writer.write('数据清洗记录\n')
writer.write('无作者数据:{0}'.format(null_count))
