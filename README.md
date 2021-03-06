# GNSS2FNL [From GNSS position timeseries measurements to 4-mo displacement field]

`jeonghyeop Kim` (jeonghyeop.kim@gmail.com) \
APR 01, 2022

## These codes download and preprocess GNSS position timeseries data to generate 4-month displacement fields.
### The displacement fields are saved in `data/processing/*.fnl` 

### HOW TO USE this repository 
- Install ipython
- **`alias python=python3`**
- Clone the entire repository: *git clone https://github.com/jey-kim/GNSS2FNL.git* 
- Go to the cloned directory and run **`process_GNSS2FNL.sh`** *sh process_GNSS2FNL.sh* 
>    Running process_GNSS2FNL.sh will download GNSS data, preprocess GNSS position time series measurements, and generate **`*.fnl`** files. \
>    Each of the **`*.fnl`** files is a 4-month displacement field for a month. \
>    To know the month and year of a displacement field (a `*.fnl` file), check the output file **`displacement_time_label.dat`** 
>>    The element in the ith row of **`displacement_time_label.dat`** file is the month and year for a `i.fnl` file.




#### *STEPS* 
\
STEP01:download_files  (v.1.0.1) \
STEP02:preprocess_data  (v.1.0.2) \
STEP03:ch_date_unr  (v.1.0.2) \
STEP04:time_vector_generator  (v.1.0.1) \
STEP05:remove_data_outside_analysis_period  (v.1.0.2) \
STEP06:correct_steps  (v.1.0.3) \
STEP07:fill_entire_time  (v.1.0.0) \
STEP08:remove_outliers  (v.1.0.1) \
STEP09:plot_time_series  (v.1.0.3) \
STEP10:monthly_avg  (v.1.0.1) \
STEP11:vertical_timeseries_analysis  (v 0.0.0) 
> Use the previous analysis for now (vertical_analysis_PBO.out) \
> Update later (10/28/2021) 

STEP12:diff  (v.1.0.0) \
STEP13:fnl  (v.1.0.0) 

#### *DONE*



**`process_GNSS2FNL.sh` works for AWS EC2 servers (Amazon Linux 2)** (tested 11.05.2021)
**`process_GNSS2FNL.sh` also works for Mac OS X (Intel)** (tested 11.03.2021)
** 
