EXAMPLE=/local2/home/tong/fashionRecommendation/models/fashionNet_6/data_prep/lmdb_data
DATA=/local2/home/tong/fashionRecommendation/models/fashionNet_6/data_prep/lmdb_list
TOOLS=/local2/home/tong/caffe-master/build/tools

DATA_ROOT=/local2/..

#############################################
echo "Creating train_l_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_l_top.txt \
    $EXAMPLE/train_l_top_lmdb

echo "Creating train_l_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_l_bot.txt \
    $EXAMPLE/train_l_bot_lmdb

echo "Creating train_l_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_l_sho.txt \
    $EXAMPLE/train_l_sho_lmdb

#########################
echo "Creating train_r_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_r_top.txt \
    $EXAMPLE/train_r_top_lmdb

echo "Creating train_r_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_r_bot.txt \
    $EXAMPLE/train_r_bot_lmdb

echo "Creating train_r_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_r_sho.txt \
    $EXAMPLE/train_r_sho_lmdb

#############################################
echo "Creating val_l_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_l_top.txt \
    $EXAMPLE/val_l_top_lmdb

echo "Creating val_l_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_l_bot.txt \
    $EXAMPLE/val_l_bot_lmdb

echo "Creating val_l_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_l_sho.txt \
    $EXAMPLE/val_l_sho_lmdb

#########################
echo "Creating val_r_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_r_top.txt \
    $EXAMPLE/val_r_top_lmdb

echo "Creating val_r_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_r_bot.txt \
    $EXAMPLE/val_r_bot_lmdb

echo "Creating val_r_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_r_sho.txt \
    $EXAMPLE/val_r_sho_lmdb

#############################################
echo "Creating test_l_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_l_top.txt \
    $EXAMPLE/test_l_top_lmdb

echo "Creating test_l_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_l_bot.txt \
    $EXAMPLE/test_l_bot_lmdb

echo "Creating test_l_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_l_sho.txt \
    $EXAMPLE/test_l_sho_lmdb

#########################
echo "Creating test_r_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_r_top.txt \
    $EXAMPLE/test_r_top_lmdb

echo "Creating test_r_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_r_bot.txt \
    $EXAMPLE/test_r_bot_lmdb

echo "Creating test_r_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_r_sho.txt \
    $EXAMPLE/test_r_sho_lmdb

#############################################
echo "Done."