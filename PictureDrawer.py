import logging
import DataModel, DBConnector
from matplotlib import pyplot as plt
import Calculator
import time
import numpy as np

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def draw_plot_by_year():
    paper_year_list = []
    for i in range(1997, 2018):
        paper_year_list.append(DBConnector.query_cnki_main_content_by_year(i))
    x = range(1997, 2018)
    plt.xlabel('Year')
    plt.ylabel('Paper Output Count')
    plt.xticks(range(1997, 2018, 1), rotation=45)
    plt.plot(x, paper_year_list, 'o-')

    plt.show()


def draw_gini_and_cr3():
    t1 = time.time()
    paper_city_tuple_list = DBConnector.get_city_paper_tuple_list()
    t2 = time.time()
    print('Load tuple list, cost {0} secs.'.format(str(round(t2 - t1, 3))))
    ginis, cr3s = [], []
    for i in range(1997, 2018):
        t1 = time.time()
        sid_list = DBConnector.get_sid_list_from_cnki_main_by_year(i)
        year_list = list(filter(lambda o: o[1] in sid_list, paper_city_tuple_list))
        paper_city_list = []
        for item in year_list:
            paper_city_list.append(item[2])
        ginis.append(Calculator.get_gini_index(paper_city_list))
        cr3s.append(Calculator.get_cr3(paper_city_list))
        t2 = time.time()
        print('Finish Year {0}, cost time: {1} secs.'.format(str(i), str(round(t2 - t1, 3))))
    x = range(1997, 2018)
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.xticks(range(1997, 2018, 1), rotation=45)
    plt.ylim((0.0, 1.0))
    plt.yticks(np.arange(0.0, 1.0, step=0.1))
    plt.plot(x, ginis, 'o-', label='Gini Index')
    plt.plot(x, cr3s, '^-m', label='CR3')
    plt.legend(loc='upper right')
    plt.show()
    year = 1997
    for item in ginis:
        print(str(year) + ':' + str(item))
        year = year + 1


draw_gini_and_cr3()
