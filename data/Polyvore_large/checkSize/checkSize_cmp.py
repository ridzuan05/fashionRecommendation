#!/usr/bin/env python

checkSize = open('./checkSize.txt').readlines()
checkSize_dell = open('./checkSize_dell.txt').readlines()

checkSize_cmp_fp = open('./checkSize_cmp.txt','w')
checkSize_cmp_fp.close()

for u_dell in range(0,len(checkSize_dell)):
	for u in range(0,len(checkSize)):

		checkSize_dell_list = checkSize_dell[u_dell].strip('\r\n').split(' ')
		checkSize_list = checkSize[u].strip('\r\n').split(' ')

		# if userName match
		if (checkSize_dell_list[0] == checkSize_list[0]):
			# if userContents don't match
			if (checkSize_dell_list != checkSize_list):

                                checkSize_cmp_fp = open('./checkSize_cmp.txt','a')

				userName = checkSize_dell_list[0]
				items = str(int(checkSize_dell_list[1])-int(checkSize_list[1]))
				itemsNum = str(int(checkSize_dell_list[2])-int(checkSize_list[2]))
				items_append = str(int(checkSize_dell_list[3])-int(checkSize_list[3]))
				items_appendNum = str(int(checkSize_dell_list[4])-int(checkSize_list[4]))
				sets = str(int(checkSize_dell_list[5])-int(checkSize_list[5]))
				setsNum = str(int(checkSize_dell_list[6])-int(checkSize_list[6]))
	
				checkSize_cmp_fp.write(userName+' '+items+' '+itemsNum+' '+items_append+' '+items_appendNum+' '+sets+' '+setsNum+'\r\n')

                                checkSize_cmp_fp.close()

			break
