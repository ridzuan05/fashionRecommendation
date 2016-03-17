EXAMPLE=/local2/home/tong/fashionRecommendation/models/fashionNet_5/data_prep/lmdb_data
DATA=/local2/home/tong/fashionRecommendation/models/fashionNet_5/data_prep/lmdb_list
TOOLS=/local2/home/tong/caffe-master/build/tools

DATA_ROOT=/local2/..

#############################################
echo "Creating train_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_top.txt \
    $EXAMPLE/train_top_lmdb

echo "Creating train_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_bot.txt \
    $EXAMPLE/train_bot_lmdb

echo "Creating train_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_sho.txt \
    $EXAMPLE/train_sho_lmdb

#############################################
echo "Creating val_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_top.txt \
    $EXAMPLE/val_top_lmdb

echo "Creating val_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_bot.txt \
    $EXAMPLE/val_bot_lmdb

echo "Creating val_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_sho.txt \
    $EXAMPLE/val_sho_lmdb

#############################################
echo "Creating test_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_top.txt \
    $EXAMPLE/test_top_lmdb

echo "Creating test_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_bot.txt \
    $EXAMPLE/test_bot_lmdb

echo "Creating test_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_sho.txt \
    $EXAMPLE/test_sho_lmdb

#############################################
echo "Done."