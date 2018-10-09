import logging
import math

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def get_gini_index(city_paper_list: list):
    total_paper_num = len(city_paper_list)
    cities = set(city_paper_list)
    city_num = len(cities)
    paper_count_list = []
    city_paper_average = total_paper_num / city_num
    for city in cities:
        paper_count_list.append(len(list(filter(lambda o: o == city, city_paper_list))))
    z_n = 0
    for i in range(city_num):
        for j in range(city_num):
            z_n = z_n + abs(paper_count_list[i] - paper_count_list[j])
    result = z_n / (2 * (math.pow(city_num, 2)) * city_paper_average)
    return result


def get_cr3(city_paper_list: list):
    cities = set(city_paper_list)
    total_paper_num=len(city_paper_list)
    paper_count_list = []
    for city in cities:
        paper_count_list.append((city, len(list(filter(lambda o: o == city, city_paper_list)))))
    sorted_list = sorted(paper_count_list, key=lambda o: o[1], reverse=True)
    return (sorted_list[0][1] + sorted_list[1][1] + sorted_list[2][1])/total_paper_num
