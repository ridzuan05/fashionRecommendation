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

1. 准备再来3个epoch，先查看前3个epoch的结果：
	"i" is finished at 18355, the next "i" to start should be 18356;
	发生了overfitting，调整lr(0.0001, 0.001)->lr(0.00001,0.0001)，从val loss最低处 (t2.1(finished i = 7727)) 开始训练，先来3个epoch [commit on local (done); pull on local (done); commit on local (done); pull on ares (ing...); start t2.2(0)]；
    时间记录：
	3月28日, 8:35 pm., 0 iters (start time); 3月2*日, **:** a/pm., *** iters (inter time)
	speed: *h*m + *m = *m, */*= 0.0*** min/iter;

2. prepare for t2.2(0)：
	a) 找到 val loss的最低点（loss=0.653,i=7727）；
	b) 删除 train／test中的部分纪录 (done)；
	c) 准备好training_record.ipython notebook(done)；
	d)  mv train/test/png to t1/ folder (done);
	e) mv 1/7728.caffemodel to t1/s_.caffemodel (done);
	f) start t2.2(0) (...ing);

==========================================================================================

1. 选定 train batch size & val batch size：
	64->128->96->80；
	50；

2. 确定solver，training_record.notebook里的各种iter参数：
	9002 / 50 = 180 (test-iter)
	734224 / 80 = 9178, 9178*50 = 458900 (max_iter)
	9178 / 150 = 184 (save .caffemodel [1.1G]), total size: 1.1*300 = 330 G/2 epoch 
	9178 / 150 = 184 (test_interval & save test accu/loss)
	9178 / 2000 = 5 (display)

3. 开始训练：
	先来2个epoch；
    时间记录：
	3月27日, 3:28 pm., 0 iters (start time); 3月28日, 12:20 am., 13984 iters (inter time)
	speed: 8h32m + 20m = 8h52m = 532m, 532/13984= 0.0380 min/iter


