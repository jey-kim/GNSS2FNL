#!/bin/bash

##########################
###### MASTER CODE #######
##########################

#step 1: download GNSS data
ipython download_files_v_1_0_1.py<<EOF
no  # yes-allGNSS; no-NOTA
yes  # yes-PBO; no-NOTA
EOF

#step 2
python preprocess_data_v_1_0_2.py


#step 3
python ch_date_unr_v_1_0_2.py


#step 4
python time_vector_generator_v_1_0_1.py<<EOF
no #Not specific end date of the analysis
EOF

#step 5
python remove_data_outside_analysis_period_v_1_0_2.py


#step 6
python correct_steps_v_1_0_1.py


#step 7
python fill_entire_time_v_1_0_0.py


#step 8
python remove_outliers_v_1_0_0.py


#step 9
python plot_time_series_v_1_0_0.py


#step 10
python monthly_avg_v_1_0_1.py


#step 11
python vertical_timeseries_analysis_v_0_0_0.py<<EOF
yes
EOF


#step 12
python diff_v_1_0_0.py


#step 13
python fnl_v_1_0_0.py  
