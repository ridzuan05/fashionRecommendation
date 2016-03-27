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

1. 选定 train batch size & val batch size；
	32->
	50->

2. determine parameters in training_record/ipython notebook (edit on local->git pull on local->git push on local->git pull on ares):
	not yet;