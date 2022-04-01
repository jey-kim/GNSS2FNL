#!/usr/bin/env python
# coding: utf-8

# <img src="Figs/GEOS_logo.pdf" width="500" />

# 
# # Step **6** of **`G2FNL`**: <font color=blue>"correct_steps.ipynb"</font>
# #### Apr 1, 2022  <font color=red>(v. 1.0.3)</font> 
# ##### Jeonghyeop Kim (jeonghyeop.kim@gmail.com)
# 
# > input file(s)  : **`time_vector.dat`, `steps.txt` ,`station_list_full.dat` & `timeCropped_i`** \
# > output file(s) : **`stepCorrected_i`** \
# > module(s) used : **`ismember.py`**
# 
# 0. This code is a part of GPS2FNL process 
# 1. A GNSS timeseries for years usually has a few discontinuous steps related to maintenance of equipments
# 2. The Nevada Geodetic Lab provides metadata which provides information about these two types of steps. 
# > http://geodesy.unr.edu/NGLStationPages/steps.txt (This file was already downloaded in the previous steps)
# 3. This code uses the metadata to correct listed steps. 
# 4. Step correction algorithm is proposed by *Johnson et al., 2021 (Earth and Space Science)*
# 5. This algorithm does NOT correct for coseismic signals

# <div class="alert alert-danger">
# Do NOT run this code twice without re-starting the kernel
# </div>

# In[1]:


# 1. import python modules
import numpy as np
import pandas as pd
from datetime import datetime
from ismember import ismember
import os
import pandas.io.common

time_window_size = 4; 
# 4-month moving time-window
time_window_size = time_window_size*30 + 35 


# In[2]:


time_window_size


# In[3]:


current_dir=os.getcwd()
os.getcwd()


# ## 1. Build a list of all stations (e.g., 907 stations for california)
# > For some reasons, two list files exist (7/30/2021) 
# > change this later after the STEP 1 and STEP 2 codes are ready

# In[4]:


list_full = "station_list_full.dat"
df_list=pd.read_csv(list_full, header=None)
N_list = len(df_list) #length of the combine Df?
print("the total number of stations for the analysis is %i" % N_list)
df_list.columns=['stID']


# ## 2. Read 'time_vector.dat' & Define datenum
# > Here **`datenum`** will be defined as **df_time_vector.index+1**. \
# > This provides consecutive integers that are equivalent to all of the daily time steps within the analysis. \
# > These integers serve as time flags, and they will be used in this code for regressions for functions of time. \
# > For instance, 2 = 2006-01-02; 3 = 2006-01-03; 5658 = 2021-06-29; ....

# In[5]:


inputfile = 'time_vector.dat'
df_full_time_vector = pd.read_csv(inputfile,header=None)
df_full_time_vector.columns=['date']
df_full_time_vector['datenum'] = df_full_time_vector.index + 1 #consecutive integers

earliest_time=df_full_time_vector.loc[0,['date']]
earliest_time=int(earliest_time)
lastest_time=df_full_time_vector.iloc[-1,0]
lastest_time=int(lastest_time)
print("steps before %i and after %i will be ignored" % (earliest_time,lastest_time))


full_date_list=df_full_time_vector['date'].tolist() # a list
full_date_df=df_full_time_vector['date'] # a df
full_datenum_list=df_full_time_vector['datenum'].tolist() # a list
full_datenum_df=df_full_time_vector['datenum'] # a df


# ## 3. READ metadata and separate them into 
# >(1) equipment-related steps : `df_steps_man_made_interest` \
# >(2) coseismic steps : `df_steps_earthquakes_interest` \
# >This algorithm only deals with **steps within the analysis time** defined in `time_vector.dat`
# 
# **`This code also finds datenum of steps!`**

# In[6]:


metadata = "steps.txt" #file name
df_metadata=pd.read_csv(metadata, header=None, names=list('0123456'), sep=r'(?:,|\s+)',                         comment='#', engine='python')
## steps.txt is in an irregular shape
## 'names=list('0123456')' is to fill empty spots with NaN 

df_steps_man_made = df_metadata[df_metadata['2'] == 1]
df_steps_man_made = df_steps_man_made[['0', '1', '2', '3']]
df_steps_man_made.columns=['stID','time','flag','log'] #time is in yyMMMdd format

## date format conversion
date_old = df_steps_man_made.time.tolist() # A DataFrame to a list
date_new = pd.to_datetime(date_old, format='%y%b%d').strftime('%Y%m%d') # convert date format
df_steps_man_made.loc[:,'time'] = date_new # replaces with the new date  in YYYYMMDD
df_steps_man_made['time']=df_steps_man_made['time'].astype(int) #str to int


df_steps_man_made_interest=df_steps_man_made.loc[(df_steps_man_made['time'] >= earliest_time) & (df_steps_man_made['time'] <= lastest_time)] 
df_steps_man_made_interest=df_steps_man_made_interest.reset_index(drop=True)

## ADD datenum to df_steps_man_made_interest

man_time_list=df_steps_man_made_interest.time.tolist()# To list 
man_time_index=ismember(man_time_list,full_date_list) # Find time index 
man_new_time_vector = df_full_time_vector.iloc[man_time_index] # Find values corresponding to the time index
man_new_time_vector = man_new_time_vector.reset_index(drop=True) # Reset index
    
df_steps_man_made_interest['datenum']=man_new_time_vector['datenum'] # add equivalent datenum 
    ## (datenum will be used to match with steps and will be used for inversions)
df_steps_man_made_interest=df_steps_man_made_interest[['stID','time','datenum','flag','log']]
    ## change column orders    
    
#----------------------------------------------------------------------------------------------#   

################################################################################################     
#######################           *v1.0.x.*       ##############################################
################################################################################################ 
###############  This algorithm does NOT correct co-seismic steps.  ############################ 
###############  But one can modify the code to correct such steps. ############################ 
###############  Now the coseismic-step data will be just saved as  ############################ 
###############  in a DataFrame 'df_steps_earthquakes_interest'.    ############################ 
###############                                                     ############################ 
###############  You can make a step list made of both equipment-   ############################ 
###############  related and earthquakes, sort ascending in time,   ############################ 
###############  and then correct in the order of time later.       ############################ 
###############  Save step flag {1=man-made; 2=earthquake} together ############################ 
###############  because you may need two different ways to correct ############################ 
###############  steps depending on their types!                    ############################ 
################################################################################################ 
#######################         J.K. (yy-mm-dd)       ##########################################
################################################################################################ 

## for column names, see the readme file (http://geodesy.unr.edu/NGLStationPages/steps_readme.txt)
df_steps_earthquakes = df_metadata[df_metadata['2'] == 2].reset_index(drop=True)
df_steps_earthquakes.columns=['stID','time','flag','threshold','distance','mag','eventID'] 
## time is in yyMMMdd format
## date format conversion
date_old2 = df_steps_earthquakes.time.tolist() # A DataFrame to a list
date_new2 = pd.to_datetime(date_old2, format='%y%b%d').strftime('%Y%m%d') # convert date format
df_steps_earthquakes.loc[:,'time'] = date_new2 # replaces with the new date  in YYYYMMDD 
df_steps_earthquakes['time']=df_steps_earthquakes['time'].astype(int) #str to int

df_steps_earthquakes_interest=df_steps_earthquakes.loc[(df_steps_earthquakes['time'] >= earliest_time) & (df_steps_earthquakes['time'] <= lastest_time)] 
df_steps_earthquakes_interest=df_steps_earthquakes_interest.reset_index(drop=True)

## ADD datenum to df_steps_earthquakes_interest
EQ_time_list=df_steps_earthquakes_interest.time.tolist()# To list 
EQ_time_index=ismember(EQ_time_list,full_date_list) # Find time index 
EQ_new_time_vector = df_full_time_vector.iloc[EQ_time_index] # Find values corresponding to the time index
EQ_new_time_vector = EQ_new_time_vector.reset_index(drop=True) # Reset index
    
df_steps_earthquakes_interest['datenum']=EQ_new_time_vector['datenum'] # add equivalent datenum 
    ## (datenum will be used to match with steps and will be used for inversions)
df_steps_earthquakes_interest=df_steps_earthquakes_interest[['stID','time','datenum','flag','threshold','distance','mag','eventID']]
    ## change column orders


# ## 4. Correct steps! 
# > (a) Read input data **`timeCropped_i`** \
# > (b) Find and add **`datenum`** for the time-axis of the input data \
# > (c) Check if the target station has unwanted steps. 
# >> if no, continue the for loop \
# >> if yes, keep going 
# 
# > (d) Save datenum for all steps \
# > (e) For loop j in range(steps) \
# > (f) Corrections! \
# > (g) REMOVE ALL POSITION ESTIMATES on the date of step(s) \
# > (h) Save corrected data **`stepCorrected_i`**

# In[7]:


processing_dir = os.path.join(current_dir, 'data', 'processing')
os.chdir(processing_dir) # cp to processing directory
os.getcwd()


# In[8]:


## Correcting the steps!

for i in range(N_list): #range(N_list) later
    
## (a) Read input data 'timeCropped_i'
    target_data="timeCropped_"+str(i+1)
    try:
        df_GPS=pd.read_csv(target_data, header=None, sep=' ')
    except pandas.io.common.EmptyDataError:
        save_array=np.array([[earliest_time,0,0,0,0,0,0,0,0,0,0]])
        savefile = "stepCorrected_"+str(i+1) #output file = stepCorrected_"$i"
        np.savetxt(savefile, save_array, fmt='%i')
        continue
        
    df_GPS.columns=['time','lon','lat','e','n','z','se','sn','sz','corr_en','flag']
    
    station=df_list.loc[i,['stID']].to_string(index=False)
    SearchSt=station[0:4] # a space in the first byte of the string
    #NOT ANYMORE (4/1/2022)
    
    #SearchSt is the target station for corrections
    
## (b) Add datenum for the input data 'timeCropped_i'    
    time_list=df_GPS.time.to_list() #to list    
    time_index=ismember(time_list,full_date_list) #find time index 
    
    #Check if everything is okay
    if len(time_index)-len(df_GPS) != 0:
        print("*****************************")
        print("*****************************")
        print("*****************************")
        print("*****************************")
        print("WARNING: something is wrong!!")
        print("*****************************")
        print("*****************************")
        print("*****************************")
        print("*****************************")
    new_time_vector =df_full_time_vector.iloc[time_index]
    
    new_time_vector=new_time_vector.reset_index() # reset index
    
    df_GPS['datenum']=new_time_vector['datenum'] # add equivalent datenum 
    #(datenum will be used to match with steps and will be used for inversions)
    df_GPS=df_GPS[['time','datenum','lon','lat','e','n','z','se','sn','sz','corr_en','flag']]
    #change column orders
    
    
    # Unit [m] to [mm]
    df_GPS.e = df_GPS.e*1000
    df_GPS.n = df_GPS.n*1000
    df_GPS.z = df_GPS.z*1000
    df_GPS.se = df_GPS.se*1000
    df_GPS.sn = df_GPS.sn*1000
    df_GPS.sz = df_GPS.sz*1000
    
    
    
## (c) Check is the target station with unwatned step(s) 
## > if no, continue the for loop
## >> if yes, keep going 

    itemindex = np.where(df_steps_man_made_interest['stID']==SearchSt) # similar to find() in MATLAB
    HowManySteps=itemindex[0].size  # the number of steps
    
    
    print("%i: Attempt to correct time series of %s" % (i,SearchSt))
    
    if HowManySteps==0: # No step      
        print("       No step found")
   
    else: # step(s) exist
        
        event_idx = itemindex[0]

## (d) Save datenum for all steps 

        all_datenum = df_steps_man_made_interest.datenum
        event_datenum = all_datenum.iloc[event_idx]
        event_datenum = pd.unique(event_datenum) 
        # In a day, more than a job can be done.
        # In this case, the steps.txt saves all the jobs in multiple logs.
        # But the date in the logs are the same. 
        # Here, the code gets rid of all the overlaps

        N_events = len(event_datenum) #How many steps without counting multiple times for overlapped steps
        
## (e) For loop j in range(N_events)
        for j in range(N_events):
        
            print("       Step(s) found: %i/%i" %(j+1,N_events))
            step_standards=event_datenum[j]

            before_step = list(range(step_standards-14,step_standards)) #14 days before the step (a list)
            after_step = list(range(step_standards+1,step_standards+15)) #14 days after the step (a list)
            #These are in datenum 
            
            data_datenum = df_GPS.datenum       
            date_before=ismember(before_step,data_datenum) 
            date_after=ismember(after_step,data_datenum)
            #find the same datenum in the data, and give the indices!
            
            idx_before=[x for x in date_before if x == x] # get rid of float('NaN') from the list
            idx_after=[x for x in date_after if x == x] # get rid of float('NaN') from the list
            

## (f) Obtain before_step and after_step (14 days for each)
## > 4 cases. 


## >> (  i) len(idx_before) <  10 and len(idx_after) >= 10
            if len(idx_before) < 10 and len(idx_after) >= 10:
                print("              case1: Not enough position estimates before a step to take the median")
                #print(len(idx_before))
                # case1: fewer than 10 position estimates are available before the step")
                # A linear fit will be performed to fill the gap using the time series 
                # of one-year period before the step. 
                # If fewer than 250 position estimates are available over the year period,
                # 5 month positions before the step will be removed. 
                # WHY 5 months? The default of the algorithm uses 4-month moving time window
                # to obtain seasonal strain. 
                
                One_year_before_step = list(range(step_standards-365,step_standards)) # one year before the step
                date_one_year_before=ismember(One_year_before_step,data_datenum)
                idx_one_year_before=[x for x in date_one_year_before if x == x]
            
                if len(idx_one_year_before) < 250:
                    print("              >>>>>>Some position estimates will be removed")
                    Time_window_size_before = list(range(step_standards-time_window_size,step_standards))
                    #time_window_size = 4*30 + 35 = ~5 months
                    date_time_window_size_before=ismember(Time_window_size_before,data_datenum)
                    idx_time_window_size_before = [x for x in date_time_window_size_before if x == x]
                    df_GPS=df_GPS.drop(idx_time_window_size_before) #drop the data. #make sure later you need to reset the index of DF!
                    df_GPS=df_GPS.reset_index(drop=True)
                else:
                    print("              >>>>>>A linear fitting will be performed")
                    # Linear fit will be performed.      
                    
                    # data with errors
                    #t=df_GPS.datenum[idx_one_year_before]
                    t=df_GPS.loc[idx_one_year_before,['datenum']]
                    
                    
                    e=df_GPS.e[idx_one_year_before]
                    n=df_GPS.n[idx_one_year_before]
                    z=df_GPS.z[idx_one_year_before]
                    
                    se=df_GPS.se[idx_one_year_before]
                    sn=df_GPS.sn[idx_one_year_before]
                    sz=df_GPS.sz[idx_one_year_before]
                    
                    inv_se = 1/se 
                    inv_sn = 1/sn
                    inv_sz = 1/sz
                    
                    # 1/error diagonal matrices
                    We = pd.DataFrame(np.diag(inv_se),index=inv_se.index,columns=inv_se.index) #1/error diagonal matrix
                    Wn = pd.DataFrame(np.diag(inv_sn),index=inv_sn.index,columns=inv_sn.index) #1/error diagonal matrix
                    Wz = pd.DataFrame(np.diag(inv_sz),index=inv_sz.index,columns=inv_sz.index) #1/error diagonal matrix

                    
                    #G-matrices with errors
                    
                    Ge=pd.DataFrame(t,index=t.index)
                    Ge['ones']=pd.DataFrame(np.array([1] * len(Ge)),index=Ge.index)
                    Gew=We@Ge
                    
                    Gn=pd.DataFrame(t,index=t.index)
                    Gn['ones']=pd.DataFrame(np.array([1] * len(Gn)),index=Gn.index)
                    Gnw=Wn@Gn
                    
                    Gz=pd.DataFrame(t,index=t.index)
                    Gz['ones']=pd.DataFrame(np.array([1] * len(Gz)),index=Gz.index) 
                    Gzw=Wz@Gz
                    
                
                    #date vectors with errors
                    
                    ew = We@e
                    nw = Wn@n
                    zw = Wz@z
                    
                    Gew_prime = Gew.transpose()
                    Gnw_prime = Gnw.transpose()
                    Gzw_prime = Gzw.transpose()
                    
                    GP_G_e = Gew_prime @ Gew
                    GP_G_n = Gnw_prime @ Gnw
                    GP_G_z = Gzw_prime @ Gzw
                    
                    try:
                        inv_GP_G_e = pd.DataFrame(np.linalg.inv(GP_G_e.to_numpy()), GP_G_e.columns, GP_G_e.index)
                    except:
                        inv_GP_G_e = pd.DataFrame(np.linalg.pinv(GP_G_e.to_numpy()), GP_G_e.columns, GP_G_e.index)
                        print("For station %s, the 'e'-component. Try pseudo inversion")

                    try:
                        inv_GP_G_n = pd.DataFrame(np.linalg.inv(GP_G_n.to_numpy()), GP_G_n.columns, GP_G_n.index)
                    except:
                        inv_GP_G_n = pd.DataFrame(np.linalg.pinv(GP_G_n.to_numpy()), GP_G_n.columns, GP_G_n.index)
                        print("For station %s, the 'n'-component. Try pseudo inversion")
                        
                    try:
                        inv_GP_G_z = pd.DataFrame(np.linalg.inv(GP_G_z.to_numpy()), GP_G_z.columns, GP_G_z.index)
                    except:
                        inv_GP_G_z = pd.DataFrame(np.linalg.pinv(GP_G_z.to_numpy()), GP_G_z.columns, GP_G_z.index)                        
                        print("For station %s, the 'z'-component. Try pseudo inversion")
                    
                    
                    #INVERSION MODELs
                    model_e = inv_GP_G_e@Gew_prime@ew
                    model_n = inv_GP_G_n@Gnw_prime@nw
                    model_z = inv_GP_G_z@Gzw_prime@zw
                    
                    e_model_at_the_step=model_e[0]*step_standards+model_e[1]
                    n_model_at_the_step=model_n[0]*step_standards+model_n[1]
                    z_model_at_the_step=model_z[0]*step_standards+model_z[1]
                    
                    median_before_e=e_model_at_the_step #from linear model
                    median_before_n=n_model_at_the_step #from linear model
                    median_before_z=z_model_at_the_step #from linear model
                    
                    
                    median_after_e=df_GPS.e[idx_after].median() #from data (median value)
                    median_after_n=df_GPS.n[idx_after].median() #from data (median value)
                    median_after_z=df_GPS.z[idx_after].median() #from data (median value)
                    
                    
                    # Modeled steps
                    diff_after_before_e = median_after_e - median_before_e
                    diff_after_before_n = median_after_n - median_before_n
                    diff_after_before_z = median_after_z - median_before_z
                    
                    
                    #Correcting.. 
                    idx_start=idx_after[0]
                    idx_end=len(df_GPS)
                    idx_correction=list(range(idx_start,idx_end))
                    
                    df_GPS.loc[idx_correction,['e']]=df_GPS.loc[idx_correction,['e']]-diff_after_before_e
                    df_GPS.loc[idx_correction,['n']]=df_GPS.loc[idx_correction,['n']]-diff_after_before_n
                    df_GPS.loc[idx_correction,['z']]=df_GPS.loc[idx_correction,['z']]-diff_after_before_z

                    
                    
                    
                    
## >> ( ii) len(idx_before) >= 10 and len(idx_after) < 10            
            elif len(idx_before) >= 10 and len(idx_after) < 10:
                print("              case2: Not enough position estimates after a step to take the median")
                #print(len(idx_after))
                # case2: fewer than 10 position estimates are available after the step")
                # A linear fit will be performed to fill the gap using the time series 
                # of one-year period after the step. 
                # If fewer than 250 position estimates are available over the year period,
                # 5 month positions before the step will be removed. 
                # WHY 5 months? The default of the algorithm uses 4-month moving time window
                # to obtain seasonal strain. 
                
                One_year_after_step = list(range(step_standards+1,step_standards+366)) # one year after the step
                date_one_year_after=ismember(One_year_after_step,data_datenum)
                idx_one_year_after=[x for x in date_one_year_after if x == x]

                if len(idx_one_year_after) < 250:
                    print("              >>>>>>Some position estimates will be removed")
                    Time_window_size_after = list(range(step_standards+1,step_standards+time_window_size+1))
                    #time_window_size = 4*30 + 35 = ~5 months
                    date_time_window_size_after=ismember(Time_window_size_after,data_datenum)
                    idx_time_window_size_after = [x for x in date_time_window_size_after if x == x]
                    df_GPS=df_GPS.drop(idx_time_window_size_after) #drop the data. #make sure later you need to reset the index of DF!
                    
                else:
                    print("              >>>>>>A linear fitting will be performed")
                    # Linear fit will be performed.      
                    
                    # data with errors
                    t=df_GPS.datenum[idx_one_year_after]
                    
                    e=df_GPS.e[idx_one_year_after]
                    n=df_GPS.n[idx_one_year_after]
                    z=df_GPS.z[idx_one_year_after]
                    
                    se=df_GPS.se[idx_one_year_after]
                    sn=df_GPS.sn[idx_one_year_after]
                    sz=df_GPS.sz[idx_one_year_after]
                    
                    inv_se = 1/se 
                    inv_sn = 1/sn
                    inv_sz = 1/sz
                    
                    # 1/error diagonal matrices
                    We = pd.DataFrame(np.diag(inv_se),index=inv_se.index,columns=inv_se.index) #1/error diagonal matrix
                    Wn = pd.DataFrame(np.diag(inv_sn),index=inv_sn.index,columns=inv_sn.index) #1/error diagonal matrix
                    Wz = pd.DataFrame(np.diag(inv_sz),index=inv_sz.index,columns=inv_sz.index) #1/error diagonal matrix

                    
                    #G-matrices with errors
                    
                    Ge=pd.DataFrame(t,index=t.index)
                    Ge['ones']=pd.DataFrame(np.array([1] * len(Ge)),index=Ge.index)
                    Gew=We@Ge
                    
                    Gn=pd.DataFrame(t,index=t.index)
                    Gn['ones']=pd.DataFrame(np.array([1] * len(Gn)),index=Gn.index)
                    Gnw=Wn@Gn
                    
                    Gz=pd.DataFrame(t,index=t.index)
                    Gz['ones']=pd.DataFrame(np.array([1] * len(Gz)),index=Gz.index) 
                    Gzw=Wz@Gz
                    
                
                    #date vectors with errors
                    
                    ew = We@e
                    nw = Wn@n
                    zw = Wz@z
                    
                    Gew_prime = Gew.transpose()
                    Gnw_prime = Gnw.transpose()
                    Gzw_prime = Gzw.transpose()
                    
                    GP_G_e = Gew_prime @ Gew
                    GP_G_n = Gnw_prime @ Gnw
                    GP_G_z = Gzw_prime @ Gzw
                    
                    try:
                        inv_GP_G_e = pd.DataFrame(np.linalg.inv(GP_G_e.to_numpy()), GP_G_e.columns, GP_G_e.index)
                    except:
                        inv_GP_G_e = pd.DataFrame(np.linalg.pinv(GP_G_e.to_numpy()), GP_G_e.columns, GP_G_e.index)
                        print("For station %s, the 'e'-component. Try pseudo inversion")

                    try:
                        inv_GP_G_n = pd.DataFrame(np.linalg.inv(GP_G_n.to_numpy()), GP_G_n.columns, GP_G_n.index)
                    except:
                        inv_GP_G_n = pd.DataFrame(np.linalg.pinv(GP_G_n.to_numpy()), GP_G_n.columns, GP_G_n.index)
                        print("For station %s, the 'n'-component. Try pseudo inversion")
                        
                    try:
                        inv_GP_G_z = pd.DataFrame(np.linalg.inv(GP_G_z.to_numpy()), GP_G_z.columns, GP_G_z.index)
                    except:
                        inv_GP_G_z = pd.DataFrame(np.linalg.pinv(GP_G_z.to_numpy()), GP_G_z.columns, GP_G_z.index)                        
                        print("For station %s, the 'z'-component. Try pseudo inversion")
                    
                    
                    #INVERSION MODELs
                    model_e = inv_GP_G_e@Gew_prime@ew
                    model_n = inv_GP_G_n@Gnw_prime@nw
                    model_z = inv_GP_G_z@Gzw_prime@zw
                    
                    e_model_at_the_step=model_e[0]*step_standards+model_e[1]
                    n_model_at_the_step=model_n[0]*step_standards+model_n[1]
                    z_model_at_the_step=model_z[0]*step_standards+model_z[1]
                    
                    median_after_e=e_model_at_the_step #from linear model
                    median_after_n=n_model_at_the_step #from linear model
                    median_after_z=z_model_at_the_step #from linear model
                    
                    
                    median_before_e=df_GPS.e[idx_before].median() #from data (median value)
                    median_before_n=df_GPS.n[idx_before].median() #from data (median value)
                    median_before_z=df_GPS.z[idx_before].median() #from data (median value)
                    
                    
                    # Modeled steps
                    diff_after_before_e = median_after_e - median_before_e
                    diff_after_before_n = median_after_n - median_before_n
                    diff_after_before_z = median_after_z - median_before_z
                    
                    
                    #Correcting.. 
                    
                    idx_end=len(df_GPS)
                    
                    if len(idx_after)!=0:             
                        idx_start=idx_after[0]
                    else: # len(idx_after)==0 Not sure when df_GPS has the first data after the step.
                        idx_start=idx_before[-1]+1+15 # First possibility 
                        
                    try:                          
                        idx_correction=list(range(idx_start,idx_end))              
                        df_GPS.loc[idx_correction,['e']]=df_GPS.loc[idx_correction,['e']]-diff_after_before_e
                        df_GPS.loc[idx_correction,['n']]=df_GPS.loc[idx_correction,['n']]-diff_after_before_n
                        df_GPS.loc[idx_correction,['z']]=df_GPS.loc[idx_correction,['z']]-diff_after_before_z
                    except: 
                        idx_start = idx_start + 1
                        idx_correction=list(range(idx_start,idx_end))
                        df_GPS.loc[idx_correction,['e']]=df_GPS.loc[idx_correction,['e']]-diff_after_before_e
                        df_GPS.loc[idx_correction,['n']]=df_GPS.loc[idx_correction,['n']]-diff_after_before_n
                        df_GPS.loc[idx_correction,['z']]=df_GPS.loc[idx_correction,['z']]-diff_after_before_z                
                        

## >> (iii) len(idx_before) >= 10 and len(idx_after) >= 10
            elif len(idx_before) >= 10 and len(idx_after) >= 10:              
                print("              case3: Great! ")
                #print(len(idx_before),len(idx_after))
                median_before_e=df_GPS.e[idx_before].median() #from data (median value)
                median_before_n=df_GPS.n[idx_before].median() #from data (median value)
                median_before_z=df_GPS.z[idx_before].median() #from data (median value)
                    
                    
                median_after_e=df_GPS.e[idx_after].median() #from data (median value)
                median_after_n=df_GPS.n[idx_after].median() #from data (median value)
                median_after_z=df_GPS.z[idx_after].median() #from data (median value)
                    
                    
                # Modeled steps
                diff_after_before_e = median_after_e - median_before_e
                diff_after_before_n = median_after_n - median_before_n
                diff_after_before_z = median_after_z - median_before_z
                    
                #Correcting.. 
                idx_start=idx_after[0]
                idx_end=len(df_GPS)
                idx_correction=list(range(idx_start,idx_end))
                    
                df_GPS.loc[idx_correction,['e']]=df_GPS.loc[idx_correction,['e']]-diff_after_before_e
                df_GPS.loc[idx_correction,['n']]=df_GPS.loc[idx_correction,['n']]-diff_after_before_n
                df_GPS.loc[idx_correction,['z']]=df_GPS.loc[idx_correction,['z']]-diff_after_before_z
        
        
        
        
        
## >> ( iv) len(idx_before) <  10 and len(idx_after) <  10 
            elif len(idx_before) < 10 and len(idx_after) < 10:
                print("              case4: Both before and after step position estimates are not enough")
                print("              >>>>>> Some position estimates will be removed")
                time_window_size_half = time_window_size/2    
                time_window_size_half = int(time_window_size_half)
                Time_window_size_worst = list(range(step_standards-time_window_size_half,step_standards+time_window_size_half+1))
                #time_window_size = 4*30 + 35 = ~5 months
                date_time_window_size_worst=ismember(Time_window_size_worst,data_datenum)
                idx_time_window_size_worst = [x for x in date_time_window_size_worst if x == x]
                df_GPS=df_GPS.drop(idx_time_window_size_worst) #drop the data. #make sure later you need to reset          
                df_GPS=df_GPS.reset_index(drop=True)
            else:
                print("*****************************")
                print("*****************************")
                print("*****************************")
                print("*****************************")
                print("WARNING! : something is wrong")
                print("*****************************")
                print("*****************************")
                print("*****************************")
                print("*****************************")
                
## (g) REMOVE ALL POSITION ESTIMATES on the date of step(s)
    
        IDX_event_data_overlap=ismember(event_datenum,data_datenum) # Find if we have position estimates
        cleanedList = [x for x in IDX_event_data_overlap if x == x] # get rid of float('NaN') from the list
        if len(cleanedList)!=0:            
            try:
                df_GPS=df_GPS.drop(cleanedList)                
            except: 
                K = len(cleanedList)               
                for k in range(K):
                    try:
                        df_GPS=df_GPS.drop(cleanedList[k])
                    except:
                        continue          
    
## (h) Save corrected data

    df_GPS=df_GPS.reset_index() # reset index
    df_GPS.e = df_GPS.e/1000
    df_GPS.n = df_GPS.n/1000
    df_GPS.z = df_GPS.z/1000
    df_GPS.se = df_GPS.se/1000
    df_GPS.sn = df_GPS.sn/1000
    df_GPS.sz = df_GPS.sz/1000
    df_GPS=df_GPS[['time','lon','lat','e','n','z','se','sn','sz','corr_en','flag']]
    

    savefile = "stepCorrected_"+str(i+1) #output file = stepCorrected_"$i"
    df_GPS.to_csv(savefile ,header=None, index=None,sep=' ',float_format='%g') #SAVE AS THEY ARE
    
#    df_GPS.to_csv(savefile ,header=None, index=None,sep=' ',float_format='%.6f')


# In[ ]:




