#!/usr/bin/env python
# coding: utf-8

# <img src="Figs/GEOS_Logo.pdf" width="500"/> 

# 
# # Step **1** of **`G2FNL`**: <font color=blue>"download_files.ipynb"</font>
# #### Sep 13, 2021  <font color=red>(v. 1.0.1)</font> 
# ##### Jeonghyeop Kim (jeonghyeop.kim@gmail.com) 
# 
# > input prompts: **`yes`** or **`no`** & **`yes`** or **`no`**\
# > input files: **`list_default.dat`** \
# > output files: **`steps.txt`**, **`station_list_full.txt`**, and **`coordinate_list_full.dat`**
# 
# 
# 0. This code is a part of G2FNL process (Project1: GNSS to FNL)
# 1. It is required to specify a longitude and latitude boundary (see the first block of this notebook).
# 2. This code will download GNSS position data provided by the Nevada Geodetic Laboratory 
# 3. This code will also download metadata for steps (steps.txt), which will be used for corrections.
# 4. **One can choose to download all data (except MAGNET), PBO (old), or NOTA.** 
# 5. If one chose to download all data or NOTA only, analyses of the vertical position estimates will be required later.
# 6. Later in this code, the threshold of minimum daily position estimates will be determined. 
#  > The minimum number of daily position estimates: \
#  > if one wants the PBO or NOTA stations, threshold_num = 0 (to include all NOTA stations) \
#  > Otherwise, threshold_num = 200
# 
# 
# **`The NGL website is available at:`**  [click here](http://geodesy.unr.edu)
# 
# > On the right side of the website, find **"Downloadable Lists of GPS Data Holdings:"** \
# > This algorithm uses data from "stations with 24 hour sample rate solutions, final orbits, 2 week latency." 
# 
# 
# 

# In[1]:


# Specify Location Boundary
lon_min=235.43
lon_max=246.99
lat_min=31.31
lat_max=42.99


# In[2]:


#import modules
import numpy as np
import pandas as pd
import urllib
# In[3]:


# A list of all GNSS stations from the NGL 
url_list="http://geodesy.unr.edu/NGLStationPages/DataHoldings.txt" # URL
list_file="list_NGL.txt" # file name. # This file will be removed

# metadata for steps from the NGL
url_metadata="http://geodesy.unr.edu/NGLStationPages/steps.txt" # URL
metadata_file="steps.txt" # file name


# In[4]:


# Download the list of GNSS stations (final orbits) and metadata 
try:
    urllib.request.urlretrieve(url_list, list_file)
    urllib.request.urlretrieve(url_metadata, metadata_file)
    print("Downloaded metadata for discontinuous steps from the NGL")
except:
    import urllib.request
    urllib.request.urlretrieve(url_list, list_file)
    urllib.request.urlretrieve(url_metadata, metadata_file)
    print("Downloaded metadata for discontinuous steps from the NGL")

# In[5]:


# Read the station list.
df_original_list=pd.read_csv(list_file ,header=None, sep=r'(?:,|\s+)', 
                comment='#', engine='python',
                names=['Sta','lat','lon','3','4','5','6','7','8','9','NumSol','11','12','13'])


# Here the first 4 columns will be used.
df_four_cols=df_original_list.loc[1:len(df_original_list),['Sta','lat','lon','NumSol']] #first three columns
df_four_cols=df_four_cols.reset_index(drop=True)

# str to float
df_four_cols['lon'] = df_four_cols['lon'].astype(float)
df_four_cols['lat'] = df_four_cols['lat'].astype(float)
df_four_cols['NumSol'] = df_four_cols['NumSol'].astype(int)


# In[6]:


# While the user input is not either yes or no, this loop will repeat

while True:      
    print(" > If you want to include all GNSS stations in California, type 'yes'.")
    print(" >> If you type 'no', only NOTA stations will be downloaded.")
    YESorNO=input(" type 'yes' or 'no' ")
    YESorNO=YESorNO.lower()
    
    while YESorNO not in ("yes","no"):
        print("*** Please type 'yes' or 'no' ***")
        YESorNO=input(" type 'yes' or 'no' ")
        YESorNO=YESorNO.lower()
        
    if YESorNO == "no" or YESorNO == "yes":
        break 
        #break the while loop
         

# YES! => all stations (except MAGNET stations) will be downloaded.
if YESorNO.startswith('y'): 
    # Select stations within the region of interest.
    # > lon_min,lon_max,lat_min,lat_max must be defined.
    
    threshold_num=200
    df_interest=df_four_cols.loc[(df_four_cols['lat'] >= lat_min)                            & (df_four_cols['lat'] <= lat_max)                            & (df_four_cols['lon'] >= lon_min)                            & (df_four_cols['lon'] <= lon_max)                            & (df_four_cols['NumSol'] >= threshold_num)]

    df_interest=df_interest.reset_index(drop=True)
    
    #REMOVE MAGNET STATIONS FROM THE LIST
    URL_MAGNET="http://geodesy.unr.edu/magnet/Table2web.html"
    df_MAGNET=pd.read_html(URL_MAGNET, header=1, flavor = 'bs4')
    df_MAGNET=df_MAGNET[0]
    df_MAGNET.columns=['Sta','1','2','3','4','5','6']
    df_no_MAGNAT = df_interest[~df_interest['Sta'].isin(df_MAGNET['Sta'])].reset_index(drop=True)
    df_final = df_no_MAGNAT
    
# NO!
else: 
    
    threshold_num=0
    df_interest=df_four_cols.loc[(df_four_cols['lat'] >= lat_min)                            & (df_four_cols['lat'] <= lat_max)                            & (df_four_cols['lon'] >= lon_min)                            & (df_four_cols['lon'] <= lon_max)                            & (df_four_cols['NumSol'] >= threshold_num)]

    df_interest=df_interest.reset_index(drop=True)
    
    
    #NOTA vs PBO?
    while True:      
        print(" > You chose to download NOTA stations only.")
        print(" >> Do you want to include some decommissioned PBO stations (~120) in addition to NOTA stations?")
        YESorNO=input(" type 'yes' or 'no' ")
        YESorNO=YESorNO.lower()
    
        while YESorNO not in ("yes","no"):
            print("*** Please type 'yes' or 'no' ***")
            YESorNO=input(" type 'yes' or 'no' ")
            YESorNO=YESorNO.lower()
        
        if YESorNO == "no" or YESorNO == "yes":
            break 
            #break the while loop
    
    if YESorNO.startswith('y'): #YES => use PBO
        list_default="list_default.dat" # pre-existing PBO stations for California. 
        df_default=pd.read_csv(list_default, header=None, names=['Sta'])    
        df_NOTA = df_interest[df_interest['Sta'].isin(df_default['Sta'])].reset_index(drop=True)
        df_final = df_NOTA
    else: #NO => use NOTA only! 
        
        url_UNAVCO="https://data.unavco.org/archive/gnss/products/position/gage_gps.igs14.txt"
        list_UNAVCO="list_UNAVCO.txt" # LIST is from UNAVCO webpage.
        urllib.request.urlretrieve(url_UNAVCO, list_UNAVCO)
        df_UNAVCO_list=pd.read_csv(list_UNAVCO , sep=',', 
                comment='#', engine='python',
                names=['Sta','1','2','3','4','5','6','7','8','9','10','11','12','13'])
        df_NOTA = df_interest[df_interest['Sta'].isin(df_UNAVCO_list['Sta'])].reset_index(drop=True)
        df_final = df_NOTA


# In[7]:


df_station=df_final.loc[:,['Sta']]


# In[8]:


df_coor=df_final.loc[:,['lon','lat']]


# In[9]:


#SAVE FILES 
# coordinates and station list
df_station.to_csv('station_list_full.dat',header=None, index=None,sep=' ',float_format='%g')
df_coor.to_csv('coordinate_list_full.dat',header=None, index=None, sep=' ',float_format='%g')


# In[10]:


#Remove some unwanted files
get_ipython().system('rm list_NGL.txt ')
get_ipython().system('rm list_UNAVCO.txt ')


# In[11]:


# mkdir archive folder
import os 
current_dir = os.getcwd()
archive_dir = os.path.join(current_dir,'data', 'archive')
processing_dir = os.path.join(current_dir, 'data', 'processing')
print("Your current directory:", current_dir)
print("Your level-2 GNSS data will be saved at:", archive_dir)
print("Your processed FNL files will be at:", processing_dir)
print("")
try:
    os.makedirs(archive_dir, exist_ok=False)
except: 
    print ("%s is aleady exist." %archive_dir)
try: 
    os.makedirs(processing_dir, exist_ok=False)
except: 
    print ("%s is aleady exist." %processing_dir)
    
os.chdir(current_dir)
os.getcwd() 

#Pass python str variable archive_dir to the next cell with 'bash magic'
os.environ["DATA_PATH"] = archive_dir


# In[12]:


print("downloading GNSS data....")


# In[13]:


get_ipython().run_cell_magic('bash', '', 'echo $DATA_PATH\nwhile IFS= read -r line || [[ -n "$line" ]]; do\n    echo "Text read from file: $line"\n    curl -X GET \'http://geodesy.unr.edu/gps_timeseries/tenv3/IGS14/\'$line\'.tenv3\' > $line.txt\n    cp $line.txt $DATA_PATH\n    rm $line.txt\ndone < station_list_full.dat')


# In[ ]:





# In[ ]:





# In[ ]:




