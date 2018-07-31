import logging
import matplotlib.pyplot as pls

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
pls.plot(x, y)
pls.show()
