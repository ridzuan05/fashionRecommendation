#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 10:51:44 2014

@author: yanghu
"""

import operator
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from matplotlib import rc
rc('mathtext', default='regular')

import os
import json
import operator
import re
import numpy as np
import codecs

SUBSET_START = 0
SUBSET_END = 500
NUM_CAT = 3
URL_BASE = 'http://www.polyvore.com'
#ignore_users = set(['pretty-girl-xo']) 
watch_users = set(['fortheloveofpoly', 'hamaly', 'malenafashion27', 'colierollers', 'cutekawaiiandgoodlooking', 'raelee-xoxo', 'limass', 'nadiasxox'])
FASHION_WORDS = set(["outerwear", "jacket", "blazer", "coat", "sweater", "top",
                     "t-shirt", "shirt", "blouse", "tee", "tank", "pullover", 
                     "hoodie", "sweatshirt", "tunic", "cardigan",
                     "skirt", "jeans", "jean", "pants", "pant", "trousers", "shorts", "dress", "jumpsuit", 
                     "leggings", "legging", "overalls", "overall",
                     "shoe", "bootie", "boot", "clog", "flat", "loafer", 
                     "moccasin", "oxford", "pump", "sandal", 
                     "sneaker", "slipper", "shoes", "booties", "boots", "clogs", "flats", "loafers", 
                     "moccasins", "oxfords", "pumps", "sandals", 
                     "thongs", "sneakers", "slippers"]) 
                     
FASHION_CATEGORIES = set(["Clothing", "Dresses", "Skirts", "Tops", "Outerwear", 
    "Jackets", "Blazers", "Coats", "Jeans", "Pants", "Shorts", "Jumpsuits & Rompers",
    "Sweatshirts & Hoodies", "Intimates", "Swimwear", "Activewear", "Shoes", "Athletic", "Boots", 
    "Clogs", "Flats", "Loafers & Moccasins", "Oxfords", "Pumps", "Sandals", 
    "Sneakers", "Bags", "Backpacks", "Handbags", "Messenger Bags", "Wallets"])
    
NONFASHION_CATEGORIES = set(["Jewelry", "Bracelets & Bangles", "Brooches", 
    "Charms & Pendants", "Earrings", "Necklaces", "Rings", "Watches",
    "Accessories", "Belts", "Eyewear", "Gloves", "Hair Accessories", "Hats",
    "Scarves", "Tech Accessories", "Umbrellas",
    "Beauty", "Beauty Products", "Makeup", "Face Makeup", "Cheek Makeup", 
    "Eye Makeup", "Lip Makeup", "Makeup Tools", "Skincare", "Face Care", 
    "Eye Care", "Lip Care", "Fragrance", "Bath & Body", "Body Cleansers", 
    "Body Moisturizers", "Body Treatments", "Deodorant", "Sun Care", "Haircare",
    "Hair Shampoo", "Hair Conditioner", "Styling Products", "Hair Styling Tools",
    "Nail Care", "Nail Polish", "Nail Treatments", "Manicure Tools", 
    "Gift Sets & Kits", "Beauty Accessories", "Bags & Cases", 
    "Home", "Furniture", "Lighting", "Rugs", "Home Decor", "Kitchen & Dining",
    "Bedding", "Bath", "Outdoors"])

class PSet:
    def __init__(self, create_time, ind):
        self.create_time = create_time
        self.ind = ind
        self.p = re.compile('\d+')
        
    def get_sn(self):
        m = self.p.findall(self.create_time)
        if len(m)>0:
            return int(m[0])
        else:
            time_strs = ['Yesterday', 'One', 'Two', 'Three']
            for i in range(len(time_strs)):
                if self.create_time.find(time_strs[i])>=0:
                    return i
        raise ValueError("Valid create_time")
        
def get_subset(sets_file, start, end):
    key_strs = ['hour', 'day', 'month', 'year']

    sub_sets = list([])
    for i in range(len(key_strs)):
        sub_sets.append([])
    
    with open(sets_file, 'r') as f:
        k = -1
        for line in f:
            set_item = json.loads(line)
            ctime = set_item['create_time']
            k += 1
            for i in range(len(key_strs)):        
                if (ctime.find(key_strs[i])>=0):
                    sub_sets[i].append(PSet(ctime, k))

    flag = np.empty(k+1, dtype=np.bool)
    flag.fill(False)

    start = max(0,start)
    end = min(k+1, end)                
    if start>=end:
        return flag
            
    for i in range(len(sub_sets)):
        sub_sets[i].reverse()
        sub_sets[i].sort(key=operator.methodcaller("get_sn"))
    
    all_sets = list([])
    for i in range(len(sub_sets)):
        all_sets.extend(sub_sets[i])
        
    for i in range(start, end):
        flag[all_sets[i].ind] = True
        
    return flag        

#organize all imaegs of all users
def get_all_items():
    
    item_folder = '/local2/home/tong/fashionRecommendation/data/Polyvore_large/polyvore_item/data'; #for source path of all items (users)
    item_files = [os.path.join(item_folder, f) for f in os.listdir(item_folder) if f.endswith('.jsonl')] #for individual paths of all items (users)
  
    failed_images = list([]) #record images url that have not been downloaded by user id
    fashion_items = dict([]) #to record (image url(key), image name), not related to specific user
    unique_images = dict([]) #record this (image name(key), other information) into unique_images, not related to specific user

    user_number = len(item_files)
    print ("\n\nThere user number is: {}\n\n".format(user_number))

    n_all_items= np.zeros(len(item_files)) #num of all items (users)
    n_fashion_items = np.zeros(len(item_files)) #num of all fashion items (users), should be smaller than n_all_items (user dependent)

    for i in range(len(item_files)): #for each item (user)
        print 'for all user_items: ' + str(i+1) + ' / ' + str(len(item_files))
        failed_images.append([]) #initiate space for new user to record images url that have not been downloaded wrt this user
        file_name_s = item_files[i].split('/')[-1].split('_') # [user name, [items.jsonl] or [items, append.jsonl]]
        user_name = file_name_s[0] #user name
        if (file_name_s[-1] == "items.jsonl"): #items.jsonl
            img_folder = '/local2/home/tong/fashionRecommendation/data/Polyvore_large/1120_users/images/'+user_name+'/items/full'        
            #img_folder = "C:\\Users\\yanghu\\Documents\\Finder\\Fashion\\Dataset\\Polyvore\\%s\\items\\full" % user_name #a folder name by user name
        else: #append.jsonl,for the earliest 203 users
            img_folder = '/local2/home/tong/fashionRecommendation/data/Polyvore_large/1120_users/images/'+user_name+'/items_append/full'
            #img_folder = "C:\\Users\\yanghu\\Documents\\Finder\\Fashion\\Dataset\\Polyvore\\%s\\items_append\\full" % user_name #a folder name by user name  
        #if user_name not in ignore_users:
        imgs_downloaded = [f for f in os.listdir(img_folder) if f.endswith('.jpg')] #list of images downloaded wrt user name
        #if user_name in watch_users: #should be commented, thus for all users 
        with open(item_files[i], 'r') as f: #open the '.jsonl' file for this user
            for line in f: #for each item stored in '.jsonl' file
                n_all_items[i] += 1 #counts items number related to this user
                #print n_all_items[i]
                item = json.loads(line) #load this item from '.jsonl' file
                if item['isfashion']: #if this item is fashion image
                    n_fashion_items[i] += 1 #counts fashion images number related to this user
                    if len(item['images'])==0 : #if this image has not been downloaded
                        failed_images[i].append((item['url'],1)) #record images url that have not been downloaded by user_i
                    else: #this image is successfully downloaded
                        img_name = item['images'][0]['path'].split('/')[1] #get image name of this image
                        if img_name in imgs_downloaded: #this image has been found in downloaded images file wrt this user
                            if item['url'] not in fashion_items: #record this (image url(key), image name) into fashion_items, not related to specific user
                                fashion_items[item['url']] = img_name
                            if img_name not in unique_images: #record this (image name(key), other information) into unique_images, not related to specific user                             
                                unique_images[img_name] = {
                                    'categories': item['categories'], 
                                    'path': os.path.join(img_folder,img_name), 
                                    'count': 1, 
                                    'name': item['name'],
                                    'price': item['price'],
                                    'description': item['description']}
                            else:
                                unique_images[img_name]['count'] += 1 #count number of this images shared by all users
                        else:
                            failed_images[i].append((item['url'],2)) #record images url that have been downloaded by user_i, but not in deed
                            
#unique_images[img_name] = {
#    'categories': item['categories'], 
#    'path': os.path.join(img_folder,img_name), 
#    'count': 1, 
#    'name': item['name'],
#    'price': item['price'],
#    'description': item['description']}      
    return (fashion_items, unique_images, failed_images, n_all_items, n_fashion_items, user_number)    

#return 0, 1, 2 to indicate image category
def get_item_category(ctgy):
    cat_tags = list([])
    cat_tags.append(set(["Tops", "Outerwear", "Jackets", "Blazers", "Coats", "Sweatshirts & Hoodies"]))
    cat_tags.append(set(["Skirts", "Jeans", "Pants", "Shorts", "Dresses", "Jumpsuits"]))
    cat_tags.append(set(["Shoes", "Athletic", "Boots", "Clogs", "Flats", "Loafers & Moccasins", "Oxfords", "Pumps", "Sandals", "Sneakers"]))
    
    for tag in ctgy:
        for i in range(NUM_CAT): #i = 0, 1, 2
            if tag in cat_tags[i]:
                return i
                
    return -1
    
def get_item_category_byname(item_name):
    
    cat_tags = list([])
    cat_tags.append(set(["top", "outerwear", "jacket", "blazer", 
                     "coat", "sweater", "t-shirt", "shirt", "blouse", 
                     "tee", "tank", "pullover", "hoodie", "sweatshirt",
                     "tunic", "cardigan"]))
    cat_tags.append(set(["skirt", "jeans", "jean", "pants", "pant", "trousers", "shorts", "dress", "jumpsuit", 
                     "leggings", "legging", "overalls", "overall"]))
    cat_tags.append(set(["shoe", "bootie", "boot", "clog", "flat", "loafer", 
                     "moccasin", "oxford", "pump", "sandal", 
                     "thong", "sneaker", "slipper", "shoes", "booties", "boots", "clogs", "flats", "loafers", 
                     "moccasins", "oxfords", "pumps", "sandals", 
                     "thongs", "sneakers", "slippers"]))

    words = item_name.split(' ')    
#    words_set = set([w.lower() for w in words])
#    
#    for i in range(len(cat_tags)):
#        for tag in cat_tags[i]:
#            if tag in words_set:
#                return i
    
    for i in range(len(cat_tags)):
        if (words[-1].lower() in cat_tags[i]):
            return i
                
    return -1
           
#judge if this set wrt this user is valid or not
def is_set_valid(items_in_set):
    if (len(items_in_set[0])>=1) and (len(items_in_set[1])==1) and (len(items_in_set[2])==1): #one set at most has one bot category and one sho category
        return True
    else:
        return False
    
def get_valid_sets(fashion_items, unique_images, user_number):
    
    sets_file_folder = '/local2/home/tong/fashionRecommendation/data/Polyvore_large/polyvore_set/data'; #for source path of all sets wrt users
    sets_files = [os.path.join(sets_file_folder, f) for f in os.listdir(sets_file_folder) if f.endswith('.jsonl')] #for individual paths of all sets wrt users
 
    item_folder = '/local2/home/tong/fashionRecommendation/data/Polyvore_large/polyvore_item/data'; #for source path of all items wrt users
    item_files = set([f for f in os.listdir(item_folder) if f.endswith('.jsonl')]) #for individual paths of all items wrt users

    all_sets = list([]) #store all information about sets, organized by user name
    n_valid_sets = list([]) #store num of valid sets, organized by user name (aligned with all_sets)
    n_invalid_sets = list([]) #store num of invalid sets, organized by user name (aligned with all_sets)

    print("\n\nThe user number should be same, {} = {}\n\n".format(user_number, len(sets_files)))

    for i in range(len(sets_files)): #for each set wrt users
    #for i in range(1,2):
        print 'for all user sets: ' + str(i+1) + ' / ' + str(len(sets_files))
        #flag = get_subset(sets_files[i], SUBSET_START, SUBSET_END)
        user_name = sets_files[i].split('/')[-1].split('_')[0] #get user name of this set
        img_folder = '/local2/home/tong/fashionRecommendation/data/Polyvore_large/1120_users/images/'+user_name+'/sets/full'
        #img_folder = "C:\\Users\\yanghu\\Documents\\Finder\\Fashion\\Dataset\\Polyvore\\%s\\sets\\full" % user_name #a folder name by user name

#        if (user_name not in ignore_users) and (user_name+'_items.jsonl' in item_files):
#        if (user_name in watch_users) and (user_name+'_items.jsonl' in item_files): #should be commented, thus we don't confine users to watch_users       
        if (user_name+'_items.jsonl' in item_files): #should be uncommented, thus we deal with all users
            with open(sets_files[i], 'r') as f: #for each '.jsonl' of sets wrt users
                #k = -1
                valid_sets = list([]) #store all sets' url,  top/bot/sho image names, and path of each valid set, just related to this users    
                invalid_sets = list([]) #to record invalid sets url, related to just this users
                for line in f: #for each set stored in this '.jsonl'
                    set_item = json.loads(line) #load each set stored in this '.jsonl'
                    #k +=1
                    #if flag[k]:
                    #if 1>0:
                    items = list([]) #a list to sotre image namges according to top (0), bot (1), sho (2)
                    for j in range(NUM_CAT): #j = 0, 1, 2
                        items.append([]) #initialization
                    for url in set_item['item_urls']: #for each image url in this set
                        full_url = URL_BASE+url.lstrip('.') #get full url of this image
                        if full_url in fashion_items: #is this image url exist in image item urls
                            t = get_item_category(unique_images[fashion_items[full_url]]['categories']) #return 0, 1, 2 to indicate image category
                            if t>=0: #if we can get image category by image category                            
                                items[t].append(fashion_items[full_url]) #a list to sotre image namges according to top (0), bot (1), sho (2)
                            else: #if we can't get image category by image name
                                t = get_item_category_byname(
                                    unique_images[fashion_items[full_url]]['name']) #try to get image category by image name, return 0, 1, 2
                                if t>=0:                            
                                    items[t].append(fashion_items[full_url]) #a list to sotre image namges according to top (0), bot (1), sho (2)
                                        
                    if is_set_valid(items): #if this set wrt user is valid
                        if (len(set_item['images'])>0):
                            img_path = os.path.join(img_folder,set_item['images'][0]['path'].split('/')[1])
                        else:
                            img_path = ''
                        valid_sets.append({'url':set_item['url'], 'items':items, 'img_path':img_path}) #store all sets' url,  top/bot/sho image names, and path of each valid set, just related to this users        
                    else: #if this set wrt user is invalid
                        invalid_sets.append(set_item['url']) #to record invalid sets url, related to just this users
                #all_sets
                #[
                #   user_name;
                #   valid_sets
                #   [
                #     set_url;
                #     items
                #     {
                #       top_image_name;
                #       top_image_name; (can be multiple top items here, will be split later)
                #       bot_image_name;
                #       sho_image_name:
                #     }
                #     set_image_path;
                #   ]
                #   invalid_sets
                #   [
                #      set_url; 
                #   ]
                #]
                all_sets.append({'user':user_name, 'valid_sets':valid_sets, 'invalid_sets':invalid_sets}) #store all information about sets, organized by user name              
                n_valid_sets.append(len(valid_sets)) #store num of valid sets, organized by user name (aligned with all_sets)
                n_invalid_sets.append(len(invalid_sets)) #store num of invalid sets, organized by user name (aligned with all_sets)
      
    return (all_sets, n_valid_sets, n_invalid_sets)

#fashion_items = dict([]), to record (image url(key), image name), not related to specific user
#unique_images = dict([]), record this (image name(key), other information) into unique_images, not related to specific user
fashion_items, unique_images, failed_images, n_all_items, n_fashion_items, user_number = get_all_items()
#all_sets = list([]), store all information about sets, organized by user name
#n_valid_sets = list([]), store num of valid sets, organized by user name (aligned with all_sets)
#n_invalid_sets = list([]), store num of invalid sets, organized by user name (aligned with all_sets)
all_sets, n_valid_sets, n_invalid_sets = get_valid_sets(fashion_items, unique_images, user_number)

#decide minimum_valid_sets_number for each user
import numpy as np


# minimum_sets_num = -1

# user_num = len(n_valid_sets) # min(user_num from get_all_items(), user_num from get_valid_sets())
# y, x = np.histogram(n_valid_sets, bins=np.linspace(1, max(n_valid_sets)+1, max(n_valid_sets)+1))
# percent = np.linspace(1,0.6,41)
# for i in range(0,41):
#     count = 0
#     for j in range(max(n_valid_sets)+1,1,-1):
#         count = count + y[j-2]
#         if(count >= (user_num * percent[i])):
#             break
#     minimum_sets_num = j -1
#     print("minimum_sets_num = {}, when percent is: {}, total user_num is: {}\n".format(minimum_sets_num, percent[i], count))

user_outfit = []
nr_tuples_sum = 0.0
#to generate dict_tops/bot/sho & i_top/bot/sho & user_ids
for i in range(len(all_sets)): #for each user
    nr_tuples = 0 #valid tuples num for each user
    for j in range(len(all_sets[i]['valid_sets'])): #for each valid tuple of user_i
        nr_tuples += len(all_sets[i]['valid_sets'][j]['items'][0]) # (can be multiple top items here, will be split later)
    user_outfit.append(nr_tuples)
    nr_tuples_sum += nr_tuples

print("\nuser num: {}, outfits num: {}\n".format(len(all_sets), nr_tuples_sum))

y, x = np.histogram(user_outfit, bins=np.linspace(1, max(user_outfit), 100))

fig = plt.figure()
plt.bar(x[:-1], y, width=1)
plt.xlim(min(x), max(x))
plt.grid()
plt.xlabel("outfit number / user")
plt.ylabel("user number")
plt.title("Polyvore outfit dataset size")
plt.savefig('./dataset_size.png', bbox_inches='tight')
plt.close('all')

# fig = plt.figure()
# ax_left = fig.add_subplot(111)
# ax_left.plot(x, y, '--g')
# lines_left, labels_left = ax_left.get_legend_handles_labels()   
# ax_left.legend(lines_left, labels_left, loc=0)
# ax_left.grid()
# ax_left.set_xlabel("outfit number / user")
# ax_left.set_ylabel("user number")
# ax_left.set_title("Polyvore outfit dataset size")
# plt.savefig(root+'./dataset_size.png', bbox_inches='tight')
# plt.close('all')