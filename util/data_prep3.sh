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

echo "Creating tr_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/tr_top.txt \
    $EXAMPLE/tr_top_lmdb

echo "Creating tr_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/tr_bottom.txt \
    $EXAMPLE/tr_bot_lmdb

echo "Creating tr_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/tr_shoe.txt \
    $EXAMPLE/tr_sho_lmdb

#############################################

echo "Creating te_top_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/te_top.txt \
    $EXAMPLE/te_top_lmdb

echo "Creating te_bot_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/te_bottom.txt \
    $EXAMPLE/te_bot_lmdb

echo "Creating te_sho_lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --keep_ratio_resize=true \
    $DATA_ROOT \
    $DATA/te_shoe.txt \
    $EXAMPLE/te_sho_lmdb

echo "Done."