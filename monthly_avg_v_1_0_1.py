#!/usr/bin/env python
# coding: utf-8

# <img src="Figs/GEOS_Logo.pdf" width="500" />

# 
# # Step **10** of **`G2FNL`**: <font color=blue>"monthly_avg.ipynb"</font>
# #### Oct 20, 2021  <font color=red>(v. 1.0.1)</font>
# ##### Jeonghyeop Kim (jeonghyeop.kim@gmail.com)
# 
# > input files: **`outlierRemoved_i"`**, **`days_per_month.dat`**, and **`station_list_full.dat`** \
# > output files: **`monthlyAvg_i`** 
# 
# 0. This code is a part of GPS2FNL process.
# 1. It will calculate monthly average position.
# 2. If the number of position estimates for a month is smaller than 6, the previous code already remove the position values. 
# 3. Simply take monthly average values. 
# 

# <div class="alert alert-danger">
# Do NOT run this code twice without re-starting the kernel
# </div>

# In[ ]:


# 1. import modules
import numpy as np
import pandas as pd
#pd.__version__
import os


# In[ ]:


current_dir=os.getcwd()
os.getcwd()


# In[ ]:


# 2. read a file for the time vector
filename = 'days_per_month.dat'
time_vec = pd.read_csv(filename,sep=' ',header=None)
time_vec.columns = ['daysMonth']


list_full = "station_list_full.dat"
df_list=pd.read_csv(list_full, header=None)
df_list.columns = ['stID']
N_list = len(df_list) 


# In[ ]:


processing_dir = os.path.join(current_dir, 'data', 'processing')
os.chdir(processing_dir) # cp to processing directory
os.getcwd()


# In[ ]:


for i in range(N_list):

    inputfile = "outlierRemoved_"+str(i+1) #input_file = outlierRemoved_"$i"
    df_input=pd.read_csv(inputfile,sep=' ',header=None)  
    df_input.columns = ['date','lon','lat','ue','un','uz','se','sn','sz','corr_en','flag'] #columns
    
    df_coor = df_input[(df_input['lon']!=0) & df_input['lat']!=0]
    df_coor = df_coor.reset_index(drop=True)
    lon=df_coor.iloc[0,1]
    lat=df_coor.iloc[0,2]
    
    end = 0
    
    
    avg_ue_total = []
    avg_un_total = []
    avg_uz_total = []
    se_propagated_total = []
    sn_propagated_total = []
    sz_propagated_total = []
    corr_total = []
    flag_total = []
    
    for j in range(len(time_vec)): 
        start = end
        end = end + time_vec.daysMonth.values[j]
        disp_3D = df_input.iloc[start:end,3:6] 
        disp_3D = disp_3D[(disp_3D['ue']!=0) & (disp_3D['un']!=0) & (disp_3D['un']!=0)]

        error_3D = df_input.iloc[start:end,6:9] 
        error_3D = error_3D[(error_3D['se']!=0) & (error_3D['sn']!=0) & (error_3D['sn']!=0)]

        
        
        if len(disp_3D)!=0:
            avg_ue=disp_3D.mean().values[0]
            avg_un=disp_3D.mean().values[1]
            avg_uz=disp_3D.mean().values[2]
        
            #error propagation 
            var_3D = error_3D**2
            N = len(var_3D)
            
            
            sum_var_e=var_3D.sum()[0]
            sum_var_e_sqrt = np.sqrt(sum_var_e)
            se_propagated=sum_var_e_sqrt/N
            
            sum_var_n=var_3D.sum()[1]
            sum_var_n_sqrt = np.sqrt(sum_var_n)
            sn_propagated=sum_var_n_sqrt/N
            
            sum_var_z=var_3D.sum()[2]
            sum_var_z_sqrt = np.sqrt(sum_var_z)
            sz_propagated=sum_var_z_sqrt/N

            corr=0.5 # arbitrarily chosen.
            flag=1
            
            
        else:
            avg_ue = 0 
            avg_un = 0
            avg_uz = 0 
            se_propagated=0 
            sn_propagated=0
            sz_propagated=0
            corr=0
            flag=0
            
        avg_ue_total.append(avg_ue)
        avg_un_total.append(avg_un)
        avg_uz_total.append(avg_uz)
        se_propagated_total.append(se_propagated)
        sn_propagated_total.append(sn_propagated)
        sz_propagated_total.append(sz_propagated)
        corr_total.append(corr)
        flag_total.append(flag)
        
        
    dict = {'ue': avg_ue_total,             'un': avg_un_total,             'uz': avg_uz_total,             'se': se_propagated_total,             'sn': sn_propagated_total,             'sz': sz_propagated_total,             'corr': corr_total,             'flag': flag_total}
  
    df_save = pd.DataFrame(dict)
    df_save['lon']=np.ones((len(df_save),1))*lon
    df_save['lat']=np.ones((len(df_save),1))*lat
    
    df_save = df_save[['lon','lat','ue','un','uz','se','sn','sz','corr','flag']]
    df_save = df_save.reset_index(drop=True)
    savefile = "monthlyAvg_"+str(i+1) #output file = monthlyAvg_"$i"
    df_save.to_csv(savefile ,header=None, index=None ,float_format='%.6f', sep=' ') 


# In[ ]:





# In[ ]:




