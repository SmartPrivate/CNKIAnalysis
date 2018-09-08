import logging, re
import os
import DataModel, DBConnector

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def process_author_list(author_item: str):
    if len(author_item) <= 3:
        return [author_item]
    for splitter in [',', '，', ';']:
        if splitter not in author_item:
            continue
        authors = author_item.split(splitter)
        author_list = []
        for author in authors:
            if '"' in author:
                author = author.replace('"', '')
            author_list.append(author)
        author_result = ';'.join(author_list)
        if author_result[-1] == ';':
            author_result = author_result[:-1]
        return author_result


def process_organ(src_base: str, organ_item: str):
    organ_item = organ_item.replace('"', '')
    if len(organ_item) == 0:
        return organ_item
    year = int(src_base[4:8])
    if year <= 2000:
        organs = organ_item.split(',')
        if len(organs) == 1:
            organ_item = organs[0]
            if '!' in organ_item:
                return organ_item.split('!')[0]
            else:
                return organ_item
        else:
            if '!' in organ_item:
                organ_list = []
                for organ in organs:
                    organ_list.append(organ.split('!')[0])
                return ';'.join(organ_list)
            else:
                return organ_item.replace(',', ';')
    if year <= 2007:
        if '!' in organ_item:
            organs = organ_item.split(',')
            if len(organs) == 1:
                return organs[0].split('!')[0]
            else:
                organ_list = []
                for organ in organs:
                    organ_list.append(organ.split('!')[0])
                return ';'.join(organ_list)
        else:
            if ' ' in organ_item:
                organ_item = organ_item[:organ_item.index(' ')]
                return organ_item.replace(',', ';')
            return organ_item

    if year == 2008:
        if ',' in organ_item and ' ' in organ_item:
            organ_item = organ_item[:organ_item.index(' ')]
            return organ_item.replace(',', ';')
        if ';' in organ_item and ',' not in organ_item:
            if organ_item[-1] == ';':
                return organ_item[:-1]
            return organ_item
        return organ_item
    if year > 2008:
        if organ_item[-1] == ';':
            return organ_item[:-1]
        return organ_item
    return organ_item


def process_keyword(src_base: str, keyword_item: str):
    if not keyword_item:
        return keyword_item
    if '"' in keyword_item:
        keyword_item = keyword_item.replace('"', '')
    if ';;' in keyword_item:
        return keyword_item.replace(';;', ';')
    if '，' in keyword_item:
        return keyword_item.replace('，', ';')
    if ',' in keyword_item:
        return keyword_item.replace(',', ';')
    if keyword_item[-1] == ';':
        return keyword_item[:-1]
    return keyword_item


def process_summary(summary_item: str):
    if len(summary_item) == 0:
        return summary_item
    if summary_item[0] == '"':
        summary_item = summary_item[1:]
    if summary_item[-1] == '"':
        summary_item = summary_item[:-1]
    return summary_item


def cnki_read_from_file(filename, is_test=True):
    reader = open(r'C:\Users\macha\iCloudDrive\Documents\DataSource\核心期刊数据\汇总\{0}'.format(filename), errors='ignore',
                  encoding='gbk')
    model_list = []
    while True:
        line = reader.readline()
        if not line:
            break
        items = line.split('\t')
        # SrcDatabase Title Author Organ Source Keyword Summary PubTime FirstDuty Fund Year Period Volume Period
        # PageCount
        if items[2] == '':
            continue
        if items[0] == 'SrcDatabase-来源库':
            continue
        if is_test:
            model = DataModel.CNKIContent()
        else:
            model = DataModel.CNKIMainContent()
        model.SrcDatabase = items[0]
        model.Title = items[1]
        model.Author = process_author_list(items[2])
        organ = process_organ(items[0], items[3])
        organ_list = []
        for item in organ.split(';'):
            if re.search('\d\d\d\d\d\d', item):
                continue
            organ_list.append(item)
        model.Organ = ';'.join(organ_list)
        model.Source = items[4]
        model.Keyword = process_keyword(items[0], items[5])
        model.Summary = process_summary(items[6])
        model.PubTime = items[7]
        model.FirstDuty = items[8]
        model.Fund = items[9]
        if items[10] != '':
            model.Year = int(items[10])
        model_list.append(model)
        print('已加载{0}条数据'.format(str(len(model_list))))
    DBConnector.db_list_writer(model_list)
    print('{0}已完成导入，共{1}条记录!'.format(filename, str(len(model_list))))


cnki_read_from_file('中文信息学报.txt', is_test=False)
