import matplotlib.pyplot as plt
import numpy
import csv
import random
import os
import math

from BSE import market_session

#global varibales

#时间设定
n_time = 10 #minutes

start_time = 0
end_time = 60 * n_time

if __name__ == "__main__":

	#限定价格区间

	#为了模拟真实交易市场中supply demand curve可能会略微改变的情况，可以添加一定的 offset 使价格区间进行上下的波动，
	# 当ask方和bid方的波动方式一致，那么就产生了offset，随之equbilium price也会产生波动
	def schedule_offsetfn(t):
		pi2 = math.pi * 2
		c = math.pi * 3000
		wavelength = t/c
		gradient = 100 * t / (c / pi2)
		amplitude = 100 * t / (c / pi2)
		offset = gradient + amplitude * math.sin(wavelength * t)
		return int(round(offset, 0))


	price_range = (5, 205)
	price_range_2 = (250, 499)
	#定义两个带offset的价格区间
	price_range_3 = (95, 95, schedule_offsetfn)
	price_range_4 = (105, 105, schedule_offsetfn)


	'''
			@stepmode : fixed : prices are generated to give a constant difference between 
								successive prices when sorted into order. 
								todo : 可能是连续价格？ 
						random: 随机定价， 定价范围较广  可以使用一个元组设定多个价格区间，然后客户定价的时候会从中抽选价格区间定价 若是没有选择random模式，但是元组有多个元素，那么则默认使用第一个价格区间
						jittered : 定价和fixed基本一致，但是偶尔会有一些小的波动
		'''

	#可以选择设置多段时间-价格区间，用以形成 'shock changes' 模拟真实市场上 equbilium price 的不停变化
	supply_schedule = [{'from' : start_time, 'to' : 5 * 60, 'ranges' : [price_range], 'stepmode' : 'fixed'},
					   {'from' : 5 * 60, 'to' : end_time, 'ranges' : [price_range_2], 'stepmode' : 'fixed'}]
	demand_schedule = [{'from': start_time, 'to': 5 * 60, 'ranges': [price_range], 'stepmode': 'fixed'},
					   {'from': 5 * 60, 'to': end_time, 'ranges': [price_range_2], 'stepmode': 'fixed'}]
	#supply_schedule = [{'from' : start_time, 'to' : end_time, 'ranges' : [price_range_3], 'stepmode' : 'fixed'}]
	#demand_schedule = [{'from' : start_time, 'to' : end_time, 'ranges' : [price_range_4], 'stepmode' : 'fixed'}]


	#设置交易间隔    todo: 猜测：每60s添加新的订单 ——》市场收到新的订单满足买家的策略开始交易
	#todo : DONE  每order_interval时间为一个交易期，可以选择使用 'periodic' 或 'drip-xxx' 来表示报价的时间（一次性发布  pseudo-periodic）
	order_interval = 60

	'''
			@timemode : periodic : 按照interval的时间定期发布订单
                        drip-fixed : 以p second作为基准，然后产生'连续的报价'
						drip-jitter: 以p second作为基准，然后产生有一定波动的连续报价
						drip-poisson : 柏松分布报价
	'''
	#order_schedule = {'sup' : supply_schedule, 'dem' : demand_schedule, 'interval' : order_interval, 'timemode' : 'periodic'}
	order_schedule = {'sup': supply_schedule, 'dem': demand_schedule, 'interval': order_interval,
					  'timemode': 'drip-fixed'}


	#设置交易机器人类型及数量
	sellers = [('ZIP', 40)]
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

	random.seed(1)
	#此处调用BSE.py的函数开启市场交易，并输出对应的csv文件
	market_session(trail_id, start_time, end_time, traders, order_schedule, tdump, dump_all, verbose)

	tdump.close()

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


	#删除测试文件
	flag = True
	if flag :
		os.system('rm Zhiyuan*')
		os.system('rm avg_balance.csv')

















