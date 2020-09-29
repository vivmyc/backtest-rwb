#
# Backtest RWB moving averages pattern for stocks
#
import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st
import datetime as dt
from pandas_datareader import data as pdr
from PIL import Image

yf.pdr_override()

# Set the background image in the main panel
#-------
import base64

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('bg4.jpg')
#-------


st.write("""
# Backtest RWB Pattern
Backtests the Red White Blue moving average pattern from 
[**wishingwealthblog.com**](https://wishingwealthblog.com/glossary/)
""")
st.markdown("---")

#
#function to get user input
#
def get_input():
	stock=st.sidebar.text_input("Enter Ticker Symbol", "")
	#startyear=st.sidebar.text_input("Start Year", "")
	# Add a selectbox to the sidebar:
	startyear=add_selectbox = st.sidebar.selectbox(
    	'Select Starting Year',
    	('2020', '2019', '2018', '2017', '2016', '2015','2014', '2013', '2012', '2011', '2010')
	)
	return stock,startyear

stock, startyear = get_input()
startmonth=11
startday=1

start=dt.datetime(int(startyear)-1,startmonth,startday)

now=dt.datetime.now()

#todo Need to do some input validation
if not stock:
	'''
	### <------- Enter stock symbol and year in the side panel
	'''
else:
	ticker = yf.Ticker(stock)
	try: 
		company_name = ticker.info['longName'] + ' (' + stock.upper() + ')'
	except:
		company_name = stock.upper()

	st.write('#',company_name)
	st.write('**Note:** The 6 shorter term exponential averages used are 3, 5, 8, 10, 12, 15 days, and the 6 longer term exponential averages used are 30, 35, 40, 45, 50, 60 days.')
	st.write('## Back test results from January ', startyear)

	df=pdr.get_data_yahoo(stock,start,now)

# df[smaString]=df.iloc[:,4].rolling(window=ma).mean()

	emasUsed=[3,5,8,10,12,15,30,35,40,45,50,60] #days
	for x in emasUsed:
		ema=x
		df["Ema_"+str(ema)]=round(df.iloc[:,4].ewm(span=ema, adjust=False).mean(),2)

	df=df.iloc[60:]

	pos=0
	num=0
	percentchange=[]

	for i in df.index:
		cmin=min(df["Ema_3"][i],df["Ema_5"][i],df["Ema_8"][i],df["Ema_10"][i],df["Ema_12"][i],df["Ema_15"][i],)
		cmax=max(df["Ema_30"][i],df["Ema_35"][i],df["Ema_40"][i],df["Ema_45"][i],df["Ema_50"][i],df["Ema_60"][i],)

		close=df["Adj Close"][i]
	
		if(cmin>cmax):
			#Red White Blue Pattern
			if(pos==0):
				bp=round(close,2)
				pos=1
				st.write('\n\n\n\nBuying at ',str(bp) ,' on ', str(i))

		elif(cmin<=cmax):
			#Blue White Red Pattern
			if(pos==1):
				pos=0
				sp=round(close,2)
				st.write ('Selling at ', str(sp), ' on ',  str(i), '\n')
				#print("Selling at "+str(sp) +" on " + str(df["Date"][i]) )
				pc=(sp/bp-1)*100
				percentchange.append(round(pc,2))

		if(num==df["Adj Close"].count()-1 and pos==1):
			pos=0
			sp=round(close,2)
			pc=(sp/bp-1)*100
			percentchange.append(round(pc,2))
			if (pc>0):
				st.write('Current price is: ', round(close,2), ' up ',   round(pc,2), ' percent as of',  str(i))
			else:
				st.write('Current price is: ', round(close,2), ' down ', round(pc,2), ' percent as of',  str(i))

		num+=1

	st.write('Percent Change ', percentchange)

	gains=0
	ng=0
	losses=0
	nl=0
	totalR=1

	for i in percentchange:
		if(i>0):
			gains+=i
			ng+=1
		else:
			losses+=i
			nl+=1
		totalR=totalR*((i/100)+1)

	totalR=round((totalR-1)*100,2)

	if(ng>0):
		avgGain=gains/ng
		maxR=str(max(percentchange))
	else:
		avgGain=0
		maxR="undefined"

	if(nl>0):
		avgLoss=losses/nl
		maxL=str(min(percentchange))
		ratio=str(-avgGain/avgLoss)
	else:
		avgLoss=0
		maxL="undefined"
		ratio="inf"

	if(ng>0 or nl>0):
		battingAvg=ng/(ng+nl)
	else:
		battingAvg=0

	st.write('Number of trades: ',str(ng+nl))
	# print("EMAs used: "+str(emasUsed))
	st.write("Batting Avg: ", str(battingAvg))
	st.write("Gain/loss ratio: "+ ratio)
	st.write("Average Gain: ", str(avgGain))
	st.write("Average Loss: ", str(avgLoss))
	st.write("Largest Gain: ", maxR)
	st.write("Largest Loss: ", maxL)
	st.write("Total return over "+str(ng+nl), " trades: "+ str(totalR)+"%" )
	#st.write("Example return Simulating "+str(n), " trades: "+ str(nReturn)+"%" )
	st.write()
	df

