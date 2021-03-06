#!/usr/bin/env python
# coding: utf-8

# 1. import modules
import numpy as np
import pandas as pd
import os
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import figaspect
from matplotlib import ticker
import pandas.io.common


current_dir=os.getcwd()
os.getcwd()



#############################################
#(1)
list_full = "station_list_full.dat"
df_list=pd.read_csv(list_full, header=None)
df_list.columns=['StID']
N_list = len(df_list) 

#############################################
#(2)
timefile = 'time_vector.dat'
df_time=pd.read_csv(timefile, header=None)
df_time.columns = ['date']
startDateAnalysis=int(df_time.iloc[0])
endDateAnalysis=int(df_time.iloc[-1])
##########################################################################################
#(3)
metadata = "steps.txt" #file name
df_metadata=pd.read_csv(metadata, header=None, names=list('0123456'), sep=r'(?:,|\s+)',                         comment='#', engine='python')
## steps.txt is in an irregular shape
## equipment-related steps
df_steps_maintenance = df_metadata[df_metadata['2'] == 1].reset_index(drop=True)
df_steps_maintenance = df_steps_maintenance.iloc[:,[0,1,2,3]]
df_steps_maintenance.columns=['stID','date','flag','log']
date_old = df_steps_maintenance.date.tolist() # A DataFrame to a list
date_new = pd.to_datetime(date_old, format='%y%b%d').strftime('%Y%m%d') # convert date format
df_steps_maintenance.loc[:,'date'] = date_new # replaces with the new date  in YYYYMMDD
df_steps_maintenance['date']=df_steps_maintenance['date'].astype(int) #str to int
df_steps_maintenance = df_steps_maintenance[(df_steps_maintenance['date']>=startDateAnalysis) &                                             (df_steps_maintenance['date']<=endDateAnalysis)]

## earthquake-related steps
df_steps_earthquakes = df_metadata[df_metadata['2'] == 2].reset_index(drop=True)
df_steps_earthquakes.columns=['stID','date','flag','threshold','distance','mag','eventID'] 
#The step data has a time column in the form of yyMMMdd 
date_old = df_steps_earthquakes.date.tolist() # A DataFrame to a list
date_new = pd.to_datetime(date_old, format='%y%b%d').strftime('%Y%m%d') # convert date format
df_steps_earthquakes.loc[:,'date'] = date_new # replaces with the new date  in YYYYMMDD
df_steps_earthquakes['date']=df_steps_earthquakes['date'].astype(int) #str to int
df_steps_earthquakes = df_steps_earthquakes[(df_steps_earthquakes['date']>=startDateAnalysis) &                                             (df_steps_earthquakes['date']<=endDateAnalysis)]
df_steps_earthquakes = df_steps_earthquakes.reset_index(drop=True)

##########################################################################################
#(4)
days_per_month = "days_per_month.dat"
df_days_per_month = pd.read_csv(days_per_month, header=None)
df_days_per_month.columns = ['days']


processing_dir = os.path.join(current_dir, 'data', 'processing')
os.chdir(processing_dir) # cp to processing directory
os.getcwd()


df_days_per_month = df_days_per_month.to_numpy()[:,0]
df_days_per_month
start = -1
time_tick_index = []
for N in range(len(df_days_per_month)):
    start = start + df_days_per_month[N]
    time_tick_index.append(start)
    
time_tick_index=time_tick_index[::3]


names = ['date','lon','lat','ue','un','uz','se','sn','sz','corr','flag']

for i in range(N_list):
    
    stID=df_list.StID[i]
    
    steps = df_steps_maintenance[df_steps_maintenance['stID']==stID]
    df_step=steps['date'].unique()
    list_step=df_step.tolist()
    
    earthquakes = df_steps_earthquakes[df_steps_earthquakes['stID']==stID]
    df_earthquake=earthquakes['date'].unique()
    list_earthquake=df_earthquake.tolist()
    
    file_uncorrected = 'timeCropped_'+str(i+1)
    try:
        df_uncorrected=pd.read_csv(file_uncorrected, header=None, sep = ' ')
    except pandas.io.common.EmptyDataError:
        file_uncorrected = 'zeroFilled_'+str(i+1)
        df_uncorrected=pd.read_csv(file_uncorrected, header=None, sep = ' ')    

    df_uncorrected.columns = names
    df_uncorrected_filled=df_time.merge(df_uncorrected, on='date', how='left')
    # MERGE the two data frames based on 'date' column. 
    # ** df_time (full time period) is the left dF.
    # ** df_uncorrected (timeCropped_i) is the right dF. 
    # how='left' means that 
    # MERGE them together filling all empty elements of df_input (right), 
    # comparing with time_vector (left), with NaN  
    df_uncorrected_filled=df_uncorrected_filled.fillna(float(0))
    # Fill up with zeros instead of NaNs.
    df_uncorrected_filled.loc[:,['ue','un','uz','se','sn','sz','corr']]=df_uncorrected_filled.loc[:,['ue','un','uz','se','sn','sz','corr']]*1000 
    # [m] to [mm]
    
    file_corrected = 'zeroFilled_'+str(i+1)
    df_corrected=pd.read_csv(file_corrected, header=None, sep = ' ')
    df_corrected.columns = names
    df_corrected.loc[:,['ue','un','uz','se','sn','sz','corr']]=df_corrected.loc[:,['ue','un','uz','se','sn','sz','corr']]*1000
    
    
    file_no_outlier = 'outlierRemoved_'+str(i+1)
    df_no_outlier=pd.read_csv(file_no_outlier, header=None, sep = ' ')
    df_no_outlier.columns = names
    
    
    
    t_raw = df_no_outlier.loc[:,['date']]
    t_raw = t_raw.to_numpy()[:,0]
    date_fmt = '%Y%m%d'
    dt_t = [dt.datetime.strptime(str(i), date_fmt) for i in t_raw]
    t = [mdates.date2num(i) for i in dt_t] #x in 'datenum'-like format in MATLAB 
    
    ue=df_no_outlier.loc[:,['ue']]
    ue.replace(0, np.nan, inplace=True) #zero to nan
    se=df_no_outlier.loc[:,['se']]
    se.replace(0, np.nan, inplace=True)  
    ue_outlier=df_corrected.loc[:,['ue']]
    ue_outlier.replace(0, np.nan, inplace=True) #zero to nan
    ue_step = df_uncorrected_filled.loc[:,['ue']]
    ue_step.replace(0, np.nan, inplace=True) #zero to nan
    
    un=df_no_outlier.loc[:,['un']]
    un.replace(0, np.nan, inplace=True) #zero to nan
    sn=df_no_outlier.loc[:,['sn']]
    sn.replace(0, np.nan, inplace=True)
    un_outlier=df_corrected.loc[:,['un']]
    un_outlier.replace(0, np.nan, inplace=True) #zero to nan
    un_step = df_uncorrected_filled.loc[:,['un']]
    un_step.replace(0, np.nan, inplace=True) #zero to nan
    
    uz=df_no_outlier.loc[:,['uz']]
    uz.replace(0, np.nan, inplace=True) #zero to nan
    sz=df_no_outlier.loc[:,['sz']]
    sz.replace(0, np.nan, inplace=True)
    uz_outlier=df_corrected.loc[:,['uz']]
    uz_outlier.replace(0, np.nan, inplace=True) #zero to nan
    uz_step = df_uncorrected_filled.loc[:,['uz']]
    uz_step.replace(0, np.nan, inplace=True) #zero to nan
        
################################
######    STEPS (in 't')  ######
################################        

    #STEPs
    stepDATE=df_no_outlier[df_no_outlier['date'].isin(list_step)]
    stepDATE.reset_index()
    stepINDEX = stepDATE.index
    stepINDEX = stepINDEX.tolist()
    step_in_t = [t[c] for c in stepINDEX]
    
    #EQs
    eqDATE=df_no_outlier[df_no_outlier['date'].isin(list_earthquake)]
    eqDATE.reset_index()
    eqINDEX = eqDATE.index
    eqINDEX = eqINDEX.tolist()
    eq_in_t = [t[c] for c in eqINDEX]    
    
     
    file_vel = "velocity_"+str(i+1)
    df_model_vel=pd.read_csv(file_vel, header=None, sep = ' ')
    
    del_x=df_model_vel.iloc[0,0]
    del_y=df_model_vel.iloc[1,0]
    del_z=df_model_vel.iloc[2,0]
    inct_x=df_model_vel.iloc[0,1]
    inct_y=df_model_vel.iloc[1,1]
    inct_z=df_model_vel.iloc[2,1]

    t_for_model=df_no_outlier.index.values+1
    min_non_nan=ue_outlier.apply(pd.Series.first_valid_index).values
    min_non_nan=min_non_nan[0]
    max_non_nan=ue_outlier.apply(pd.Series.last_valid_index).values
    max_non_nan=max_non_nan[0]
    t_for_model=t_for_model.astype(np.float32)
    
    if max_non_nan !=len(t_for_model) and min_non_nan!=0:
        t_for_model[max_non_nan:-1]=np.nan
        t_for_model[0:min_non_nan]=np.nan
        
    elif max_non_nan == len(t_for_model) and min_non_nan!=0:
        t_for_model[0:min_non_nan]=np.nan
        
    elif max_non_nan !=len(t_for_model) and min_non_nan==0:
        t_for_model[max_non_nan:-1]=np.nan
        
    ue_model=del_x*t_for_model+inct_x
    un_model=del_y*t_for_model+inct_y
    uz_model=del_z*t_for_model+inct_z
    
################################
######        PLOT        ######
################################
    
    
    
    w, h = figaspect(1/2.5)
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(w,h))

    #plot vertical lines for the steps related to equipment maintenance
    for x in range(len(step_in_t)):       
        ax1.axvline(step_in_t[x], color='LightSalmon', linestyle='-',linewidth=1)
        ax2.axvline(step_in_t[x], color='LightSalmon', linestyle='-',linewidth=1)
        ax3.axvline(step_in_t[x], color='LightSalmon', linestyle='-',linewidth=1)
        
    #plot vertical lines for the steps related to earthquakes
    for x in range(len(eq_in_t)):       
        ax1.axvline(eq_in_t[x], color='gray', linestyle='--',linewidth=1)
        ax2.axvline(eq_in_t[x], color='gray', linestyle='--',linewidth=1)
        ax3.axvline(eq_in_t[x], color='gray', linestyle='--',linewidth=1)    
    
    
    
    M = 6 # How Many Y ticks?
    yticks1 = ticker.MaxNLocator(M)  
    yticks2 = ticker.MaxNLocator(M) 
    yticks3 = ticker.MaxNLocator(M) 
    
    
    ax1.plot_date(t, ue_step.values, 'o', color='black', markerfacecolor='gray', markersize=2, markeredgewidth=0.1)
    ax1.plot(t, ue_outlier.values, 'o', color='black', markerfacecolor='red', markersize=2, markeredgewidth=0.1)
    ax1.plot(t, ue.values, 'o', color='black', markerfacecolor='blue', markersize=2, markeredgewidth=0.1)  
#    ax1.plot(t, ue_model,'-y',linewidth=5,alpha=0.6)
    ax1.grid(color='gray', linestyle='-', linewidth=0.01)
    ax1.yaxis.set_major_locator(yticks1)

    
    ax2.plot_date(t, un_step.values, 'o', color='black', markerfacecolor='gray', markersize=2, markeredgewidth=0.1)
    ax2.plot(t, un_outlier.values, 'o', color='black', markerfacecolor='red', markersize=2, markeredgewidth=0.1)
    ax2.plot(t, un.values, 'o', color='black', markerfacecolor='blue', markersize=2, markeredgewidth=0.1)
#    ax2.plot(t, un_model,'-y',linewidth=5,alpha=0.6)
    ax2.grid(color='gray', linestyle='-', linewidth=0.01)
    ax2.yaxis.set_major_locator(yticks2)
    
    
    ax3.plot_date(t, uz_step.values, 'o', color='black', markerfacecolor='gray', markersize=2, markeredgewidth=0.1)
    ax3.plot(t, uz_outlier.values, 'o', color='black', markerfacecolor='red', markersize=2, markeredgewidth=0.1)
    ax3.plot(t, uz.values, 'o', color='black', markerfacecolor='blue', markersize=2, markeredgewidth=0.1)
#    ax3.plot(t, uz_model,'-y',linewidth=5,alpha=0.6)
    ax3.grid(color='gray', linestyle='-', linewidth=0.01)
    ax3.yaxis.set_major_locator(yticks3)
    
    
    
    plt.suptitle('GNSS Position time series for station %s' %stID, fontsize=25)    
    ax1.set_ylabel('E-W [mm]')
    ax2.set_ylabel('N-S [mm]')
    ax3.set_ylabel('U-D [mm]')
    

    
    date_formatter = mdates.DateFormatter('%Y-%m')
    ax1.xaxis.set_major_formatter(date_formatter)
    # This simply rotates the x-axis tick labels slightly so they fit nicely.
    fig.autofmt_xdate()
    plt.xticks(rotation=90,ha='center',fontsize=8)
    ticks1 = [t[index] for index in time_tick_index]
    ax1.set_xticks(ticks1)
    ax2.set_xticks(ticks1)
    ax3.set_xticks(ticks1)
    fig.savefig('plot_timeseries_'+str(i+1)+'.pdf',bbox_inches='tight')
    plt.close(fig)




