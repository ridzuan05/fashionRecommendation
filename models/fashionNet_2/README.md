######################################################################## net record bellow

simple 3FC with softmax loss layer (optional: rank loss training)

the total user number is 1311, by items.jsonl;
the total user number is 1211, by sets.jsonl;
the total user number is 1110, by intersection of items.jsonl & sets.jsonl;

minimum_sets_num = 200, user percent = 0.788, user_num = 875(false, by compact sets)->989(true, by decomposed sets, which means more users' set_num can be >= min_sets_num, thus more users here)

posi:neg = 1:1.

train:val:test = 80:1:19.

train input pair: 734224;
val input pair: 9002;
test input pair: 175502;

train batch_size: 80 (softmax);
test batch_size: 50;

net structure: cnn_top/bot/sho share the same parameters.

######################################################################## training record bellow

0. 改变user_2需要改变的一些参数：
	Done;
	[user_2]
	training size: 1674
	val size: 21
	testing size: 398
  ｛
	max_iter：1674 / 80 = 21, 21*50+1 = 1051 (max_iter)
	
	test_iter：21 / 21 = 1 (test-iter)
	test_interval：21 / 4 = 5 (test_interval & save test accu/loss & save .caffemodel [1.1G]), total size: 1.1*60 = 66 G/15 epoch
	visual_interval：21 / 21 = 1 (display)
	｝
	1) train_val.prototxt中的data_source_path, train&test_batch_size;
	2) training_record中的recordDir, test_iter, test_interval, visual_interval, training_epochs;
	3) solver.prototxt中的lr, max_iter;
	4) mkdir for t2.2.2;

1. fine tuning on user_2, using 15 epochs、thresh_fp=0.999、lr=0.001 & 1.2-2):
	总是觉得有点怪，ndcg在下降，估计是因为这部分数据比较多，处于正态分布的高端部分;
	但是在 user_0/1 上ndcg是存在上升趋势的，因此每个 user 会有不同；

2. fine tuning on user_2, using 15 epochs、thresh_fp=0.9、lr=0.001 & 1.2-2):
	0.9造成的波动太大了，还是0.999能够比较稳定地剔除 false-positive;

3.改变user_3涉及的一些参数：
	Done;
	[user_3]
	training size: 1570
	val size: 20
	testing size: 374
  ｛
	max_iter：1570 / 80 = 20, 20*50+1 = 1001 (max_iter)
	
	test_iter：20 / 20 = 1 (test-iter)
	test_interval：20 / 4 = 5 (test_interval & save test accu/loss & save .caffemodel [1.1G]), total size: 1.1*60 = 66 G/15 epoch
	visual_interval：20 / 20 = 1 (display)
	｝
	1) train_val.prototxt中的data_source_path, train&test_batch_size;
	2) training_record中的recordDir, test_iter, test_interval, visual_interval, training_epochs;
	3) solver.prototxt中的lr, max_iter;
	4) mkdir for t2.2.3;

4.fine tuning on user_3, using 15 epochs、thresh_fp=0.999、lr=0.001 & 1.2-2):
	ndcg数值的确在提高，我打算加快lr，使他学习的更快;

5.fine tuning on user_3, using 15 epochs、thresh_fp=0.999、lr=0.01 & 1.2-2):
	这个lr太大了，会造成波动，建议0.002尝试一下;

6.fine tuning on user_3, using 15 epochs、thresh_fp=0.999、lr=0.002 & 1.2-2):
	softmax accu在下降，很奇怪，我怀疑是val data的问题，打算用test data看一下训练的效果;

6.1.把6的val data换成test data, 并重新进行fine tuning:
	...ing;
	1) prototxt里面val2test&test_batch_size;
	2) training_record的test_interval&test_iter;
	3) update README.md;

==========================================================================================

1.1.检查目前 t2.1(next i=137706)[7-0.0001*(1,100)->8-0.0001*(1,10)] to check stop result 在rank_net上的accuracy & loss数值，与最后一次在10th epoch时测的 rank_accu/loss 的变化，决定是否需要继续 user-general training？
	可以终止了；
	从ndcg的变化看，false positive的影响增大了，越来越容易排名靠前，甚至超过right positive，有点overfitting了;

1.2.选中2个候选caffemodel，作为user_specific训练的初始化参数：
	发现mean_ndcg数值大的caffemodel所对应的rank_accu/test都基本数值较好；
	1) [90000,110000]～H_mean_ndcg@(0.735,103960), C_ndcg_10@(0.937) [备选参数]
	caffemodel_idx: 103960
	test_accu: 0.641111113959, test_loss: 0.641836200158

	2) [110000,137706～H_mean_ndcg@(0.735,124200), C_ndcg_10@(1.000) [优先考虑]
	caffemodel_idx: 124200
	test_accu: 0.644000006384, test_loss: 0.642684461673

1.3.需要清空的txt&需要重新绘制的png：
	Done;
	 时间记录：
	1m33s/test (剩余估计时间：4h)
	test_rank_accu.txt
	test_rank_loss.txt
	conf_l_matrix.txt
	conf_r_matrix.txt
	t2.1_rank/dd_dislike.txt
	t2.1_rank/dl_dislike.txt
	t2.1_rank/d_dislike.txt
	t2.1_rank/ld_like.txt
	t2.1_rank/ll_like.txt
	t2.1_rank/l_like.txt
	t2.1_rank/ndcg.txt
###
	rank_record.png
	cMat.png
	t2.1_rank/dd_record.png
	t2.1_rank/dl_record.png
	t2.1_rank/d_record.png
	t2.1_rank/ld_record.png
	t2.1_rank/ll_record.png
	t2.1_rank/l_record.png
	t2.1_rank/ndcg.png

1.4.准备fashionNet_2的top-10 user 数据，分别对每个user数据进行训练：
	Done;

1.5.1.修改train_val.prototxt准备对user_0进行fine_tuning;
	...在local上先进行更改，然后把ares与local进行以下sync;
	1）锁定cnn的参数不改变；
	2）调整fc层的lr，从0.0001开始改变；
	3）将2.1收入folder中，准备开始t2.2
	3）先上它5个epoch: t2.2.0(next i=0)[10_0.01*(0,1)]；
	[110000,137706～H_mean_ndcg@(0.735,124200), C_ndcg_10@(1.000) [优先考虑]
	caffemodel_idx: 124200
	test_accu: 0.644000006384, test_loss: 0.642684461673
	时间记录：
	4月11日, 3:19 pm., 26 iters (start time); 4月11日, 3:25 pm., 110 iters (inter time)
	speed: 6m, 6/84= 0.0714 min/iter (总时间估计：～30mins)
	4) 将t2.2.0中的相关files进行git add；

1.5.2.对user_1进行fine_tuning;
	...大致确定为15epoch、thresh_fp=0.99、lr=0.001;
	1) 先来15个epoch；
	t2.2.1(next i=0)[15_0.001*(0,1)], thresh_fp=0.9
	2) git add t2.2.1中的files；

1.6. 给所有的training_record的cMat加上recordDir;
	Done;

1.7.must get rid of false-positive using a threshold_fp = 0.999 for all training_record:
	Done;
	[user_1]
	training size: 1770
	val size: 22
	testing size: 422
  ｛
	max_iter：1770 / 80 = 22, 22*10+1 = 221 (max_iter)
	
	test_iter：22 / 22 = 1 (test-iter)
	test_interval：22 / 4 = 5 (test_interval & save test accu/loss & save .caffemodel [1.1G]), total size: 1.1*40 = 44 G/10 epoch
	visual_interval：22 / 22 = 1 (display)
	｝
	1）train_val.prototxt中的data_source_path, train&test_batch_size;
	2) training_record中的recordDir, test_iter, test_interval, visual_interval, training_epochs;
	3) solver.prototxt中的lr, max_iter;
	4) mkdir for t2.2.1;

1.8.改变训练的iter参数，适应于user_specific数据集的大小:
	Done;
	[user_0]
	training size: 1910
	val size: 24
	testing size: 454
  ｛
	max_iter：1910 / 80 = 24, 24*50+1 = 1201 (max_iter)
	
	test_iter：24 / 24 = 1 (test-iter)
	test_interval：24 / 10 = 2 (test_interval & save test accu/loss & save .caffemodel [1.1G]), total size: 1.1*500 = 550 G/50 epoch
	visual_interval：24 / 10 = 2 (display)
	｝

1.9.改变prototxt中的部分参数：
	Done;
	1) test_batch_size = 24;

2.1.分析dd,dl,d,ld,ll,l这5张图的曲线，从而判断training的阶段：
	training 基本收敛了，并略微产生了overfitting；
	3vs2的failure case的数量越来越多，造成rank accu降低；

2.2.检查rank_accu & loss, 与之前的数值对比：
	开始产生overfitting了，数值开始恶化，因此我决定停止user_general训练;
    时间记录：
	1m33s/test (剩余估计时间：70 mins)

2.3.解决figure打开太多造成的内存占用问题：
	Done;

3.根据1&2的分析结果，决定继续training，还是准备user specific fine微调？
	 进行user_specific微调；

==========================================================================================

1.打出softmax net 的confusion matrix,分析val_loss的问题出在哪里：
	val_loss's gradually increase is because of dislike-like's increase;
	a) HVA@(0.601,36984), LVL@(0.770,32200); [30000,40000]
		[[2463, 2037],
         [1549, 2951]] ～ 0.602
	b) HVA@(0.606,58144), LVL@(0.783,44160); [40000,60000]
		[[2237, 2263],
         [1278, 3222]] ～ 0.607
	c) HVA@(0.612,66240), LVL@(0.815,66240); [60000,80000]
		[[2360, 2140],
         [1350, 3150]] ～ 0.612
	d) HVA@(0.610,91448), LVL@(0.844,87216); [80000,91780]
		[[2217, 2283],
         [1223, 3277]] ～ 0.610

2.修改所有的training_record代码自动储存每次validation的confusion matix到txt中：
	Done;

3.从大概40000次、中间次、中间次、90000次分别取caffemodel，放入rank_loss中测试validation accuracy：
	can be explained by 6.2's figures;
	22485 / 50 = 450 (test iters)
	a) HVA@(0.601,36984), LVL@(0.770,32200); [30000,40000]
		VA@0.629955559307、VL@0.649533153243，
		cMat_l: [[    0     0]，[ 7749 14751]]
		cMat_r:[[12191 10309]，[    0     0]]

	b) HVA@(0.606,58144), LVL@(0.783,44160); [40000,60000]
		VA@0.63133333789、VL@0.64657627066
		cMat_l: [[    0     0]，[ 6396 16104]]
		cMat_r:[[10887 11613]，[    0     0]]

	c) HVA@(0.612,66240), LVL@(0.815,66240); [60000,80000]
		VA@0.63662222498、VL@0.644074650606
		cMat_l:[[    0     0]，[ 6754 15746]]
		cMat_r:[[11436 11064]，[    0     0]]

	d) HVA@(0.610,91448), LVL@(0.844,87216); [80000,91780]
		VA@0.640622226066、VL@0.642674128479
		cMat_l:[[    0     0]，[ 6122 16378]]
		cMat_r:[[10720 11780]，[    0     0]]

4.利用softmax的参数打印rank_accu/loss的曲线：
	Done;
    时间记录：
	4月3日, 12:17 pm., 30912 just starts models (inter time); 4月3日, 12:34 pm., 31280 just done models (inter time)
	speed: 17m, 17/3= 5.667 min/caffemodel = 0.0126 min/iter (剩余时间估计：～ 32h, 3 times as fast as Training Speed)

5.图示化rank_net的conf_matrix的变化过程：
	Done;

6.1.将conf_matrix图示化的代码写入所有的train_record中来：
	Done;

6.2.还需要给所有的training_record增加6张图：
	Done;
	dislike[correct](dislike,like), dislike[wrong](dislike,like), dislike[average](dislike,like)
	like[wrong](dislike,like), like[correct](dislike,like), like[average](dislike,like)

6.3. Data -> ImageData:
	Done;

7.1.利用NDCG指标进行测试：
    must integrate general meanNDCG into my testing code for all training_record;

7.2. before going too deep into customizing a layer, I should first see mean NDCG for all users as a whole:
	promising result;
	a) HVA@(0.601,36984), LVL@(0.770,32200); [30000,40000]
	mean_ndcg: 0.73381
	ndcg_at: 10个1
	b) HVA@(0.606,58144), LVL@(0.783,44160); [40000,60000]
	mean_ndcg: 0.73450
	ndcg_at: 10个1
	c) HVA@(0.612,66240), LVL@(0.815,66240); [60000,80000]
	mean_ndcg: 0.73809
	ndcg_at: 10个1
	d) HVA@(0.610,91448), LVL@(0.844,87216); [80000,91780]
	mean_ndcg: 0.73760
	ndcg_at: 10个1

8.根据1的结果，选择合适的caffemodel，调整lr，进入第三阶段training：
	[mv repeated files into ./t2.1_rank/, for backup]:
	dd_dislike.txt [cp]
	dl_dislike.txt [cp]
	d_dislike.txt [cp]
	ld_like.txt [cp]
	ll_like.txt [cp]
	l_like.txt [cp]
	cMat.png [cp]
	dd_record.png [cp]
	dl_record.png [cp]
	d_record.png [cp]
	ld_record.png [cp]
	ll_record.png [cp]
	l_record.png [cp]
	[resume training on fashionNet_2 still with 0.0001*(1,10) for 5 more epochs]:
	Done：
	4月5日, 4:44 pm., 91816 iters done(start time); 4月5日, 8:17 pm., 97250 iters done (inter/stop time)
	speed: 16m + 3h17m = 3h*33m = 213m, 213/5434= 0.0392 min/iter
==========================================================================================

1.保持第一阶段 lr_rate，再来1个epoch training, 以确认test_accu/loss是否真正收敛了：
	时间记录：
	3月31日, 11:15 am., 55068 iters (start time); 3月31日, 05:40 pm., 64246 iters (inter/stop time)
	speed: 45m + 5h40m = 5h85m = 385m, 385/9178= 0.0419 min/iter
	开始进入下一lr_rate训练阶段。

2.调整lr_rate，进入下一训练阶段：
	0.0001*(1,100)->#0.0001*(1,10)#->0.0001*(1,1)->0.00001*(1,1)
	时间记录：
	3月31日, 06:51 pm., 64246 iters (start time); 4月1日, 12:50 am., 73510 iters (inter time)；4月1日, 10:59 am., 89230 iters (inter time)；
	speed: 5h9m + 50m = 5h59m = 359m, 359/9264= 0.0388 min/iter
	speed:10h9m = 609m, 609/15720 = 0.0387 min/iter

==========================================================================================

1.test accu还在提高，train数据还未收敛，保持第一阶段 lr_rate，再来3个epoch training：
	时间记录（截止时间错过了）：
	3月30日, 02:54 pm., 27534 iters (start time); *月*日, **:** am., 55068 iters (stop time)
	speed: *h*m + *h*m = *h*m = *m, */*= 0.03** min/iter

2.把所有 train_val.prototxt 的输入数据格式都改为 lmdb->jpg:
	Done;
	*******fashionNet_k to _3 for mean imgs
	*******_lmdb to .txt
	*******lmdb_data to imgdata_list
	*******train batch size to 30 or 80
	*******test batch size to 50

3.下载 fashionData 到胡杨老师的台式机上：
	...ing;

==========================================================================================

1.验证test.forward的batch数量：
	和prototxt一样；
2.测试test_forward整体循环的速度：
	都差不多是1min45s；
3.验证train所记录的数据：
	记录的batch loss／accu数据，打算同时纪录一下avg数据；
4. 更改所有的training_record/ipython.notbook的代码：
	done;
	******add two CHANGES!!!
	******comment codes
	******cp def()
	******blobs name * 2
	******cp all codes
	******recordDir _K
	******blobs name * 4
	******save caffemodel _k_
	******delete codes
5. 研究一下python写入‘\r\n’的问题：
	回车就是\r\n,注意下一行不要出现空格或者tab；
6.先对 t2.1(next i=0) 来3个epoch:
	先来3个epoch；
    时间记录：
	3月29日, 6:32 pm., 0 iters (start time); 3月30日, 09:33 am., 27534 iters (stop time)
	speed: 5h28m + 9h33m = 15h1m = 901m, 901/27534= 0.0327 min/iter


==========================================================================================

1. 准备再来3个epoch，先查看前3个epoch的结果：
	"i" is finished at 18355, the next "i" to start should be 18356;
	发生了overfitting，调整lr(0.0001, 0.001)->lr(0.00001,0.0001)，从val loss最低处 (t2.1(finished i = 7727)) 开始训练，先来3个epoch [commit on local (done); pull on local (done); commit on local (done); pull on ares (ing...); start t2.2(0)]；

2. prepare for t2.2(0)：
	a) 找到 val loss的最低点（loss=0.653,i=7727）；
	b) 删除 train／test中的部分纪录 (done)；
	c) 准备好training_record.ipython notebook(done)；
	d)  mv train/test/png to t1/ folder (done);
	e) mv 1/7728.caffemodel to t1/s_.caffemodel (done);
	f) start t2.2(0) (done);

==========================================================================================

1. 选定 train batch size & val batch size：
	64->128->96->80；
	50；

2. 确定solver，training_record.notebook里的各种iter参数：
	9002 / 50 = 180 (test-iter)
	734224 / 80 = 9178, 9178*50 = 458900 (max_iter)
	9178 / 50 = 184 (save .caffemodel [1.1G]), total size: 1.1*300 = 330 G/6 epoch 
	9178 / 50 = 184 (test_interval & save test accu/loss)
	9178 / 2000 = 5 (display)

3. 开始训练：
	先来2个epoch；
    时间记录：
	3月27日, 3:28 pm., 0 iters (start time); 3月28日, 12:20 am., 13984 iters (inter time)；
	speed: 8h32m + 20m = 8h52m = 532m, 532/13984= 0.0380 min/iter


