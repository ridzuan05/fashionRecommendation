#!/bin/bash

for u in $( seq 0 988 )
do 
	/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user/training_script/control_${u}.py 2>&1 | tee -a run.log
done