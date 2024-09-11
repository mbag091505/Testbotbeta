import ccxt
import pandas as pd
import numpy as np
import tulipy as ti
from datetime import datetime as dt , timedelta
import time

exchange=ccxt.binance()
exchange.loadMarkets()
symbol='BTCUSDT'

def create_since(days,mins):
	Now=dt.now()
	since=Now-timedelta(days=1*days,minutes=1*mins)
	starttime=int(since.timestamp()*1000)
	return starttime
def create_endttime(dayz,minz):
	Now=dt.now()
	if minz and dayz:
		end=Now-timedelta(days=1*dayz, minutes=1*minz)
		endttime=int(end.timestamp()*1000)
	else:
		end=Now
		endttime=int(end.timestamp()*1000)
	return endttime
	
	
def fetch_data(symbol,timeframe,days,mins,**kwargs):
	since=create_since(days,mins)
	dayz=kwargs.get('dayz')
	minz=kwargs.get('minz')
	endttime=create_endttime(dayz,minz)

	all_candles=[]
	while since < endttime:
		candles=exchange.fetchOHLCV(symbol, timeframe, since)
		all_candles.extend(candles)
		if len(candles) < 1000:
			break
		
		since=candles[0][-1] + 1
		
		
	df=pd.DataFrame(all_candles,columns=['timestamp','open','high','low','close','volume'])
	data=np.array(df)
	return data
	

def calculate_mins(timeframe,period):
	units=timeframe[-1]
	value=float(timeframe[:-1])
	if units=='m':
		return value*  period
	if units=='h':
		return value * 60 * period
	if units=='d':
		return value * 24 *60 * period


def calculate_indicators(symbol,timeframe,days,indicator,period,**kwargs):
	mins=calculate_mins(timeframe,period)
	data=fetch_data(symbol,timeframe,days,mins,**kwargs)
	
	
	k_periods=kwargs.get('k_periods')
	stddev=kwargs.get('stddev')
	D_periods=kwargs.get('D_periods')
	if indicator=='sma':
		indicator=ti.sma(data[:,4],period)
	elif indicator=='bbands':
		indicator= ti.bbands(data[:,4],period,stddev)
	elif indicator == 'stoch':
		indicator=ti.stoch(data[:,2],data[:,3],data[:,4],period,k_periods,D_periods)
		
	return indicator

def create_crosses(indicator1,indicator2,data):
	timestamp=data[0]
	crossover=[]
	for i in range(len(timestamp)):
		if indicator1[i]>indicator2[i]:
			P=[1,timestamp[i]]
			crossover.append(P)
		elif indicator1[i]<indicator2[i]:
			P=[0,timestamp[i]]
			crossover.append(P)
	
	return crossover

def create_segment(main_data,master_data):
	main_timestamp=main_data[:,0]
	master_timestamp=master_data[:,0]
	set1=set(main_timestamp)
	set2=set(master_timestamp)
	intersection=list(set1.intersection(set2))
	
	segments=[]
	for i in range(len(intersection)-1):
		start=intersection[i]
		stop=intersection[i+1]
		segment=[x for x in main_timestamp if start <= x < stop]
		segments.append(segment)
	return segments

def concatenate_crosses(*Args):
	if len(Args)>1:
		x_value= len(Args)
		combined_list=[]
		for lst in Args:
			combined_list.extend(lst)
			return combined_list,x_value
	else:
		x_value=1
		combined_list=Args
	return combined_list

def find_compare_timestamp(segments,i):
	for p in range(1,len(segments)):
		J=p*len(segments[p])
		if J > i:
			return segments[p][0]
				
def buy_cond(buy_crosses,timestamp,x_value):
	N=[]
	for x in range(len(buy_crosses)):
		if buy_crosses[x]==[1,timestamp]:
			n=1
			N.append(n)
		
	if len(N) == x_value:
		return 1
	else:
		return 0
		
def sell_cond(sell_crosses,timestamp,x_value):
	N=[]
	for x in range(len(sell_crosses)):
		if sell_crosses[x] == [0,timestamp]:
			n=1
			N.append(n)
			
	if len(N)==x_value:
		return 1
	else:
		return 0

def close_buy_cond(close_crosses,timestamp,x_value):
	N=[]
	for x in range(len(close_crosses)):
		xond_xlose=close_crosses[x]==[0,timestamp]
		if xond_xlose:
			return 1
		
def close_sell_cond(close_crosses,timestamp,x_value):
		N=[]
		for x in range(len(close_crosses)):
			if close_crosses[x] == [1,timestamp]:
				n=1
				N.append(n)
		if len(N) == x_value:
			return 1
		else:
			return 0


def create_Q(Ub,Lb):
	Q=[]
	for i in range(len(Ub)):
		d=1/(Ub[i]-Lb[i])
		q=d
		Q.append(q)
		return Q
		
def Tconf_buy(params,n):
	rule =[]
	
	if n==0:
		rule=params[n]
		return rule
	elif n==1:
		rule=params[n]
		return rule
	if 0< n <10:
		for i in range(1,n):
			dot=params[n-i]
			rule.append(dot)
		return max(rule)
	if 0<n>10:
		for i in range(1,10):
			dot=params[n-i]
			rule.append(dot)
		
	if n==-1:
		for i in range(1,10):
			dot=params[n-i]
			rule.append(dot)
		
	else:
		rule=0
		return rule
		
def Tconf_sell(params,n):
	rule=[]
	if n==0:
		rule=params[n]
		return rule
	if n==1:
		rule=params[n]
		return rule
	if 0<n>10:
		for i in range(1,10):
			dot=params[n-i]
			rule.append(dot)
		return min(rule)
	if n==-1:
		for i in range(1,10):
			dot=params[n-i]
			rule.append(dot)
		return min(rule)
	else:
		rule=params[n]
		return rule
		

def buy_pnl(Q,Data,Buy_crosses,Close_buy_crosses,master_crosses,segment_1,segment_2,*kwargs):
	open=Data[:,1]
	close=Data[:,4]
	main_timestamp=Data[:,0]
	close_x_value=1
	Buy_x_values=1
	
	
	
	
	Total_pnl=[]
	
	for i in range(1,len(main_timestamp)):
		n=0
		if i > n:
			base_timestamp=main_timestamp[i]
			cond1=buy_cond(Buy_crosses,base_timestamp,Buy_x_values)
			cond1d=cond1==1
			
			middle_timestamp=find_compare_timestamp(segment_2,i)
			master_timestamp=find_compare_timestamp(segment_1,i)
			
			cond2=buy_cond(master_crosses, master_timestamp,1)== 1
			cond3=buy_cond(middle_crosses,middle_timestamp,1)==1
			Tconf=Tconf_buy(close,i)
			cond4 = close[i] > Tconf
			n=0
			buy=0
			if cond1d and cond2 and cond3 and cond4:
				n=i
				buy=[open[i+1], Q[i] ]
				for p in range(len(main_timestamp)):
					if p>n:
						close_timestamp=main_timestamp[p]
						cond_close=close_buy_cond(Close_buy_crosses,close_timestamp, close_x_value,)==1
						SL=(close[p] - buy[0]) *buy[1]
						cond_SL=SL>-1
						if cond_close:
							close=open[p+1]
							n=p
							break
					pnl=(close-buy[0]) *buy(n)[1]
					Total_pnl.extend(pnl)
	return Total_pnl
				    		

def sell_pnl(Q,Data,sell_crosses,Close_sell_crosses,master_crosses,middle_crosses,segment_1,segment_2,**kwargs):
	open=Data[:,1]
	close=Data[:,4]
	main_timestamp=Data[:,0]
	close_x_value=1
	sell_x_values=1
	

	Total_pnl=[]
	
	for i in range(1,len(main_timestamp)):
		n=0
		if i > n:
			base_timestamp=main_timestamp[i]
			cond1=sell_cond(sell_crosses,base_timestamp,sell_x_values)==1
			
			middle_timestamp=find_compare_timestamp(segment_2,i)
			master_timestamp=find_compare_timestamp(segment_1,i)
			
			cond2=sell_cond(master_crosses,master_timestamp,1)== 1
			cond3=sell_cond(middle_crosses,middle_timestamp,1)==1
			Tconf=Tconf_sell(close,i)
			cond4 = close[i] > Tconf
			if cond1 and cond2 and cond3 and cond4:
				n=i
				sell=[open[i+1], Q[i] ]
				for p in range(len(main_timestamp)):
					if p>n:
						close_timestamp=main_timestamp[p]
						cond_close=close_sell_cond(Close_sell_crosses[0],close_timestamp, close_x_value)==1
						SL= (close[p] - sell(n)[0]) *sell[1]
						cond_SL=SL>1
						if cond_close:
							close=open[p+1]
							n=p
							break
						elif cond_SL:
							close=open[p+1]
							n=p
							break
						Tp=(sell[0]-close[p])*sell[1]
						cond_Tp=Tp=3
						if cond_Tp:
							sell=open[p+1]
							n=p
							break
				pnl=(sell[0]-close) *sell[1]
				Total_pnl.extend(pnl)
				   
	return Total_pnl


main_data=fetch_data(symbol,timeframe='3m',days=2,mins=0)
master_data=fetch_data(symbol,timeframe='1h',days=2,mins=0)
middle_data=fetch_data(symbol,timeframe='15m',days=2,mins=0)


ma5i=calculate_indicators(symbol,timeframe='3m',days=2,indicator='sma',period=5)


ma20=calculate_indicators(symbol,timeframe='3m',days=2,indicator='sma',period=20)

ma5ii=calculate_indicators(symbol,timeframe='15m',days=2,indicator='sma',period=5)

ma5iii=calculate_indicators(symbol,timeframe='1h',days=2,indicator='sma',period=5)

bbandsi=calculate_indicators(symbol,timeframe='3m',days=2,indicator='bbands',period=10,stddev=2)


bbandsii=calculate_indicators(symbol,timeframe='15m',days=2,indicator='bbands',period=10,stddev=2)


bbandsiii=calculate_indicators(symbol,timeframe='1h',days=2,indicator='bbands',period=10,stddev=2)

Ubi=bbandsi[2]
Lbi=bbandsi[0]
Mbi=bbandsi[1]

Ubii=bbandsii[2]
Mbii=bbandsii[1]

Ubiii=bbandsiii[2]
Mbiii=bbandsiii[1]

Q=create_Q(Ubi,Lbi)	
				
crossi1=create_crosses(ma5i,ma20,main_data)		

crossii1=create_crosses(ma5ii,Mbii,middle_data)

crossiii1=create_crosses(ma5iii,Mbiii,master_data)

segment_1=create_segment(main_data,master_data)	

segment_2=create_segment(main_data,middle_data)

main_crosses=concatenate_crosses(crossi1)
middle_crosses=concatenate_crosses(crossii1)
master_crosses=concatenate_crosses(crossiii1)



def drawdown(data):
	drawdown=[]
	for i in range(len(data)):
		if data[i]<0:
			draw=data[i]
			drawdown.append(draw)
	return drawdown

buypnl= buy_pnl(Q,main_data,main_crosses,main_crosses,segment_1,segment_2,master_crosses,middle_crosses)


sellpnl=sell_pnl(Q,main_data,main_crosses,main_crosses,segment_1,segment_2,master_crosses,middle_crosses)


Total_pnl=sum(buypnl) + sum(sellpnl)
drawdown_buy=drawdown(buypnl)
drawdown_sell=drawdown(sellpnl)
Total_drawdown=sum(drawdown_buy)+sum(drawdown_sell)
print(len(ma5ii))
print(len(ma5i))
print(len(ma5iii))
print(len(Mbi))
print(len(Mbii))
print(len(Mbiii))



print(Total_pnl)
print(Total_drawdown)
print(len(buypnl))

