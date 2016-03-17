EXAMPLE=/local2/home/tong/fashionRecommendation/data/Polyvore_small
DATA=/local2/home/tong/fashionRecommendation/data
TOOLS=/local2/home/tong/caffe-master/build/tools

DATA_ROOT=/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/

RESIZE=true
if $RESIZE; then
  RESIZE_HEIGHT=224
  RESIZE_WIDTH=224
else
  RESIZE_HEIGHT=0
  RESIZE_WIDTH=0
fi

if [ ! -d "$DATA_ROOT" ]; then
  echo "Error: TRAIN_DATA_ROOT_TOP is not a path to a directory: $TRAIN_DATA_ROOT_TOP"
  echo "Set the TRAIN_DATA_ROOT_TOP variable in create_imagenet.sh to the path" \
       "where the FashionRecommendation training data is stored."
  exit 1
fi

echo "Creating tr_p_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/tr_p_top.txt \
    $EXAMPLE/tr_p_top_lmdb

echo "Creating tr_p_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/tr_p_bottom.txt \
    $EXAMPLE/tr_p_bot_lmdb

echo "Creating tr_p_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/tr_p_shoe.txt \
    $EXAMPLE/tr_p_sho_lmdb

######

echo "Creating tr_n_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/tr_n_top.txt \
    $EXAMPLE/tr_n_top_lmdb

echo "Creating tr_n_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/tr_n_bottom.txt \
    $EXAMPLE/tr_n_bot_lmdb

echo "Creating tr_n_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/tr_n_shoe.txt \
    $EXAMPLE/tr_n_sho_lmdb

#############################################

echo "Creating te_p_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/te_p_top.txt \
    $EXAMPLE/te_p_top_lmdb

echo "Creating te_p_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/te_p_bottom.txt \
    $EXAMPLE/te_p_bot_lmdb

echo "Creating te_p_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/te_p_shoe.txt \
    $EXAMPLE/te_p_sho_lmdb

######

echo "Creating te_n_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/te_n_top.txt \
    $EXAMPLE/te_n_top_lmdb

echo "Creating te_n_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/te_n_bottom.txt \
    $EXAMPLE/te_n_bot_lmdb

echo "Creating te_n_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/te_n_shoe.txt \
    $EXAMPLE/te_n_sho_lmdb

echo "Done."