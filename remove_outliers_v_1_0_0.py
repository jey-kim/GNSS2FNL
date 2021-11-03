#!/usr/bin/env python
# coding: utf-8

# <img src="GEOS_Logo.pdf" width="500" />

# 
# # Step **8** of **`G2FNL`**: <font color=blue>"remove_outliers.ipynb"</font>
# #### Oct 19, 2021  <font color=red>(v. 1.0.0)</font>
# ##### Jeonghyeop Kim (jeonghyeop.kim@gmail.com)
# 
# > input files: **`zeroFilled_i`**, **`days_per_month.dat`**, **`station_list_full.dat`**,  **`steps.txt`**, and **`time_vector.dat`** \
# > output files: **`outlierRemoved_i`** : <font color=red>UNIT will be changed [m] to [mm]</font>
# 
# 
# 0. This code is a part of GPS2FNL process 
# 1. It will get rid of outliers.  
# > Position data for each month will be treated as a set. \
# > The code will fit a linear line to each month and then subtract this model from the data. \
# > Perform a simple statistical analysis for the residual. \
# > Outliers for each month are defined as any data outside of the tolerance level. \
# > The default tolerance level is +/- 3 sigma. \
# > If fewer than 6 positions are available for a month, this code will remove the data for the month.
# 2. Potential issues: 
# > There exist some stations that still show problematic outliers after this algorithm applied. \
# > Possibly some post-seismic signals are identified as outliers and removed, which means a loss of interesting signal. \
# > Maybe pass the month if an earthquake occurred in that month?
# 
# 3. <font color=red>** NOTE! UNIT will be changed [m] to [mm] **</font>
# 4. If this algorithm identifies an outlier for a day for a component, it will remove the other two components for the day.

# <div class="alert alert-danger">
# Do NOT run this code twice without re-starting the kernel
# </div>

# In[1]:


threshold = 3
# outlier defined as the residual position estimates outside of the 3-sigma range for each month.

turnoff_print = 1


# In[2]:


# 1. import modules
import numpy as np
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt


# In[3]:


current_dir=os.getcwd()
os.getcwd()


# In[4]:


# 2. read files for (1) Number of Date per each month 
#               and (2) Number of Stations 
#               and (3) time_vector.dat for the first and end dates of the analysis
#               and (4) earthquake-related steps


#############################################
#(1)
datefile = 'days_per_month.dat'
dateNvec = pd.read_csv(datefile, sep = ' ', header = None)
dateNvec.columns = ['NofD']

#############################################
#(2)
list_full = "station_list_full.dat"
df_list=pd.read_csv(list_full, header=None)
df_list.columns=['StID']
N_list = len(df_list) 


#############################################
#(3)
timefile = 'time_vector.dat'
df_time=pd.read_csv(timefile, header=None)
startDateAnalysis=int(df_time.iloc[0])
endDateAnalysis=int(df_time.iloc[-1])
##########################################################################################
#(4)
metadata = "steps.txt" #file name
df_metadata=pd.read_csv(metadata, header=None, names=list('0123456'), sep=r'(?:,|\s+)',                         comment='#', engine='python')
## steps.txt is in an irregular shape
## 'names=list('0123456')' is to fill empty spots with NaN 
df_steps_earthquakes = df_metadata[df_metadata['2'] == 2].reset_index(drop=True)
df_steps_earthquakes.columns=['stID','time','flag','threshold','distance','mag','eventID'] 
#The step data has a time column in the form of yyMMMdd 
date_old = df_steps_earthquakes.time.tolist() # A DataFrame to a list
date_new = pd.to_datetime(date_old, format='%y%b%d').strftime('%Y%m%d') # convert date format
df_steps_earthquakes.loc[:,'time'] = date_new # replaces with the new date  in YYYYMMDD
df_steps_earthquakes['time']=df_steps_earthquakes['time'].astype(int) #str to int
df_steps_earthquakes = df_steps_earthquakes[(df_steps_earthquakes['time']>=startDateAnalysis) &                                             (df_steps_earthquakes['time']<=endDateAnalysis)]
df_steps_earthquakes = df_steps_earthquakes.reset_index(drop=True)


# In[5]:


processing_dir = os.path.join(current_dir, 'data', 'processing')
os.chdir(processing_dir) # cp to processing directory
os.getcwd()


# # **`IDENTIFY AND ELIMINATE OUTLIERS`**
# 
# ### FIT position data for each month with a line (LSM). 
# ### SUBTRACT the linear model from the data for the month. 
# ### DEFIND as outliers if the residuals are out of the 3 sigma range.
# ### REPLACE the outliers with zero values.

# In[6]:


N_months = len(dateNvec) # How many months for the time period of interest?

##############################################
# STEP 1: Read data files station by station #
##############################################

column_names = ['datenum','date','lon','lat','ue','un','uz','se','sn','sz','corr_en','flag']

for i in range(N_list):  

    inputfile = "zeroFilled_"+str(i+1) #input_file = zeroFilled_"$i"
    df_input=pd.read_csv(inputfile,sep=' ',header=None)   
    df_input = df_input.reset_index() #Index column will be added and will be used as 'datenum' consecutive integers.
    df_input.columns = column_names
    df_input.loc[:,['datenum']]=df_input.loc[:,['datenum']]+1 #datenum starts from 1 instead of 0
    df_input.loc[:,['ue']]=df_input.loc[:,['ue']]*1000 # [m] to [mm]
    df_input.loc[:,['un']]=df_input.loc[:,['un']]*1000 # [m] to [mm]
    df_input.loc[:,['uz']]=df_input.loc[:,['uz']]*1000 # [m] to [mm]
    df_input.loc[:,['se']]=df_input.loc[:,['se']]*1000 # [m] to [mm]
    df_input.loc[:,['sn']]=df_input.loc[:,['sn']]*1000 # [m] to [mm]
    df_input.loc[:,['sz']]=df_input.loc[:,['sz']]*1000 # [m] to [mm]
    df_input.loc[:,['corr_en']]=df_input.loc[:,['corr_en']]*1000 # [m] to [mm]
    stationID=df_list.loc[i,['StID']]
    stationID=stationID.tolist()[0]

##############################################
# STEP 2: READ DATA MONTH BY MONTH!          #
##############################################

    FirstMonth = 0
    for j in range(N_months):
        date_for_the_month=int(dateNvec.iloc[j])
        LastMonth = FirstMonth + date_for_the_month
        df_month = df_input.loc[FirstMonth:LastMonth-1,:].reset_index(drop=True)
        FirstMonth = LastMonth
        
        df_month_nonzero = df_month[(df_month['lon']!=0) & (df_month['lat']!=0)]
        df_month_nonzero = df_month_nonzero.reset_index(drop=True)    
        
##############################################
# STEP 3: Decide to pass the month or not    #
##############################################

        # 3-a The number of non-zero values is less than 6 : skip 
        if len(df_month_nonzero) == 0:    
            if turnoff_print !=1:
                print("few positions for the month %s for station %s : Skip this month" %(str(f"{j:03}"),stationID))
            continue
        elif len(df_month_nonzero) > 0 and len(df_month_nonzero) < 6:
            # HERE 
            few_data_idx = df_month_nonzero['datenum'] - 1
            few_data_idx = few_data_idx.tolist()
            df_input.iloc[few_data_idx,[2,3,4,5,6,7,8,9,10,11]] = 0 
            # remove the position estimates defined as outliers  
            if turnoff_print !=1:
                print("few positions for the month %s for station %s : Skip this month" %(str(f"{j:03}"),stationID))
            continue
            
        # 3-b An earthquake occurred within that month : skip    
        IniTimeNonzeroMonth=df_month_nonzero.iloc[0,1]
        EndTimeNonzeroMonth=df_month_nonzero.iloc[-1,1]
        df_steps_exist=df_steps_earthquakes[(df_steps_earthquakes['stID']==stationID) &                                     (df_steps_earthquakes['time']>=IniTimeNonzeroMonth) &                                     (df_steps_earthquakes['time']<=EndTimeNonzeroMonth)]    
        
        if len(df_steps_exist) != 0:  
            if turnoff_print !=1:
                print("Earthquake within the month %s for station %s : Skip this month" %(str(f"{j:03}"),stationID))
            continue
            
        # 3-c Fit the data with a line and get the residual    
        else: 
            t = df_month_nonzero.loc[:,['datenum']]
            ux = df_month_nonzero.loc[:,['ue']]
            uy = df_month_nonzero.loc[:,['un']]
            uz = df_month_nonzero.loc[:,['uz']]
            sx = df_month_nonzero.loc[:,['se']]
            sy = df_month_nonzero.loc[:,['sn']]
            sz = df_month_nonzero.loc[:,['sz']]
            

            # Build G-matrix for a line
            G_matrix = t
            G_matrix['cont']=np.ones((len(t),1))
            
            # Build diagonal weighting matrice for the three components
            sx_inv = 1/sx
            sx_inv = sx_inv.to_numpy()  
            wx = np.diag(sx_inv[:,0])
            wx = pd.DataFrame(wx)
            
            sy_inv = 1/sy
            sy_inv = sy_inv.to_numpy()  
            wy = np.diag(sy_inv[:,0])
            wy = pd.DataFrame(wy)
            
            sz_inv = 1/sz
            sz_inv = sz_inv.to_numpy()  
            wz = np.diag(sz_inv[:,0])
            wz = pd.DataFrame(wz)
            
            # Wd, WG
            x = wx @ ux
            y = wy @ uy
            z = wz @ uz
            Gx = wx @ G_matrix
            Gy = wy @ G_matrix
            Gz = wz @ G_matrix
            
            
            # Inversion (LSM)           
            # G'
            GxT = Gx.transpose()
            GyT = Gy.transpose()
            GzT = Gz.transpose()
            # G'G
            GpG_x=GxT @ Gx
            GpG_y=GyT @ Gy
            GpG_z=GzT @ Gz
            # inv(G'G)
            GpG_x_inv= pd.DataFrame(np.linalg.inv(GpG_x.to_numpy()), GpG_x.columns, GpG_x.index)
            GpG_y_inv= pd.DataFrame(np.linalg.inv(GpG_y.to_numpy()), GpG_y.columns, GpG_y.index)
            GpG_z_inv= pd.DataFrame(np.linalg.inv(GpG_z.to_numpy()), GpG_z.columns, GpG_z.index)
            # mL2 = inv(G'G)G'd
            model_x = GpG_x_inv @ GxT @ x
            model_y = GpG_y_inv @ GyT @ y
            model_z = GpG_z_inv @ GzT @ z
            # predictions & residuals & standard deviations 
            x_pred = G_matrix @ model_x           
            x_residual = ux - x_pred     
            sigma_x=x_residual.std()
            x3std=float(threshold*sigma_x)
            
            y_pred = G_matrix @ model_y           
            y_residual = uy - y_pred     
            sigma_y=y_residual.std()
            y3std=float(threshold*sigma_y)
            
            z_pred = G_matrix @ model_z           
            z_residual = uz - z_pred     
            sigma_z=z_residual.std()
            z3std=float(threshold*sigma_z)
            
            # CHECK Outliers
            x_target=x_residual.loc[(x_residual['ue']>=x3std) | (x_residual['ue']<=-1*x3std)]
            y_target=y_residual.loc[(y_residual['un']>=y3std) | (y_residual['un']<=-1*y3std)]
            z_target=z_residual.loc[(z_residual['uz']>=z3std) | (z_residual['uz']<=-1*z3std)]
            
            # ADD monthly index numbers to the dataframe 
            x_target=x_target.reset_index() 
            x_target=x_target.loc[:,['index']]
            y_target=y_target.reset_index()
            y_target=y_target.loc[:,['index']]
            z_target=z_target.reset_index()
            z_target=z_target.loc[:,['index']]

            frame = [x_target, y_target, z_target]
            target_for_month = pd.concat(frame, ignore_index=True)


            if len(target_for_month)>0:
                indexOutlierMonth=target_for_month['index'].unique().tolist()
                
                # monthly index to entire index for outlier(s)
                target_entire_time=df_month_nonzero.loc[indexOutlierMonth,['datenum']] - 1  
                # datenum = index + 1; index = datenum - 1
                
                idx_outlier=target_entire_time['datenum'].tolist()
                df_input.iloc[idx_outlier,[2,3,4,5,6,7,8,9,10,11]] = 0 # remove the position estimates defined as outliers
                if turnoff_print !=1:
                    print("outlier found for the month %s for station %s : Remove outliers" %(str(f"{j:03}"),stationID))
            else: 
                if turnoff_print !=1:
                    print("no outlier(s) for the month %s for station %s : Skip this month" %(str(f"{j:03}"),stationID))
    
    df_save = df_input[['date','lon','lat','ue','un','uz','se','sn','sz','corr_en','flag']]
    df_save = df_save.reset_index(drop=True)
    
    
    # FINALLY REMOVE all data with se > 10 or sn > 10 or sz > 20
    idx_big_error=df_save[(df_save['se']>=10) | (df_save['sn']>=10) | (df_save['sz']>=20)].index.values
    idx_big_error=idx_big_error.tolist()
    if len(idx_big_error)!=0:
        #if len(idx_big_error)==1:        
        df_save.loc[idx_big_error,['lon','lat','ue','un','uz','se','sn','sz','corr_en','flag']]=0
        #print(i)
    outputfile = "outlierRemoved_"+str(i+1) #output_file = outlierRemoved_"$i"
    df_save.to_csv(outputfile ,header=None, index=None ,float_format='%.6f', sep=' ')


# In[ ]:





# In[ ]:




