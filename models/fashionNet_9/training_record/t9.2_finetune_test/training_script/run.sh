#!/bin/bash

for u in $( seq 0 799 )
do 
	/home/dell/fashionRecommendation/models/fashionNet_9/training_record/t9.2_finetune_test/training_script/control_k/control_${u}.py 2>&1 | tee -a run.log
done