training method: simple 3FC with direct rank loss training

minimum_sets_num = 200, user percent = 0.78, total user_num = 987.

posi:neg = 1:5, posi data has been augmented for 5 times larger.

train:val:test = 80:1:19.

train input pair: 1833825;
val input pair: 22485;
test input pair: 438340.

net structure: cnn_top/bot/sho share the same parameters.

确定solver，training_record.notebook里的各种iter参数;
	22485 / 50 = 450 (test-iter)
	1833825 / 30 = 61128, 61128*50 = 3056400 (max_iter)
	61128 / 150 = 408 (save .caffemodel [1.1G]), total size: 1.1*150 = 165 G/epoch 
	61128 / 150 = 408 (test_interval & save test accu/loss)
	61128 / 2000 = 31 (display)
