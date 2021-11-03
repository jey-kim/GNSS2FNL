#!/usr/bin/env python
# coding: utf-8

# <img src="Figs/GEOS_Logo.pdf" width="500" />

# 
# # Step **7** of **`G2FNL`**: <font color=blue>"fill_entire_time.ipynb"</font>
# #### Oct 2, 2021  <font color=red>(v. 1.0.0)</font>
# ##### Jeonghyeop Kim (jeonghyeop.kim@gmail.com)
# 
# > input files: **`stepCorrected_i"`**, **`time_vector.dat`**, and **`station_list_full.dat`** \
# > output files: **`zeroFilled_i`** 
# 
# 0. This code is a part of GPS2FNL process 
# 1. This code will use `time_vector.dat` 
# 2. It will make a matrix with the time vector as the first column of it. 
# 3. If no data is available for a day, this code will fill up zero values. 
# 

# <div class="alert alert-danger">
# Do NOT run this code twice without re-starting the kernel
# </div>

# In[1]:


# 1. import modules
import numpy as np
import pandas as pd
#pd.__version__
import os


# In[2]:


current_dir=os.getcwd()
os.getcwd()


# In[3]:


# 2. read a file for the time vector
filename = 'time_vector.dat'
time_vec = pd.read_csv(filename,sep=' ',header=None)
time_vec.columns = ['date']


list_full = "station_list_full.dat"
df_list=pd.read_csv(list_full, header=None)
N_list = len(df_list) 


# In[4]:


processing_dir = os.path.join(current_dir, 'data', 'processing')
os.chdir(processing_dir) # cp to processing directory
os.getcwd()


# In[5]:


# # Make zeros matrix template! 
# zeros_np_array=np.zeros((len(time_vec),10))
# df_zeros = pd.DataFrame(zeros_np_array, columns = ['lon','lat','ue','un','uz','se','sn','sz','corr_en','flag'])
# template_frame = [time_vec, df_zeros]

# #This DF is the template
# df_save_template = pd.concat(template_frame, axis=1) 


# # NOTE: 
# **The cell above is not needed if one uses df.merge in-built function** \
# **see this stackoverflow thread: [click](https://stackoverflow.com/questions/53645882/pandas-merging-101)** \
# `pd.merge 101` 

# In[6]:


for i in range(0,N_list):  #range(N_list)

    inputfile = "stepCorrected_"+str(i+1) #input_file = stepCorrected_"$i"
    df_input=pd.read_csv(inputfile,sep=' ',header=None) 
    df_input.columns = ['date','lon','lat','ue','un','uz','se','sn','sz','corr_en','flag'] #columns

    df_save=time_vec.merge(df_input, on='date', how='left')
    # MERGE the two data frames based on 'date' column. 
    # ** time_vec (full time period) is the left dF.
    # ** df_input (stepCorrected_i) is the right dF. 
    # how='left' means that 
    # MERGE them together filling all empty elements of df_input (right), 
    # comparing with time_vector (left), with NaN
    
    df_save=df_save.fillna(float(0))
    savefile = "zeroFilled_"+str(i+1) #output file = zeroFilled_"$i"
    df_save.to_csv(savefile ,header=None, index=None ,float_format='%.6f', sep=' ') #SAVE AS THEY ARE


# In[ ]:




