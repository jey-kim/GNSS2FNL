#!/usr/bin/env python
# coding: utf-8

# <img src="Figs/GEOS_Logo.pdf" width="500"/> 

# 
# # Step **4** of **`G2FNL`**: <font color=blue>"time_vector_generator.ipynb"</font>
# #### Sep 13, 2021  <font color=red>(v. 1.0.1)</font> 
# ##### Jeonghyeop Kim (jeonghyeop.kim@gmail.com)
# 
# > input prompt: **`yes`** or **`no`** \
# > output files: **`time_vector.dat` & `days_per_month.dat`**
# 
# 0. This code is a part of G2FNL process (Project1: GNSS to FNL)
# 1. This code makes a consecutive time vector from 2006/1/1 to the last date of the end month (`time_vector.dat`).
# 2. Even though the start month is January 2006, the first solution will be always January 2007. 
# 3. The end month can be specified by users. The default end month is the previous month from TODAY.
# 4. This code also generates `days_per_month.dat`,where each of the rows indicates the number of days of all months in the analysis time period in order. 
# 
# 

# In[1]:


# 1. import modules
import numpy as np
import datetime as datetime
import calendar
import pandas as pd
import os
#from calendar import monthrange
#pd.__version__


# In[2]:


os.getcwd()


# In[3]:


# While the user input is not either yes or no, this loop will repeat
date_initial = pd.to_datetime(20060101, format='%Y%m%d')

while True:      
    print(" > The initial month of this analysis is Jan. 2006.")
    print(" >> You can (1) specify the end month of your analysis")
    print(" >>> or (2) just use the default end month (last month from today).")
    print(" >>>> This algorithm does **NOT** produce solutions for the current month.")
    print(" >>>>> Final GNSS position estimates are usually available after about 14 days.")
    print(" >>>>>> {This algorithm uses GNSS stations with 'final orbits' (Two week latency).}")
    print(" ")
    YESorNO=input(" Would you like to specify the end month of your analysis? [yes/no]")
    YESorNO=YESorNO.lower()
    
    while YESorNO not in ("yes","no"):
        print("*** Please type 'yes' or 'no' ***")
        YESorNO=input(" Would you like to specify the end month of your analysis? [yes/no]")
        YESorNO=YESorNO.lower()
        
    if YESorNO == "no" or YESorNO == "yes":
        break 
        #break the while loop
         
      
    
#If yes -> A specific final month (up to its last date)
#If no ->  The last date of the previous month from today is the final date


# YES!
if YESorNO.startswith('y'): 
    print(" ")
    print(" How would you like to set the end month of your analysis (type YYYYMM)? : ")
    last_yearmonth=input()
    date_target_adjusting = pd.to_datetime(last_yearmonth, format='%Y%m').strftime('%Y%m')
    year_target = date_target_adjusting[0:4]
    month_target = date_target_adjusting[4:6]
    
    year_target_int=int(year_target)
    month_target_int=int(month_target)
    date_target_int=calendar.monthrange(year_target_int, month_target_int)[1]
    date_target = str(date_target_int)
    last_date = year_target+month_target+date_target
    
    print(" ")
    print("**The end month of your analysis will be %s" %last_date[0:6])  
    
# NO!
else: 
    
    today=datetime.datetime.today()
    date_target_today_adjusting = pd.to_datetime(today).strftime('%Y%m%d')
    year_target_today = date_target_today_adjusting[0:4]
    month_target_today = date_target_today_adjusting[4:6]
    year_target_today_int = int(year_target_today)
    month_target_today_int = int(month_target_today)
    
    # The end month will be the previous month from today
    if month_target_today_int == 1: #Janary
        year_target_today_int = year_target_today_int -1 #year -1
        month_target_today_int = 12 #December
    else:
        month_target_today_int = month_target_today_int-1 #month-1     
    
    date_target_today_int=calendar.monthrange(year_target_today_int, month_target_today_int)[1]
    
    date_target_today_new = str(date_target_today_int)
    year_target_today_new = str(year_target_today_int)
    
    
    # {1 2 ... 9 10 11 12} = {01 02 ... 09 10 11 12}
    if month_target_today_int < 10:
        month_target_today_new = "0"+str(month_target_today_int)
    else:
        month_target_today_new = str(month_target_today_int)
        
            
    last_date = year_target_today_new+month_target_today_new+date_target_today_new
    print(" ")
    print("**The end month of your analysis will be %s" %last_date[0:6])
    


# In[4]:


date_final = pd.to_datetime(last_date, format='%Y%m%d')
#This gives the YYYYMMDD, where YYYYDD is your end month; DD is the last date of your end month

time_vector_list=pd.date_range(start=date_initial,end=date_final).strftime('%Y%m%d').tolist()
#time vector list starts from 1/1/2006 and ends YYYYMMDD.  


# In[5]:


# SAVE 'time_vector.dat'
with open('time_vector.dat', 'w') as filehandle:
    for listitem in time_vector_list:
        filehandle.write('%s\n' % listitem)


# In[6]:


df_year=np.array(pd.date_range(start=date_initial,end=date_final).strftime('%Y'))
#year nparray
df_month=np.array(pd.date_range(start=date_initial,end=date_final).strftime('%m'))
#month nparray

df_year_month = pd.DataFrame(index = range(len(df_year))) 
# A blank dataFrame (n-dim. n = length of the nparrays)

# Data Frame 
df_year_month['year']=df_year
df_year_month['month']=df_month

howManyDatesPerMonths = df_year_month.groupby(['year','month']).size()
#group by each of all 'YYYYMM'
#This will give how many days for each YYYYMM


# In[7]:


# SAVE 'days_per_month.dat'
howManyDatesPerMonths.to_csv('days_per_month.dat',header=None, index=None,sep=' ',float_format='%g')


# In[ ]:




