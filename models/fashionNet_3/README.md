###### net record bellow

training method: simple 3FC with direct rank loss training

minimum_sets_num = 200, user percent = 0.78, total user_num = 987.

posi:neg = 1:5, posi data has been augmented for 5 times larger.

train:val:test = 80:1:19.

train input pair: 1833825;
val input pair: 22485;
test input pair: 438340.

net structure: cnn_top/bot/sho share the same parameters.

###### training record bellow

1. t3.2 [lr is (0.00001,0.0001)] does not converge on training dataset even:
	perhaps direct rank training does not work at all;

2. should try fashionNet_2:
	working on it now;

==========================================================================================

1. training(1) is done, prepare for training(2), need to decrease lr from (0.0001,0.001) to (0.00001,0.0001) because test_acc/loss does not converge though train_acc/test does:
	done;

2. start training for one epoch;
	training now，先来2个epoch;
    时间记录：
	3月26日, 8:23 pm., 0 iters (start time); 3月2*日, 09:30 am., 20801 iters (inter time)
	speed: 3h37m+9h30m=12*60m+67m=787m, 787/20801=0.0378 min/iter

3.1 fix that bug on Siamese training ipython notebook:
	done:	

3.2 prepare txt of ImageData for all the other nets:
	done:

4. learn to write the nips draft with LaTex:
	has been postponed;

==========================================================================================

0. resize all images；
	搞定了；

1. 查到imagedata layer的用法；
		•	Layer type: ImageData
	•	Parameters
	◦	Required
	▪	source: name of a text file, with each line giving an image filename and label
	▪	batch_size: number of images to batch together
	◦	Optional
	▪	rand_skip
	▪	shuffle [default false]
	▪	new_height, new_width: if provided, resize all images to this siz

2. 看一下lmdb运行的内存使用情况；
	已截图；

3. 以fashionNet_3为例，尝试imagedata layer；
	mem 5.1%, v-mem 101G；

4. 如果可以的话全部换成imagedata layer；
	先从fashionNet_3开始，不着急；

5. 从上次断掉的地方继续training；
	正在搞这个，接着上写，先来2个epoch；
    时间记录：
	3月25日, 10:46 pm., 58315 iters (start time); 3月26日, 06:39 pm., 89935 iters (inter time)
	speed: 1h14m + 12h + 6h39m = 19h53m = 19*60+53 = 1193m, 1193/31620=0.0377 min/iter

==========================================================================================

1.  高清楚training dataset & val set的大小；
	1833825， 22485
2. 选定 train batch size & val batch size；
	32->16->24->28->30->31->32->31->30
	50->80->65->58->54->52->51->50
3. 确定solver，training_record.notebook里的各种iter参数;
	22485 / 50 = 450 (test-iter)
	1833825 / 30 = 61128, 61128*50 = 3056400 (max_iter)
	61128 / 150 = 408 (save .caffemodel [1.1G]), total size: 1.1*150 = 165 G/epoch 
	61128 / 150 = 408 (test_interval & save test accu/loss)
	61128 / 2000 = 31 (display)
3.1 确认是否可以遍历整个val set进行测试？
	Yes.
4. 开始训练;
    先来 1 epoches;
    时间记录：
	3月21日, 11:22 pm., 5712 iters (start time); 3月22日, 7:54 am., 19096 iters (inter time)
	speed: 38m+7h54m=7*60+38+54=420+92=512m, 512/13384=0.0383 min/iter

