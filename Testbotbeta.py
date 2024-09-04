import ccxt
import pandas as pd
import numpy as np
import tulipy as ti
from datetime import datetime as dt , timedelta
import time

exchange=ccxt.binance()
exchange.loadMarkets()
symbol='BTCUSDT'

def create since(days,mins):
	Now=dt.now()
	since=Now-timedelta(days=1*days,minutes=1*minutes)
	starttime=int(since.timestamp()*1000)
	return starttime

def convert_since_to_unit(timeframe,since):
	if timeframe[-1] in ('d', 'h', 'm' ,):
		value_s=timeframe[:-1]
		unit=timeframe[-1]
		value=float(value_s)
		
		if unit== 's':
			return since/(1000*60)
		elif unit=='h':
			return since/(1000*3600)
		elif unit=='d':
			return since/(100*3600*24)

def calculate_STF(timeframe):
	value_s=timeframe[:-1]
	R=float(value)
	STF=R*1000
	return STF

def convert_Audit_to_since_format(timeframe,audit):
	unit=timeframe[-1]
	if unit == 'm':
		return audit*1000*60
	elif unit=='h':
		return audit*1000*3600
	elif unit== 'd':
		return audit*1000*3600*24
	
	
def fetch_data(symbol,timeframe,days,mins):
	since=create_since(days,mins)
	STF=calculate_STF(timeframe)
	
	all_candles=[]
	while True:
		candles=exchange.fetchOHLCV(symbol,timeframe,since)
		all_candles.extend(candles)
		
		OD=convert_since_to_unit(timeframe,since)
		Audit=OD-STF
		if Audit < 0:
			break
		elif Audit==1:
			break
		elif audit >0:
			time.sleep(1)
			sinced=convert_Audit_to_since_format(timeframe,Audit):
		since=sinced
		
	df=pd.DataFrame(all_candles,columns=['timestamp','open','high','low','close','volume'])
	data=np.array(df)
	return data
	

def calculate_mins(timeframe,period):
	units=timeframe[-1]
	value=float(timeframe[:-1])*period
	if units=='m':
		return value * period
	if units=='h':
		return value * 60 * period
	if units=='d':
		return value * 24 *60 * period


def calculate_indicators(symbol,timeframe,days,indicator,period,**kwargs):
	mins=calculate_mins(timeframe,period)
	data=fetch_data(symbol,timeframe,days,mins)
	dataP=np.array(data)
	
	k_periods=kwargs.get('k_periods')
	stddev=kwargs.get('stddev')
	D_periods=kwargs.get('D_periods')
	if indicator=='sma':
		indicator=ti.sma(dataP[:,4],period)
	elif indicator=='bbands':
		indicator= ti.bbands(dataP[:,4],period,stddev)
	elif indicator == 'stoch':
		indicator=ti.stoch(dataP[:,2],dataP[:,3],dataP[:,4],period,K_periods,D_periods)
		
	return indicator

def create_crosses(indicator1,indicator2,data)
	timestamp=data[0]
	cross=[]
	for i in range(len(indicator1)):
		if indicator1[i]>indicator2[i]:
			P=[1,timestamp[i]]
			cross.extend(P)
		elif indicator1[i]<indicator2[i]:
			P=[0,timestamp[i]]
			cross.append(P)
	
	return cross

def create_segment(main_data,master_data):
	main_timestamp=main_data[0]
	master_timestamp=master_data[0]
	set1=set(main_timestamp)
	set2=set(master_timestamp)
	intersection=set1.intersection(set2)
	
	segments=[]
	for i in range(len(intersection)):
		start=intersection[i]
		stop=intersection[i+1]
		segment=[x for x in main_timestamp if start <= x < stop]
		segments.append(segment)
	return segments

def concatenate_crosses(*Args):
	if len(Args)>1:
  	x_value= len(Args)
  	combined_list=[]
  	for lst in *Args:
	    combined_list.extend(lst)
	  return combined_list,x_value
	else:
		x_value=1
		combined_list=Arg

def find_compare_timestamp(segments,i):
	for p in range(1,len(segments)):
		J=p*len(segment[p])
		if len(J) > i:
			return segments[p][0]
				
def buy_cond(buy_crosses,timestamp,x_value):
	N=[]
	for x in range(len(buy_crosses)):
		if buy_crosses[x]==[1,timestamp]:
			n=1
			N.append(n)
	if len(N) => x_value:
		return True
	else:
		return False
		
def sell_cond(sell_crosses,timestamp,x_value):
	N=[]
	for x in range(len(sell_crosses)):
		if sell_crosses[x] == [0,timestamp]:
			n=1
			N.append(n)
			
	if len(N)=> x_value:
		return True
	else:
		return False

def close_buy_cond(close_crosses,timestamp,x_value):
	N=[]
	for x in range(len(close_crosses)):
		if close_crosses[x] == [0, timestamp]:
			n=1
			N.append(n)
	
	if len(N) => x_value:
		return True
	else:
		return False

def close_sell_cond(close_crosses,timestamp,x_value):
		N=[]
		for x in range(len(close_crosses)):
			if close _crosses[x] == [1,timestamp]:
				n=1
				N.append(n)
		if len(N) => x_value:
			return True
		else:
			return False


def create_Q(Ub,Lb):
	Q=[]
	for i in range(len(Ub)):
		q=1/(Ub-Lb)
		Q.extend(q)
		return Q
		
def_Tconf_buy(param,n):
	rule=[]
	if n==0:
		rule=params[n]
		return rule
	if 0<n<=10
	for i in range(1,n):
		dot=params[n-i]
		rule.extend(dot)
	return max(rule)
	if 0<n>10:
		for i in range(1,10):
			dot=params(n-i)
			rule.extend(dot)
		return max(rule)
	if n==-1:
		for i in range(1,10):
			dot=params[n-i]
			rule.extend(dot)
		return max(rule)
		
def_Tconf_sell(param,n):
	rule=[]
	if 0<n<=1:
		rule=params[n]
		return rule
	if 0<n<=10
	for i in range(1,n):
		dot=params[n-i]
		rule.extend(dot)
	return min(rule)
	if 0<n>10:
		for i in range(1,10):
			dot=params(n-i)
			rule.extend(dot)
		return min(rule)
	if n==-1:
		for i in range(1,10):
			dot=params[n-i]
			rule.extend(dot)
		return min(rule)
		

def buy_pnl(Q,Data,Buy_crosses,Close_buy_crosses,*kwargs):
	open=Data[:,1]
	close=Data[:,4]
	main_timestamp=Data[:,0]
	close_x_value=Close_buy_crosses[1]
	Buy_x_values=Buy_crosses[1]
	master_crosses=kwargs.get('master_crosses')
	middle_crosses=kwargs.get('middle_crosses')
	
	segment_1=kwargs.get('segments_1')
	segment_2=kwargs.get('segments_2')
	
	for i in range(1,len(main_timestamp)):
			 n=0
		    if i > n:
		    	base_timestamp=main_timestamp[i]
			    cond1=buy_cond(Buy_crosses[0],Buy_x_value,Base_timestamp)==True
			
			    middle_timetamp=find_compare_timestamp(segment_2,i)
			    master_timestamp=find_compare_timestamp(segment_1,i)
			
			    cond2=buy_cond(master_crosses[0],master_crosses[1], master_timestamp)== True
			    cond3=buy_cond(middle_crosses[0],middle_crosses[1],middle_timestamp)==True
			    Tconf=Tconf_buy(close,i)
			    cond4 = close[i] > Tconf
			    if cond1,cond2,cond3 ,cond4:
			    	n=i
				    buy(n)=[open[i+1], Q[i] ]
				    for p in range(len(main_timestamp)):
				    	if p>n:
				    		close_timestamp=main_timestamp[p]
				    		
				    		cond_close=close_buy_cond(Close_buy_crosses[0],close_timestamp, close_x_value,)==True
				    		SL= (close[p] - buy(n)[0]) *buy(n)[1]
				    		cond_SL=SL=>-1
				    		if cond_close:
				    			buy_close(n)=Open[p+1]
				    			n=p
				    			break
				    		Tp=(close[p]-buy(n)[0])*buy(n)[1]
				    		cond_Tp=Tp=>3
				    		elif cond_Tp:
				    			buy_close(n)=Open[p+1]
				    		    n=p
				    		    break
				    		else cond_SL :
				    		    buy_close(n)=Open[p+1]
				    		    n=p
				    	        break
				    pnl=(buy_close(n)-buy[n][0]) *buy(n)[1]
				    Total_pnl.extend(pnl)
				    		

def sell_pnl(Q,Data,sell_crosses,Close_sell_crosses,*kwargs):
	open=Data[:,1]
	close=Data[:,4]
	main_timestamp=Data[:,0]
	close_x_value=Close_sell_crosses[1]
	sell_x_values=sell_crosses[1]
	master_crosses=kwargs.get('master_crosses')
	middle_crosses=kwargs.get('middle _crosses')
	
	segment_1=kwargs.get('segments_1')
	segment_2=kwargs.get('segments_2')
	middle_x_value=middle_crosses[1]
	main_x_value=main_crosses[1]
	
	for i in range(1,len(main_timestamp)):
			 n=0
		    if i > n:
		    	base_timestamp=main_timestamp[i]
			    cond1=sell_cond(sell_crosses[0],sell_x_values,Base_timestamp)==True
			
			    middle_timetamp=find_compare_timestamp(segment_2,i)
			    master_timestamp=find_compare_timestamp(segment_1,i)
			
			    cond2=sell_cond(master_crosses[0],master_crosses[1], master_timestamp)== True
			    cond3=sell_cond(middle_crosses[0],middle_crosses[1],middle_timestamp)==True
			    Tconf=Tconf_sell(close,i)
			    cond4 = close[i] > Tconf
			    if cond1,cond2,cond3 ,cond4:
			    	n=i
				    sell(n)=[open[i+1], Q[i] ]
				    for p in range(len(main_timestamp)):
				    	if p>n:
				    		close_timestamp=main_timestamp[p]
				    		
				    		cond_close=close_sell_cond(Close_sell_crosses[0],close_timestamp, close_x_value,)==True
				    		SL= (close[p] - buy(n)[0]) *buy(n)[1]
				    		cond_SL=SL==1
				    		if cond_close:
				    			sell_close(n)=open[p+1]
				    			n=p
				    			break
				    		else cond_SL:
				    			sell_close(n)=open[p+1]
				    			n=p
				    			break
				    		Tp=(buy(n)[0]-close[p])*buy(n)[1]
				    		cond_Tp=Tp=>3
				    		if cond_Tp:
				    		    sell_close(n)=open[p+1]
				    		    n=p
				    	        break
				    	     
				    pnl=(sell(n)[0]-sell_close(n)) *buy(n)[1]
				    Total_pnl.extend(pnl)
				   
	 return Total


main_data=fetch_data(symbol,timeframe='3m',days=2,mins=0)
master_data=fetch_data(symbol,timeframe='1h',days=2,mins=0)
middle_data=fetch_data(symbol,timeframe='15m',days=2mins=0)


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

Ubii=bbandsi[2]
Mbii=bbandsi[1]

Ubiii=bbandsi[2]
Mbiii=bbandsi[1]

Q=create_Q(Ubi,Lbi)	
				
crossi1=create_cross(ma5i,ma20,main_data)		

crossi1i=create_cross(ma5ii,Mbii,middle_data)

crossiii1=create_cross(ma5iii,Mbiii,master_data)

segment_1=create_segment(main_data,master_data)	

segment_2=create_segment(main_data,middle_data)

main_crosses=concatenate_crosses(crossi1)
middle_crosses=concatenate_crosses(crossii1)
master_crosses=concatenate_crosses(crossiii1)



def drawdown(data):
	for i in range(length):
		drawdown=[]
		if data[i]<0:
			draw=data[i]
			drawdown.extend(draw)
	return drawdown

buy_pnl= buy_pnl(Q,main_data,main_crosses,main_crosses,segment_1,segment_2,master_crosses,middle_crosses)


sell_pnl=sell_pnl(Q,main_data,main_crosses,main_crosses,segment_1,segment_2,master_crosses,middle_crosses)


Total_pnl=sum(buy_pnl) + sum(sell_pnl)
drawdown_buy=drawdown(buy_pnl)
drawdown_sell=drawdown(sell_pnl)
Total_drawdown=sum(drawdown_buy)+sum(drawdown_sell)
print(len(ma5ii))
print(len(ma5i))
print(len(ma5iii))
print(len(Mbi))
print(len(Mbii))
print(len(Mbiii))



print(Total_pnl)
print(Total_drawdown)
