
l_root = "/local2/home/tong/fashionRecommendation/models/fashionNet_2/data_prep/"

data_type = ['train_', 'val_', 'test_']
item_type = ['_top.txt', '_bot.txt', '_sho.txt']

g_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/data_prep/general_list/'
for_length = open(g_root+'tuples_test_posi.txt').readlines()
user_num = 1+int(for_length[-1].strip('\r\n').split(' ')[0])

for u in range(0,user_num):
	for i in range(0,len(data_type)):
		for k in range(0,len(item_type)):
			imgData_source = open(l_root+"lmdb_list/"+data_type[i]+str(u)+item_type[k])
			imgData_target = open(l_root+"imgdata_list/"+data_type[i]+str(u)+item_type[k],'w')

			for line in imgData_source:
				line_temp = line.split('/')
				new_line = "/local/tong/fashionRecommendation/data/images/"+line_temp[9]+"/"+line_temp[12]
				imgData_target.write(new_line)

			imgData_source.close()
			imgData_target.close()
