#!/usr/bin/env python
# coding: utf-8

# <img src="Figs/GEOS_Logo.pdf" width="500" />

# 
# # Step **12** of **`G2FNL`**: <font color=blue>"diff.ipynb"</font>
# #### Oct 23, 2021  <font color=red>(v. 1.0.0)</font>
# ##### Jeonghyeop Kim (jeonghyeop.kim@gmail.com)
# 
# > input files: **`elasticOnly_i`**, **`time_vector.dat`**, and **`station_list_full.dat`** \
# > output files: **`displacement_i`**, **`displacement_time_label.dat`**
# 
# 0. This code is a part of GPS2FNL process.
# 1. It will calculate **4-month** displacements 
# 2. 6-month displacements can be obtained as well. 
# 3. **`displacement_time_label.dat`** is for the time label (the last month of the displacements) 
# 

# <div class="alert alert-danger">
# Do NOT run this code twice without re-starting the kernel
# </div>

# In[1]:


# 1. import modules
import numpy as np
import pandas as pd
import os


# In[2]:


#displacements over how many months?
mo = 4


# In[3]:


current_dir=os.getcwd()
os.getcwd()


# In[4]:


# Read a 'time_vector.dat' and get a label 
filename = 'time_vector.dat'
time_vec = pd.read_csv(filename,sep=' ',header=None)
time_vec.columns = ['time_vector']
date_old = time_vec.time_vector.tolist() # A DataFrame to a list
date_new = pd.to_datetime(date_old, format='%Y%m%d').strftime('%Y%m') # convert date format
time_vec.loc[:,'new_time_vector'] = date_new # replaces with the new date in YYYYMM
time_vec.loc[:,'new_time_vector']=time_vec.loc[:,'new_time_vector'].astype(int) #str to int
df_new_time = time_vec[['new_time_vector']].reset_index(drop=True)
array_month_label = df_new_time['new_time_vector'].unique()


array_diff_label = array_month_label[mo:]
df_diff_label = pd.DataFrame(array_diff_label)
df_diff_label.columns=['label'] 
df_diff_label.to_csv("displacement_time_label.dat" ,header=None, index=None ,float_format='%g')

list_full = "station_list_full.dat"
df_list=pd.read_csv(list_full, header=None)
df_list.columns = ['stID']
N_list = len(df_list) 


# In[5]:


processing_dir = os.path.join(current_dir, 'data', 'processing')
os.chdir(processing_dir) # cp to processing directory
os.getcwd()


# In[6]:


for i in range(N_list):

    inputfile = "elasticOnly_"+str(i+1) #input_file = elasticOnly_"$i"
    df_input=pd.read_csv(inputfile,sep=' ',header=None)  
    df_input.columns = ['lon','lat','ue','un','uz','se','sn','sz','corr_en','flag'] #columns
    
    if df_input.ue.sum()==0: # all the values are 0 
        df_save = df_input.iloc[4:,0:8].reset_index(drop=True)
        savefile = "displacement_"+str(i+1) #output file = displacement_"$i"
        df_save.to_csv(savefile ,header=None, index=None ,float_format='%.6f', sep=' ')
        continue
        
        
   
    lon=df_input.iloc[0,0]
    lat=df_input.iloc[0,1]

    array_frame = np.zeros((len(df_input)-mo,8))
    
    for diff in range(len(df_input)-mo):
    #mo = 4 or 6. This variable is defined in the begining of this code.
        ini = diff #initial position
        fi = diff+mo #final position
        #print("displacement between %i and %i" %(fi, ini))
        if df_input.ue[fi]!=0 and df_input.ue[ini]!=0 and df_input.un[ini]!=0 and df_input.un[fi]!=0:
            
            ue_diff = df_input.ue[fi]-df_input.ue[ini]
            un_diff = df_input.un[fi]-df_input.un[ini]
            
            se_diff = np.sqrt(df_input.se[fi]**2+df_input.se[ini]**2)
            sn_diff = np.sqrt(df_input.sn[fi]**2+df_input.sn[ini]**2)
            
            
            array_frame[diff,0]=lon
            array_frame[diff,1]=lat
            array_frame[diff,2]=ue_diff
            array_frame[diff,3]=un_diff
            array_frame[diff,4]=se_diff
            array_frame[diff,5]=sn_diff
            array_frame[diff,6]=0.5
            array_frame[diff,7]=1
      
    
    df_save = pd.DataFrame(array_frame)
    df_save.columns = ['lon','lat','ue','un','se','sn','corr','flag']

    savefile = "displacement_"+str(i+1) #output file = displacement_"$i"
    df_save.to_csv(savefile ,header=None, index=None ,float_format='%.6f', sep=' ') 


# In[ ]:





# In[ ]:




