import os

item_folders = [f for f in os.listdir('/local2/home/tong/fashionRecommendation/data/Polyvore_large/supplement/images')] 

for i in range(0,len(item_folders)):
    source = '/local2/home/tong/fashionRecommendation/data/Polyvore_large/supplement/images/'+item_folders[i]+'/items/'
    target = '/local2/home/tong/fashionRecommendation/data/Polyvore_large/1120_users/images/'+item_folders[i]+'/'
    os.system('cp -avr '+source+' '+target)