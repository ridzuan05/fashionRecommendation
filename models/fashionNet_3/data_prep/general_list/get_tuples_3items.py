import os
import numpy as np
import codecs
import time

#all_sets = list([]), store all information about sets, organized by user name
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
#     set_url; 
#   ]
#]
#unique_images = dict([]), record this (image name(key), other information) into unique_images, not related to specific user
#unique_images[img_name] = {
#    'categories': item['categories'], (a list for top/bottom/shoes)
#    'path': os.path.join(img_folder,img_name), 
#    'count': 1, 
#    'name': item['name'],
#    'price': item['price'],
#    'description': item['description']}   
def get_all_tuples(all_sets, unique_images, minimum_sets_num):
    min_nr_tuples = minimum_sets_num #old value 225, minimal number of valid tuples a user should have for his/her data to be used
    dict_tops = dict() #record top_image_name if it appear for the first time, in the range of all items
    dict_bottoms = dict() #record bot_image_name if it appear for the first time, in the range of all items
    dict_shoes = dict() #record sho_image_name if it appear for the first time, in the range of all items
    i_top = 0 #count number of different tops, in the range of all items
    i_bottom = 0 #count number of different bots, in the range of all items
    i_shoe = 0 #count number of different shos, in the range of all items
    user_ids = list([]) #record idx for user_i as valid user
    #to generate dict_tops/bot/sho & i_top/bot/sho & user_ids
    for i in range(len(all_sets)): #for each user
        nr_tuples = 0 #valid tuples num for each user
        for j in range(len(all_sets[i]['valid_sets'])): #for each valid tuple of user_i
            nr_tuples += len(all_sets[i]['valid_sets'][j]['items'][0]) # (can be multiple top items here, will be split later)
        if nr_tuples >= min_nr_tuples: #if valid tuples num of user_i > predefined min num
            user_ids.append(i) #record idx for user_i as valid user
            for j in range(len(all_sets[i]['valid_sets'])): #for each valid tuple of user_i
                fn = all_sets[i]['valid_sets'][j]['items'][1][0] #bot_image_name of this set of user_i 
                if (fn not in dict_bottoms): #record bot_image_name if it appear for the first time, in the range of all items
                    dict_bottoms[fn] = i_bottom
                    i_bottom = i_bottom+1 #count number of different bots, in the range of all items

                for k in range(len(all_sets[i]['valid_sets'][j]['items'][0])):
                    fn = all_sets[i]['valid_sets'][j]['items'][0][k] #top_image_name of this set of user_i
                    if (fn not in dict_tops): #record top_image_name if it appear for the first time, in the range of all items
                        dict_tops[fn] = i_top
                        i_top = i_top+1 #count number of different tops, in the range of all items

                fn = all_sets[i]['valid_sets'][j]['items'][2][0] #sho_image_name of this set of user_i
                if (fn not in dict_shoes): #record sho_image_name if it appear for the first time, in the range of all items
                    dict_shoes[fn] = i_shoe
                    i_shoe= i_shoe+1 #count number of different shos, in the range of all items                       
                        
    fn_top = '/local2/home/tong/fashionRecommendation/models/fashionNet_3/data_prep/general_list/img_list_top.txt'
    fn_bottom = '/local2/home/tong/fashionRecommendation/models/fashionNet_3/data_prep/general_list/img_list_bottom.txt'
    fn_shoe = '/local2/home/tong/fashionRecommendation/models/fashionNet_3/data_prep/general_list/img_list_shoe.txt'

#    root_folder = "data"         
#    fn_top = "%s\\img_list\\img_list_top.txt" % root_folder
#    fn_bottom = "%s\\img_list\\img_list_bottom.txt" % root_folder  
#    fn_shoe = "%s\\img_list\\img_list_shoe.txt" % root_folder       
#    fn_top_name = "%s\\img_list\\img_name_top.txt" % root_folder
#    fn_top_cate = "%s\\img_list\\img_category_top.txt" % root_folder
#    fn_top_price = "%s\\img_list\\img_price_top.txt" % root_folder
#    fn_top_descr = "%s\\img_list\\img_description_top.txt" % root_folder
#    fn_bottom_name = "%s\\img_list\\img_name_bottom.txt" % root_folder
#    fn_bottom_cate = "%s\\img_list\\img_category_bottom.txt" % root_folder
#    fn_bottom_price = "%s\\img_list\\img_price_bottom.txt" % root_folder
#    fn_bottom_descr = "%s\\img_list\\img_description_bottom.txt" % root_folder
#    fn_shoe_name = "%s\\img_list\\img_name_shoe.txt" % root_folder
#    fn_shoe_cate = "%s\\img_list\\img_category_shoe.txt" % root_folder
#    fn_shoe_price = "%s\\img_list\\img_price_shoe.txt" % root_folder
#    fn_shoe_descr = "%s\\img_list\\img_description_shoe.txt" % root_folder       
        
    list_top = ['' for i in range(len(dict_tops))] #initialization by number of top_image_name
    for fn, i in dict_tops.iteritems(): #convert all top_image_name from dictionary to a list
        list_top[i] = fn 
    fid = open(fn_top, 'w') #write all top image paths into img_list_top.txt
    for i in range(len(list_top)):
        fid.write('%s\n' % unique_images[list_top[i]]['path'])
    fid.close()

    list_bottom = ['' for i in range(len(dict_bottoms))] #initialization by number of bot_image_name
    for fn, i in dict_bottoms.iteritems(): #convert all bot_image_name from dictionary to a list
        list_bottom[i] = fn
    fid = open(fn_bottom, 'w') #write all bot image paths into img_list_bottom.txt
    for i in range(len(list_bottom)):
        fid.write('%s\n' % unique_images[list_bottom[i]]['path'])
    fid.close()

    list_shoe = ['' for i in range(len(dict_shoes))] #initialization by number of sho_image_name
    for fn, i in dict_shoes.iteritems(): #convert all sho_image_name from dictionary to a list
        list_shoe[i] = fn
    fid = open(fn_shoe, 'w') #write all sho image paths into img_list_sho.txt
    for i in range(len(list_shoe)):
        fid.write('%s\n' % unique_images[list_shoe[i]]['path'])
    fid.close()    
    
#    get_img_info(unique_images, list_top, fn_top_name, "name", 1)
#    get_img_info(unique_images, list_top, fn_top_cate, "categories", 0)
#    get_img_info(unique_images, list_top, fn_top_price, "price", 1)
#    get_img_info(unique_images, list_top, fn_top_descr, "description", 1)
#    get_img_info(unique_images, list_bottom, fn_bottom_name, "name", 1)
#    get_img_info(unique_images, list_bottom, fn_bottom_cate, "categories", 0)
#    get_img_info(unique_images, list_bottom, fn_bottom_price, "price", 1)
#    get_img_info(unique_images, list_bottom, fn_bottom_descr, "description", 1)
#    get_img_info(unique_images, list_shoe, fn_shoe_name, "name", 1)
#    get_img_info(unique_images, list_shoe, fn_shoe_cate, "categories", 0)
#    get_img_info(unique_images, list_shoe, fn_shoe_price, "price", 1)
#    get_img_info(unique_images, list_shoe, fn_shoe_descr, "description", 1)    
    
    all_tuples = list([]) #store final idx of (top_image, bot_image, sho_image) of each valid set wrt all users
    all_setids = list([]) #store idx of each valid set wrt all users
    for i in range(len(user_ids)): #for each valid user
        tuples = list([]) #store final idx of (top_image, bot_image, sho_image) of each valid set wrt user_i
        setids = list([]) #store idx of each valid set wrt user_i
        for j in range(len(all_sets[user_ids[i]]['valid_sets'])): #for each valid set wrt user_i
            fn = all_sets[user_ids[i]]['valid_sets'][j]['items'][1][0] #bot_image_name fo this set
            bottom_id = dict_bottoms[fn] #get final idx of bot_image_name
            fn = all_sets[user_ids[i]]['valid_sets'][j]['items'][2][0] #sho_image_name fo this set
            shoe_id = dict_shoes[fn] #get final idx of sho_image_name
            for k in range(len(all_sets[user_ids[i]]['valid_sets'][j]['items'][0])):
                fn = all_sets[user_ids[i]]['valid_sets'][j]['items'][0][k] #top_image_name fo this set
                top_id = dict_tops[fn] #get final idx of top_image_name
                tuples.append([top_id, bottom_id, shoe_id]) #get final idx of (top_image, bot_image, sho_image) of each valid set wrt user_i
                setids.append(j) #get idx of each valid set wrt user_i
        all_tuples.append(tuples) #store final idx of (top_image, bot_image, sho_image) of each valid set wrt all users
        all_setids.append(setids) #store idx of each valid set wrt all users

    train_val_test_devision = list([0.00,0.80,0.81,1.00])
 
#tuple indexes for training
#    tpl_inds_train = [np.arange(0, 60), np.arange(30, 90),
#                      np.hstack((np.arange(0, 30), np.arange(60, 90))), 
#                      np.arange(0, 90), np.arange(45, 135),
#                      np.hstack((np.arange(0, 45), np.arange(90, 135))),
#                      np.arange(0, 120), np.arange(60, 180),
#                      np.hstack((np.arange(0, 60), np.arange(120, 180))),
#                      np.arange(0, 90),
#                      np.arange(0, 135), np.arange(0, 180)]
#tuple indexes for testing
#    tpl_inds_test = [np.arange(60, 90), np.arange(0, 30), np.arange(30, 60),
#                     np.arange(90, 135), np.arange(0, 45), np.arange(45, 90),
#                     np.arange(120, 180), np.arange(0, 60), np.arange(60, 120),
#                     np.arange(180, 225)] # "tuple_90" "tuple_135" "tuple_180" share the same testing set,
                                         # which is saved in "tuple_90". Copy the corresponding testing files in "tuple_90" to "tuple_135" and "tuple_180".

#    folder_names = ["tuple_90_cv1", "tuple_90_cv2", "tuple_90_cv3",
#                    "tuple_135_cv1", "tuple_135_cv2", "tuple_135_cv3",
#                    "tuple_180_cv1", "tuple_180_cv2", "tuple_180_cv3",
#                    "tuple_90", "tuple_135", "tuple_180"]            
               

    #for each folder_names mentioned above
    #for i in range(len(folder_names)):
    sub_folder = '/local2/home/tong/fashionRecommendation/models/fashionNet_3/data_prep/general_list/'
    #sub_folder = "%s\\%s" % (root_folder, folder_names[i])
    if not os.path.isdir(sub_folder): #mkdir for each folder_names
        os.mkdir(sub_folder)

    #training dataset
    fn_top_ind_train = sub_folder+'top_ind_train.txt'
    fn_bottom_ind_train = sub_folder+'bottom_ind_train.txt'
    fn_shoe_ind_train = sub_folder+'shoe_ind_train.txt'
    fn_tuples_train_posi = sub_folder+'tuples_train_posi.txt'
    fn_tuples_train_neg = sub_folder+'tuples_train_neg.txt'
    ###validation dataset
    fn_top_ind_val = sub_folder+'top_ind_val.txt'
    fn_bottom_ind_val = sub_folder+'bottom_ind_val.txt'
    fn_shoe_ind_val = sub_folder+'shoe_ind_val.txt'
    fn_tuples_val_posi = sub_folder+'tuples_val_posi.txt'
    fn_tuples_val_neg = sub_folder+'tuples_val_neg.txt'
    ###testing dataset
    fn_top_ind_test = sub_folder+'top_ind_test.txt'
    fn_bottom_ind_test = sub_folder+'bottom_ind_test.txt'
    fn_shoe_ind_test = sub_folder+'shoe_ind_test.txt'
    fn_tuples_test_posi = sub_folder+'tuples_test_posi.txt'
    fn_tuples_test_neg = sub_folder+'tuples_test_neg.txt'

#    fn_top_ind_train = "%s\\top_ind_train.txt" % sub_folder
#    fn_bottom_ind_train = "%s\\bottom_ind_train.txt" % sub_folder
#    fn_shoe_ind_train = "%s\\shoe_ind_train.txt" % sub_folder
#    fn_tuples_train_posi = "%s\\tuples_train_posi.txt" % sub_folder
#    fn_tuples_train_neg = "%s\\tuples_train_neg.txt" % sub_folder
#    fn_tuples_train_posi_imgpath = ''
#    if i >= 9:
#        fn_tuples_train_posi_imgpath = "%s\\tuples_train_posi_imgpath.txt" % sub_folder

    #define testing file paths thare would be used very soon
#    fn_top_ind_test = "%s\\top_ind_test.txt" % sub_folder
#    fn_bottom_ind_test = "%s\\bottom_ind_test.txt" % sub_folder
#    fn_shoe_ind_test = "%s\\shoe_ind_test.txt" % sub_folder
#    fn_tuples_test_posi = "%s\\tuples_test_posi.txt" % sub_folder
#    fn_tuples_test_neg = "%s\\tuples_test_neg.txt" % sub_folder
#    fn_tuples_test_posi_imgpath = ''
#    if i >= 9:
#        fn_tuples_test_posi_imgpath = "%s\\tuples_test_posi_imgpath.txt" % sub_folder

    ratio = 5

###training dataset
    print 'training posi ...\n'
    #create: top_ind_train.txt, bottom_ind_train.txt, shoe_ind_train.txt, tuples_train_posi.txt
    dict_tops_train, dict_bottoms_train, dict_shoes_train, n_posi_tuples_train = get_positive_tuples(
        all_tuples, train_val_test_devision[0],train_val_test_devision[1],
        list_top, list_bottom, list_shoe,
        all_sets, user_ids, all_setids,
        fn_top_ind_train, fn_bottom_ind_train, fn_shoe_ind_train,
        fn_tuples_train_posi,
        ratio)
    print 'training nega ...\n'
    #create tuples_train_neg.txt
    get_negative_tuples2(user_ids, len(dict_tops_train),
                         len(dict_bottoms_train), len(dict_shoes_train),
                         fn_tuples_train_neg, fn_tuples_train_posi, n_posi_tuples_train,ratio)

###validation dataset
    print 'validation posi ...\n'
    #create: top_ind_train.txt, bottom_ind_train.txt, shoe_ind_train.txt, tuples_train_posi.txt
    dict_tops_val, dict_bottoms_val, dict_shoes_val, n_posi_tuples_val = get_positive_tuples(
        all_tuples, train_val_test_devision[1],train_val_test_devision[2],
        list_top, list_bottom, list_shoe,
        all_sets, user_ids, all_setids,
        fn_top_ind_val, fn_bottom_ind_val, fn_shoe_ind_val,
        fn_tuples_val_posi,
        ratio)
    print 'validation nega ...\n'
    #create tuples_train_neg.txt
    get_negative_tuples2(user_ids, len(dict_tops_val),
                         len(dict_bottoms_val), len(dict_shoes_val),
                         fn_tuples_val_neg, fn_tuples_val_posi, n_posi_tuples_val,ratio)

#        get_negative_tuples2_for_strong_generalization(user_ids, 
#                                                       fn_tuples_train_neg,
#                                                       fn_tuples_train_posi,
#                                                       n_posi_tuples_train,
#                                                       125)                             

    #if i <= 9: # generate test tuples for the settings in "tpl_inds_test"

###testing dataset
    print 'testing posi ...\n'
    #create top_ind_test.txt, bottom_ind_test.txt, shoe_ind_test.txt, tuples_test_posi.txt
    dict_tops_test, dict_bottoms_test, dict_shoes_test, n_posi_tuples_test = get_positive_tuples(
        all_tuples, train_val_test_devision[2],train_val_test_devision[3],
        list_top, list_bottom, list_shoe,
        all_sets, user_ids, all_setids,
        fn_top_ind_test, fn_bottom_ind_test, fn_shoe_ind_test,
        fn_tuples_test_posi,
        ratio)
    print 'testing nega ...\n'
    #create tuples_test_neg.txt
    get_negative_tuples2(user_ids, len(dict_tops_test),
                         len(dict_bottoms_test), len(dict_shoes_test),
                         fn_tuples_test_neg, fn_tuples_test_posi, n_posi_tuples_test,ratio)
    
#    get_negative_tuples_hard(all_sets, user_ids,
#                             dict_tops_test, dict_bottoms_test,
#                             dict_shoes_test, fn_tuples_test_neg,
#                             fn_tuples_test_posi, n_posi_tuples_test)

#unique_images, list of iamge_name_top/bot/sho, file_path, name/categories/price/description, 1/0/1/1
def get_img_info(unique_images, li, fn, info_name, is_string):
    fid = codecs.open(fn, encoding='utf-8', mode='w') #open file_path
    for i in range(len(li)): #for each image_name in the list
        if is_string: #is string
            #write name/categories/price/description into file_path for each image_name
            fid.write('%s\n' % unique_images[li[i]][info_name].replace('\n', ' ').replace('\r', ' ').replace(u'\u2028', ' ').replace(u'\x85', ' '))
        else: #not a string
            #write (top_category, bot_category, sho_category) into file_path for each image_name
            ctgy = unique_images[li[i]][info_name]
            for j in range(1, len(ctgy)):
                fid.write('%s ' % ctgy[j])
            fid.write('\n')
    fid.close()  


def get_positive_tuples(all_tuples, start_percent, end_percent, list_top, list_bottom, list_shoe,
                        all_sets, user_ids, all_setids,
                        fn_top_ind, fn_bottom_ind, fn_shoe_ind, fn_tuples, ratio):
    tuples = list([]) #store (user idx, final top idx, final bot idx, final sho idx) for all users
    n_posi_tuples = np.zeros(len(all_tuples), dtype=np.int) #count tuples num for each user

    for i in range(len(all_tuples)): #for each users
        start_tuple_idx = int(len(all_tuples[i])*start_percent)
        end_tuple_idx = int(len(all_tuples[i])*end_percent)
        for j in range(start_tuple_idx, end_tuple_idx):
#        for j in tpl_inds: #j = 0, 1,..., tuples num predefined for each user
            tuples.append((i, all_tuples[i][j][0], all_tuples[i][j][1], all_tuples[i][j][2])) #store (user idx, final top idx, final bot idx, final sho idx) for all users
            n_posi_tuples[i] += 1 #count tuples num for each user

    tuples = np.array(tuples) #convert list to array
    u_top, indices_top = np.unique(tuples[:, 1], return_inverse=True) #create inter top idx
    tuples[:, 1] = indices_top #inter idx for all top images
    u_bottom, indices_bottom = np.unique(tuples[:, 2], return_inverse=True) #create inter bot idx
    tuples[:, 2] = indices_bottom #inter idx for all bot images
    u_shoe, indices_shoe = np.unique(tuples[:, 3], return_inverse=True) #create inter sho idx
    tuples[:, 3] = indices_shoe #inter idx for all sho images

    # only len(dict_tops/bottoms/shoes_subset) are used later !!!! But they are important!
    # these lengths are used to confine train/val/test dataset to their own range of top/bot/sho images (completely data separation), utilizaing the concept of inter idx    
    dict_tops_subset = dict() #[top_image_name, inter top idx]
    for i in range(len(u_top)): #for each final top idx
        dict_tops_subset[list_top[u_top[i]]] = i #[top_image_name, inter top idx]

    dict_bottoms_subset = dict() #[bot_image_name, inter bot idx]
    for i in range(len(u_bottom)): #for each final bot idx
        dict_bottoms_subset[list_bottom[u_bottom[i]]] = i #[bot_image_name, inter bot idx]

    dict_shoes_subset = dict() #[sho_image_name, inter sho idx]
    for i in range(len(u_shoe)): #for each final sho idx
        dict_shoes_subset[list_shoe[u_shoe[i]]] = i #[sho_image_name, inter sho idx]

    fid = open(fn_top_ind, 'w') #open inter top idx file
    for u in u_top:
        fid.write('%d\n' % u) #write final top idx into top_ind_train.txt
    fid.close()

    fid = open(fn_bottom_ind, 'w') #open inter bottom idx file
    for u in u_bottom:
        fid.write('%d\n' % u) #write final bot idx into bottom_ind_train.txt 
    fid.close()

    fid = open(fn_shoe_ind, 'w') #open inter shoes idx file
    for u in u_shoe:
        fid.write('%d\n' % u) #write final sho idx into shoe_ind_train.txt
    fid.close()

    fid = open(fn_tuples, 'w') #open tuples_train_posi.txt
    for i in range(tuples.shape[0]):
        for k in range(0,ratio):
            fid.write('%d %d %d %d\n' % (tuples[i, 0], tuples[i, 1], tuples[i, 2],
                                      tuples[i, 3])) #write (user idx, inter top idx, inter bot idx, inter sho idx) for all users into tuples_train_posi.txt
    fid.close()

#    if fn_tuple_imgpath != '':
#        fid_path = open(fn_tuple_imgpath, 'w')
#        for i in range(len(user_ids)): #for each valid user
#            for j in tpl_inds: #j = 0, 1,..., tuples num predefined for each user
#                fid_path.write('%s\n' % all_sets[user_ids[i]]['valid_sets'][all_setids[i][j]]['img_path']) #write tuple image path for all users into tuples_train_posi_imgpath.txt
#        fid_path.close()

    return (dict_tops_subset, dict_bottoms_subset, dict_shoes_subset,
            n_posi_tuples)

#create tuples_train_neg.txt according to neg_posi_ratio, candi_margin should be large enough to create redundancy
def get_negative_tuples2(user_ids, num_top, num_bottom, num_shoe,
                         fn_tuples_neg, fn_tuples_posi, n_posi_tuples,ratio):
    neg_posi_ratio = ratio
    candi_margin_mul = 3

    posi_set = set([]) #store [user id, inter top id, inter bot id, inter sho id] for all uers
    with open(fn_tuples_posi, 'r') as f: #open tuples_train_posi.txt
        for line in f: #for each posi train tuple (user id, inter top id, inter bot id, inter sho id)
            data = line.strip('\r\n').split(' ') # data = [user id, inter top id, inter bot id, inter sho id]
            tpl = [int(ind) for ind in data]
            posi_set.add('%03d%05d%05d%05d' % (tpl[0], tpl[1], tpl[2], tpl[3])) #store [user id, inter top id, inter bot id, inter sho id] for all uers

    fid = open(fn_tuples_neg, 'w') #open tuples_train_neg.txt
    for i in range(len(user_ids)): #for each valid user i
        n_neg_tuples = n_posi_tuples[i]*neg_posi_ratio #num of valid tuples of each valid user * ration
        n_candi = n_neg_tuples*candi_margin_mul #for creating redundency (because ramdomly created neg tuple many still be the same as posi tuple)

        tuples_neg = np.empty((4, n_candi), dtype=np.int)
        tuples_neg[0, :] = i #user idx

        # num_top/bot/sho are used to confine train/val/test dataset to their own range of top/bot/sho images (completely data separation), utilizaing the concept of inter idx
        tuples_neg[1, :] = np.random.choice(num_top, n_candi, replace=True) #randomly select n_candi number of inter top idicies, based on all users' tuples
        tuples_neg[2, :] = np.random.choice(num_bottom, n_candi, replace=True) #randomly select n_candi number of inter bottom idicies, based on all users' tuples
        tuples_neg[3, :] = np.random.choice(num_shoe, n_candi, replace=True) #randomly select n_candi number of inter shoes idicies, based on all users' tuples

        ids = list([]) #valid neg tuple idx of this user i
        for k in range(n_candi): #for each neg tuples of user i
            ss = '%03d%05d%05d%05d' % (tuples_neg[0, k], tuples_neg[1, k],
                                       tuples_neg[2, k], tuples_neg[3, k]) #create (user id, neg inter top idx, neg inter bot idx, neg inter sho idx)
            if ss not in posi_set:
                ids.append(k) #valid neg tuple idx of this user i
        tuples_neg = tuples_neg.take(ids, axis=1) #take out qualified neg tuples, according to colum idx
        if tuples_neg.shape[1] < n_neg_tuples: #nega tuples number of this user should be at least above the ratio
            print ("Posi_tuple: need to increase candi_margin_mul, now it is {}".format(candi_margin_mul)) #we need more redundancy to make sure that we have created enough number of nega tuples
            # time.sleep(5.5)

        for k in range(n_neg_tuples): #for each nega tuple
            fid.write('%d %d %d %d\n' % (tuples_neg[0, k], tuples_neg[1, k],
                                         tuples_neg[2, k], tuples_neg[3, k])) #write (user id, neg inter top idx, neg inter bot idx, neg inter sho idx) into tuples_train_neg.txt
    fid.close()

def get_negative_tuples_hard(all_sets, user_ids, dict_top, dict_bottom,
                             dict_shoe, fn_tuples_neg, fn_tuples_posi,
                             n_posi_tuples):
    neg_posi_ratios = [1, 1, 1, 5] #sigma[1*1, 3*1, 1*1, 1*5] = 10
    total_ratio = 10
    candi_margin_mul = 3
    fid = open(fn_tuples_neg, 'w') #open tuples_test_neg.txt

    posi_tuples = list([]) #list to store [user id, inter top idx, inter bot idx, inter sho idx] from tuples_test_posi.txt
    with open(fn_tuples_posi, 'r') as f: #open tuples_test_posi.txt
        for line in f: #for each (user id, inter top idx, inter bot idx, inter sho idx)
            data = line.strip('\r\n').split(' ') #data = [user id, inter top idx, inter bot idx, inter sho idx]
            tpl = [int(ind) for ind in data]
            posi_tuples.append(tpl)
    posi_tuples = np.array(posi_tuples).transpose() #list to arrary, & transpose
    
    item_nums = [0, len(dict_top), len(dict_bottom), len(dict_shoe)] #top img number, bot img number, sho img number
    posi_ind = 0
    for i in range(len(user_ids)): #for each valid user i
        posi_set = set([])
        for j in range(len(all_sets[user_ids[i]]['valid_sets'])): #for each valid set j of this user_(i)
            fn = all_sets[user_ids[i]]['valid_sets'][j]['items'][1][0] #bot_image_name of set_j of user_(i)
            if (fn not in dict_bottom):
                continue
            else:
                bottom_id = dict_bottom[fn] #inter idx for this bot_image_name

            fn = all_sets[user_ids[i]]['valid_sets'][j]['items'][2][0] #sho_image_name of set_j of user_(i)
            if (fn not in dict_shoe): 
                continue
            else:
                shoe_id = dict_shoe[fn] #inter idx for this sho_image_name

            for k in range(len(all_sets[user_ids[i]][
                    'valid_sets'][j]['items'][0])):
                fn = all_sets[user_ids[i]]['valid_sets'][j]['items'][0][k] #top_image_name
                if (fn not in dict_top):
                    continue
                else:
                    top_id = dict_top[fn] #inter idx for this top_image_name

                posi_set.add('%03d%05d%05d%05d' % (i, top_id, bottom_id,
                                                   shoe_id)) #store (user idx, inter top idx, inter bot idx, inter sho idx) for all users

        n_candi = n_posi_tuples[i]*neg_posi_ratios[0] #part one
        all_neg_tuples = np.empty((4, n_candi), dtype=np.int) 
        all_neg_tuples[0, :] = i
        for k in range(1, 4):
            ind = np.random.choice(n_posi_tuples[i], n_candi, replace=True)
            ind += posi_ind
            all_neg_tuples[k, :] = posi_tuples[k, ind] #the same as test_posi_tuples

        for t in range(1, 4):
            neg_tuples = posi_tuples[:, posi_ind:posi_ind+n_posi_tuples[i]]
            neg_tuples = np.kron(np.ones((1, neg_posi_ratios[1]),
                                         dtype=np.int), neg_tuples) #the same as test_posi_tuples
            for k in range(1, 4):
                if k != t:
                    neg_tuples[k, :] = np.random.choice(
                        item_nums[k],
                        n_posi_tuples[i]*neg_posi_ratios[1],
                        replace=True)
            all_neg_tuples = np.hstack((all_neg_tuples, neg_tuples))

        ind = np.random.choice(posi_tuples.shape[1],
                               n_posi_tuples[i]*neg_posi_ratios[2],
                               replace=False)
        neg_tuples = posi_tuples[:, ind]
        neg_tuples[0, :] = i
        all_neg_tuples = np.hstack((all_neg_tuples, neg_tuples))

        n_candi = n_posi_tuples[i]*neg_posi_ratios[3]*candi_margin_mul
        neg_tuples = np.empty((4, n_candi), dtype=np.int)
        neg_tuples[0, :] = i
        neg_tuples[1, :] = np.random.choice(
            len(dict_top),
            n_candi, replace=True)
        neg_tuples[2, :] = np.random.choice(
            len(dict_bottom),
            n_candi, replace=True)
        neg_tuples[3, :] = np.random.choice(
            len(dict_shoe),
            n_candi, replace=True)
        all_neg_tuples = np.hstack((all_neg_tuples, neg_tuples))

        neg_set = set([])
        ids = list([])
        for k in range(all_neg_tuples.shape[1]):
            ss = '%03d%05d%05d%05d' % (all_neg_tuples[0, k],
                                       all_neg_tuples[1, k],
                                       all_neg_tuples[2, k],
                                       all_neg_tuples[3, k])
            if (ss not in posi_set) and (ss not in neg_set):
                ids.append(k)
                neg_set.add(ss)
        all_neg_tuples = all_neg_tuples[:, ids]
        n_neg_tuples = n_posi_tuples[i] * total_ratio
        if all_neg_tuples.shape[1] < n_neg_tuples:
            print ("Neg_tuple: need to increase candi_margin_mul, now it is {}".format(candi_margin_mul))
            time.sleep(5.5)

        for k in range(n_neg_tuples):
            fid.write('%d %d %d %d\n' % (all_neg_tuples[0, k],
                                         all_neg_tuples[1, k],
                                         all_neg_tuples[2, k],
                                         all_neg_tuples[3, k]))

        posi_ind += n_posi_tuples[i]

    fid.close()

def get_negative_tuples2_for_strong_generalization(user_ids, fn_tuples_neg,
                                                   fn_tuples_posi, 
                                                   n_posi_tuples,
                                                   num_train_user):
    neg_posi_ratio = 5
    candi_margin = 50

    posi_set = set([])
    posi_tuples = list([])
    with open(fn_tuples_posi, 'r') as f:
        for line in f:
            data = line.strip('\r\n').split(' ')
            tpl = [int(ind) for ind in data]
            posi_set.add('%03d%05d%05d%05d' % (tpl[0], tpl[1], tpl[2], tpl[3]))
            if tpl[0]<num_train_user:           
                posi_tuples.append(tpl)

    num_ptuples = len(posi_tuples)
    posi_tuples = np.array(posi_tuples).transpose()
    
    fid = open(fn_tuples_neg, 'w')
    for i in range(len(user_ids)):
        n_neg_tuples = n_posi_tuples[i]*neg_posi_ratio
        n_candi = n_neg_tuples+candi_margin

        tuples_neg = np.empty((4, n_candi), dtype=np.int)
        tuples_neg[0, :] = i

        ind = np.random.choice(num_ptuples, n_candi, replace=True)
        tuples_neg[1, :] = posi_tuples[1, ind]
        ind = np.random.choice(num_ptuples, n_candi, replace=True)
        tuples_neg[2, :] = posi_tuples[2, ind]
        ind = np.random.choice(num_ptuples, n_candi, replace=True)
        tuples_neg[3, :] = posi_tuples[3, ind]

        ids = list([])
        for k in range(n_candi):
            ss = '%03d%05d%05d%05d' % (tuples_neg[0, k], tuples_neg[1, k],
                                       tuples_neg[2, k], tuples_neg[3, k])
            if ss not in posi_set:
                ids.append(k)
        tuples_neg = tuples_neg.take(ids, axis=1)
        if tuples_neg.shape[1] < n_neg_tuples:
            print 'need increase n_candi'

        for k in range(n_neg_tuples):
            fid.write('%d %d %d %d\n' % (tuples_neg[0, k], tuples_neg[1, k],
                                         tuples_neg[2, k], tuples_neg[2, k]))

    fid.close()    
    
#all_sets = list([]), store all information about sets, organized by user name
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
#unique_images = dict([]), record this (image name(key), other information) into unique_images, not related to specific user
#unique_images[img_name] = {
#    'categories': item['categories'], 
#    'path': os.path.join(img_folder,img_name), 
#    'count': 1, 
#    'name': item['name'],
#    'price': item['price'],
#    'description': item['description']}   
get_all_tuples(all_sets, unique_images, minimum_sets_num)