#!/bin/bash



mkdir $(date +"%m%d%Y")
cd $(date +"%m%d%Y")
cp ../data/processing/fnl_**.dat .
cp ../data/processing/*.pdf .
cp ../displacement_time_label.dat .
cp ../vertical_analysis.out .
cp ../station_list_full.dat .
cp ../coordinate_list_full.dat .


cd ../
rm -r data
pwd
