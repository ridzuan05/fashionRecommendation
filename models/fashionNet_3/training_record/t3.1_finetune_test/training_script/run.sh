#!/bin/bash

for u in $( seq 0 799 )
do 
	/local2/home/tong/fashionRecommendation/models/fashionNet_3/training_record/t3.1_finetune_test/training_script/control_k/control_${u}.py 2>&1 | tee -a run.log
done

for u in $( seq 0 2 )
do 
	/local2/home/tong/fashionRecommendation/models/fashionNet_3/training_record/t3.1_finetune_test/training_script/control_k/control_${u}.py 2>&1 | tee -a run2.log
done

for u in $( seq 669 799 )
do 
	/local2/home/tong/fashionRecommendation/models/fashionNet_3/training_record/t3.1_finetune_test/training_script/control_k/control_${u}.py 2>&1 | tee -a run2.log
done