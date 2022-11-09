import matplotlib.pyplot as plt
import numpy
import csv
import random
import os

from BSE import market_session

#global varibales

#时间设定
n_time = 5 #minutes

start_time = 0
end_time = 60 * n_time



if __name__ == "__main__":

	#限定价格区间
	price_range = (80, 200)
	price_range_2 = (20, 120)
	supply_schedule = [{'from' : start_time, 'to' : end_time, 'ranges' : [price_range], 'stepmode' : 'fixed'}]
	demand_schedule = [{'from' : start_time, 'to' : end_time, 'ranges' : [price_range_2], 'stepmode' : 'fixed'}]

	#设置交易间隔    todo: 猜测：每60s添加新的订单 ——》市场收到新的订单满足买家的策略开始交易
	order_interval = 60
	order_schedule = {'sup' : supply_schedule, 'dem' : demand_schedule, 'interval' : order_interval, 'timemode' : 'periodic'}

	#设置交易机器人类型及数量
	sellers = [('SNPR', 100)]
	buyers = sellers
	traders = {'sellers' : sellers, 'buyers' : buyers}

	"""
		@verbose:	-True  output all file
					-False output simple file
	"""
	verbose = False

	#保存输出的文件格式
	trail_id = 'Zhiyuan_%s_%d' % (sellers[0][0], sellers[0][1])
	tdump = open('avg_balance.csv', 'w')
	dump_all = True

	random.seed(100)
	#此处调用BSE.py的函数开启市场交易，并输出对应的csv文件
	market_session(trail_id, start_time, end_time, traders, order_schedule, tdump, dump_all, verbose)

	prices_fname = trail_id + '_tape.csv'

	x = numpy.empty(0)
	y = numpy.empty(0)
	with open(prices_fname, newline = '') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			time = float(row[1])
			price = float(row[2])
			x = numpy.append(x, time)
			y = numpy.append(y, price)

	#绘图
	plt.plot(x, y, 'x', color = 'black')

	flag = True
	if flag :
		os.system('rm Zhiyuan*')
		os.system('rm avg_balance.csv')

















