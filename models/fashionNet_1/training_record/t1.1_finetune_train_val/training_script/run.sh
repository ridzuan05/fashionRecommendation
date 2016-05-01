#!/bin/bash

for u in $( seq 0 799 )
do 
	/local2/home/tong/fashionRecommendation/models/fashionNet_1/training_record/t1.1_finetune_train_val/training_script/control_k/control_${u}.py 2>&1 | tee -a run.log
done