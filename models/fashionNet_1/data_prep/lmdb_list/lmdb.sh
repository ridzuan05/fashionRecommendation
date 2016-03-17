EXAMPLE=/local2/home/tong/fashionRecommendation/models/fashionNet_1/data_prep/lmdb_data
DATA=/local2/home/tong/fashionRecommendation/models/fashionNet_1/data_prep/lmdb_list
TOOLS=/local2/home/tong/caffe-master/build/tools

DATA_ROOT=/local2/..

#############################################
echo "Creating train_p_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_p_top.txt \
    $EXAMPLE/train_p_top_lmdb

echo "Creating train_p_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_p_bot.txt \
    $EXAMPLE/train_p_bot_lmdb

echo "Creating train_p_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_p_sho.txt \
    $EXAMPLE/train_p_sho_lmdb

#########################
echo "Creating train_n_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_n_top.txt \
    $EXAMPLE/train_n_top_lmdb

echo "Creating train_n_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_n_bot.txt \
    $EXAMPLE/train_n_bot_lmdb

echo "Creating train_n_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_n_sho.txt \
    $EXAMPLE/train_n_sho_lmdb

#############################################
echo "Creating val_p_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_p_top.txt \
    $EXAMPLE/val_p_top_lmdb

echo "Creating val_p_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_p_bot.txt \
    $EXAMPLE/val_p_bot_lmdb

echo "Creating val_p_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_p_sho.txt \
    $EXAMPLE/val_p_sho_lmdb

#########################
echo "Creating val_n_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_n_top.txt \
    $EXAMPLE/val_n_top_lmdb

echo "Creating val_n_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_n_bot.txt \
    $EXAMPLE/val_n_bot_lmdb

echo "Creating val_n_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_n_sho.txt \
    $EXAMPLE/val_n_sho_lmdb

#############################################
echo "Creating test_p_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_p_top.txt \
    $EXAMPLE/test_p_top_lmdb

echo "Creating test_p_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_p_bot.txt \
    $EXAMPLE/test_p_bot_lmdb

echo "Creating test_p_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_p_sho.txt \
    $EXAMPLE/test_p_sho_lmdb

#########################
echo "Creating test_n_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_n_top.txt \
    $EXAMPLE/test_n_top_lmdb

echo "Creating test_n_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_n_bot.txt \
    $EXAMPLE/test_n_bot_lmdb

echo "Creating test_n_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_n_sho.txt \
    $EXAMPLE/test_n_sho_lmdb

#############################################
echo "Done."