# GNSS2FNL [From GNSS position timeseries measurements to 4-mo displacement field]

jeonghyeop kim (11/02/2021) 
email : jeonghyeop.kim@gmail.com

RUN THE MASTER CODE!
sh process_GNSS2FNL.sh




*steps* 

STEP01:download_files  (v.1.0.1)

STEP02:preprocess_data  (v.1.0.2) 

STEP03:ch_date_unr  (v.1.0.2)

STEP04:time_vector_generator  (v.1.0.1)

STEP05:remove_data_outside_analysis_period  (v.1.0.2)

STEP06:correct_steps  (v.1.0.1)
    
STEP07:fill_entire_time  (v.1.0.0)

STEP08:remove_outliers  (v.1.0.0)

STEP09:plot_time_series  (v.1.0.0)

STEP10:monthly_avg  (v.1.0.1)

STEP11:vertical_timeseries_analysis  (v 0.0.0) 
    -> Use the previous analysis for now (vertical_analysis_PBO.out)
    -> Update later (10/28/2021) 

STEP12:diff  (v.1.0.0)

STEP13:fnl  (v.1.0.0)

*DONE*
