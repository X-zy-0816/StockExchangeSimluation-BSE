import matplotlib.pyplot as plt
import numpy
import csv
import random

from BSE import market_session

#global varibales

n_time = 10 #minutes

start_time = 0
end_time = 60 * n_time



if __name__ == "__main__":

	price_range = (80, 320)
	supply_schedule = [{'from' : start_time, 'to' : end_time, 'ranges' : [price_range], 'stepmode' : 'fixed'}]
	demand_schedule = [{'from' : start_time, 'to' : end_time, 'ranges' : [price_range], 'stepmode' : 'fixed'}]

	order_interval = 60
	order_schedule = {'sup' : supply_schedule, 'dem' : demand_schedule, 'interval' : order_interval, 'timemode' : 'periodic'}

	sellers = [('ZIP', 11)]
	buyers = sellers
	traders = {'sellers' : sellers, 'buyers' : buyers}

	"""
		@verbose:	-True  output all file
					-False output simple file
	"""
	verbose = False

	trail_id = 'Zhiyuan_%s_%d' % (sellers[0][0], sellers[0][1])
	tdump = open('avg_balance.csv', 'w')
	dump_all = True

	random.seed(100)
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

	plt.plot(x, y, 'x', color = 'black')
	print('234')

















