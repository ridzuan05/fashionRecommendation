###### net record bellow

simple 3FC with softmax loss layer (optional: rank loss training)

the total user number is 1311, by items.jsonl;
the total user number is 1211, by sets.jsonl;
the total user number is 1110, by intersection of items.jsonl & sets.jsonl;

minimum_sets_num = 200, user percent = 0.788, user_num = 875(false, by compact sets)->989(true, by decomposed sets)

posi:neg = 1:1.

train:val:test = 80:1:19.

train input pair: 734224;
val input pair: 9002;
test input pair: 175502;

net structure: cnn_top/bot/sho share the same parameters.

###### training record bellow

1. 选定 train batch size & val batch size：
	64->128->96->80；
	50；

2. 确定solver，training_record.notebook里的各种iter参数：
	9002 / 50 = 180 (test-iter)
	734224 / 80 = 9178, 9178*50 = 458900 (max_iter)
	9178 / 150 = 184 (save .caffemodel [1.1G]), total size: 1.1*300 = 330 G/epoch 
	9178 / 150 = 184 (test_interval & save test accu/loss)
	9178 / 2000 = 5 (display)

3. 开始训练：
	先来2个epoch；
    时间记录：
	3月27日, 3:23 pm., 0 iters (start time); 3月2*日, **:** a/pm., *** iters (inter time)
	speed: *h*m + *h*m = *h*m = *m, */***= 0.**** min/iter



