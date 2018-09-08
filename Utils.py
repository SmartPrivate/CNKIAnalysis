import logging
import dbf

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


reader=open('district_level.csv','r',encoding='utf-8')
header=reader.readline()
while True:
    line=reader.readline()
    if not line:
        break
    print(line)