#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 15:33:13 2018

@author: alvinharjanto
"""

import h5py
import numpy as np

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader as pdr

from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates


i = 0

def get_data(i) :

    filename = '/Users/alvinharjanto/Documents/Traders@UST/NSE.hdf5.txt' 
    with h5py.File(filename, 'r') as hdf :
        
        ls = list(hdf.keys())
        print('List of datasets in the file', ls)
        data = hdf.get('data')
        dataset = np.array(data)
        dataset1 = dataset[2243]
        dataset1 = dataset1[2865:2865+i+100]
        
        i = 0
        
    
        while i < len(dataset1) :
            
            
            if dataset1[i] == 0 :
                
                dataset1 = np.delete(dataset1, (i), axis = 0)
                
            else :
                
                i += 1
                
        plt.plot(dataset1)
        plt.show()
        
        return dataset1
    
    

def make_calculation(ticker, i, startdate = dt.datetime(2018,1,1)) :
    
    burst_volume = False
    burst_cp = False
    position_opened = False
    resistance = 0;
    resistance_before = 0;
    date = dt.datetime.now()
    
    
    start = startdate
    end = dt.datetime.now()
    
    
    df = get_data(i)

    #df = pdr.get_data_yahoo(ticker.upper(),start,end)
    #df.reset_index(inplace=True)
    #df.set_index('Date', inplace = True)
    
    vol = df['Volume']
    
    last = vol.tail(1)
    
    vol_array = np.array(vol.tail(100))
    vol_std = vol_array.std()
    print('Standard Deviation :', vol_std)
    
    vol_mean = vol_array.mean()
    
    cp = df['Close']
    cp_end = cp.tail(100)
    
    cp_dev = np.diff(cp_end)
    
    positive_grads = list()
    
    
    for i in cp_dev :
        
        if i > 0 :
            
            positive_grads.append(i)

    
    positive_grads_array = np.array(positive_grads)
    cp_mean = positive_grads_array.mean()
    
    cp_std = positive_grads_array.std()
    
    cp_array = np.array(cp.tail(100).reset_index())
    
    
    
    
    
    
    
    
    if position_opened == False :
        
        print('Position on Close')
    
        if vol[-1] >= (vol_mean+(3*vol_std)) :
            
            burst_volume = True
        
        
        
        if cp[-1] >= cp_mean+(2*cp_std) :
            
            burst_cp = True
            
        
        if burst_volume == True & burst_cp == True :
            
            #open_position(ticker, date, size)
            print('BUY')
            
            resistance = cp.tail(1)
            date = cp_array[-1][0]
            
        else :
            print('HOLD')
    
    
    
    
    
    if position_opened == True :
        
        print('Position on Open')
        
        check_position()
        
        rec_1 = False
        rec_2 = False
        
        
        #record resistance for down slope
        
        if cp_dev[-1] < 0 :
            
            resistance_before = resistance
            resistance = cp.tail(1)
        
        
        #test downward trend
              
        if resistance < resistance_before :
            
            rec_1 = True
            
         
        #test volume outlier
            
        diff = date - dt.datetime.now()
        days = diff.days
        
        vol = vol[days:]
    
        vol_array = np.array(vol)
        vol_std = vol_array.std()
        print('Standard Deviation :', vol_std)
        
        vol_mean = vol_array.mean()
        
        if vol.tail(1) >= vol_mean+(2*vol_std) | vol.tail(1) <= vol_mean-(2*vol_std) :
            
            rec_2 = True
        
        
        if rec_1 == True & rec_2 == True :
            
            print('SELL')
            #close_position(ticker, size)
            date = dt.datetime.now()
        
        else :
            
            print('HOLD')