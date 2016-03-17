EXAMPLE=/local2/home/tong/fashionRecommendation/models/fashionNet_7/data_prep/lmdb_data
DATA=/local2/home/tong/fashionRecommendation/models/fashionNet_7/data_prep/lmdb_list
TOOLS=/local2/home/tong/caffe-master/build/tools

DATA_ROOT=/local2/..

#############################################
echo "Creating train_ll_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_ll_top.txt \
    $EXAMPLE/train_ll_top_lmdb

echo "Creating train_ll_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_ll_bot.txt \
    $EXAMPLE/train_ll_bot_lmdb

echo "Creating train_ll_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_ll_sho.txt \
    $EXAMPLE/train_ll_sho_lmdb

#############################################
echo "Creating train_mm_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_mm_top.txt \
    $EXAMPLE/train_mm_top_lmdb

echo "Creating train_mm_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_mm_bot.txt \
    $EXAMPLE/train_mm_bot_lmdb

echo "Creating train_mm_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_mm_sho.txt \
    $EXAMPLE/train_mm_sho_lmdb

#########################
echo "Creating train_rr_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_rr_top.txt \
    $EXAMPLE/train_rr_top_lmdb

echo "Creating train_rr_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_rr_bot.txt \
    $EXAMPLE/train_rr_bot_lmdb

echo "Creating train_rr_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/train_rr_sho.txt \
    $EXAMPLE/train_rr_sho_lmdb

#############################################
echo "Creating val_ll_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_ll_top.txt \
    $EXAMPLE/val_ll_top_lmdb

echo "Creating val_ll_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_ll_bot.txt \
    $EXAMPLE/val_ll_bot_lmdb

echo "Creating val_ll_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_ll_sho.txt \
    $EXAMPLE/val_ll_sho_lmdb

#############################################
echo "Creating val_mm_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_mm_top.txt \
    $EXAMPLE/val_mm_top_lmdb

echo "Creating val_mm_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_mm_bot.txt \
    $EXAMPLE/val_mm_bot_lmdb

echo "Creating val_mm_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_mm_sho.txt \
    $EXAMPLE/val_mm_sho_lmdb

#########################
echo "Creating val_rr_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_rr_top.txt \
    $EXAMPLE/val_rr_top_lmdb

echo "Creating val_rr_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_rr_bot.txt \
    $EXAMPLE/val_rr_bot_lmdb

echo "Creating val_rr_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/val_rr_sho.txt \
    $EXAMPLE/val_rr_sho_lmdb

#############################################
echo "Creating test_ll_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_ll_top.txt \
    $EXAMPLE/test_ll_top_lmdb

echo "Creating test_ll_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_ll_bot.txt \
    $EXAMPLE/test_ll_bot_lmdb

echo "Creating test_ll_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_ll_sho.txt \
    $EXAMPLE/test_ll_sho_lmdb

#############################################
echo "Creating test_mm_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_mm_top.txt \
    $EXAMPLE/test_mm_top_lmdb

echo "Creating test_mm_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_mm_bot.txt \
    $EXAMPLE/test_mm_bot_lmdb

echo "Creating test_mm_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_mm_sho.txt \
    $EXAMPLE/test_mm_sho_lmdb

#########################
echo "Creating test_rr_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_rr_top.txt \
    $EXAMPLE/test_rr_top_lmdb

echo "Creating test_rr_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_rr_bot.txt \
    $EXAMPLE/test_rr_bot_lmdb

echo "Creating test_rr_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/test_rr_sho.txt \
    $EXAMPLE/test_rr_sho_lmdb

#############################################
echo "Done."