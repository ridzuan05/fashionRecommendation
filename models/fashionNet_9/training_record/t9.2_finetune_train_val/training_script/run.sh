#!/bin/bash

for u in $( seq 324 799 )
do 
	/home/dell/fashionRecommendation/models/fashionNet_9/training_record/t9.2_finetune_train_val/training_script/control_k/control_${u}.py 2>&1 | tee -a run.log
done
