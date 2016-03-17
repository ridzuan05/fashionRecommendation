EXAMPLE=/home/tonghe/caffe-master/data/fashionRecommendation
DATA=/home/tonghe/caffe-master/data/fashionRecommendation
TOOLS=/home/tonghe/caffe-master/build/tools

TRAIN_DATA_ROOT_TOP=/home/tonghe/caffe-master/data/fashionRecommendation/Polyvore_small/Images/top/
TRAIN_DATA_ROOT_BOTTOM=/home/tonghe/caffe-master/data/fashionRecommendation/Polyvore_small/Images/bottom/
TRAIN_DATA_ROOT_SHOE=/home/tonghe/caffe-master/data/fashionRecommendation/Polyvore_small/Images/shoe/
VAL_DATA_ROOT_TOP=/home/tonghe/caffe-master/data/fashionRecommendation/Polyvore_small/Images/top/
VAL_DATA_ROOT_BOTTOM=/home/tonghe/caffe-master/data/fashionRecommendation/Polyvore_small/Images/bottom/
VAL_DATA_ROOT_SHOE=/home/tonghe/caffe-master/data/fashionRecommendation/Polyvore_small/Images/shoe/

RESIZE=true
if $RESIZE; then
  RESIZE_HEIGHT=224
  RESIZE_WIDTH=224
else
  RESIZE_HEIGHT=0
  RESIZE_WIDTH=0
fi

if [ ! -d "$TRAIN_DATA_ROOT_TOP" ]; then
  echo "Error: TRAIN_DATA_ROOT_TOP is not a path to a directory: $TRAIN_DATA_ROOT_TOP"
  echo "Set the TRAIN_DATA_ROOT_TOP variable in create_imagenet.sh to the path" \
       "where the FashionRecommendation training data is stored."
  exit 1
fi

if [ ! -d "$TRAIN_DATA_ROOT_BOTTOM" ]; then
  echo "Error: TRAIN_DATA_ROOT_BOTTOM is not a path to a directory: $TRAIN_DATA_ROOT_BOTTOM"
  echo "Set the TRAIN_DATA_ROOT_BOTTOM variable in create_imagenet.sh to the path" \
       "where the FashionRecommendation training data is stored."
  exit 1
fi

if [ ! -d "$TRAIN_DATA_ROOT_SHOE" ]; then
  echo "Error: TRAIN_DATA_ROOT_SHOE is not a path to a directory: $TRAIN_DATA_ROOT_SHOE"
  echo "Set the TRAIN_DATA_ROOT_SHOE variable in create_imagenet.sh to the path" \
       "where the FashionRecommendation training data is stored."
  exit 1
fi

if [ ! -d "$VAL_DATA_ROOT_TOP" ]; then
  echo "Error: VAL_DATA_ROOT_TOP is not a path to a directory: $VAL_DATA_ROOT_TOP"
  echo "Set the VAL_DATA_ROOT_TOP variable in create_imagenet.sh to the path" \
       "where the FashionRecommendation test data is stored."
  exit 1
fi

if [ ! -d "$VAL_DATA_ROOT_BOTTOM" ]; then
  echo "Error: VAL_DATA_ROOT_BOTTOM is not a path to a directory: $VAL_DATA_ROOT_BOTTOM"
  echo "Set the VAL_DATA_ROOT_BOTTOM variable in create_imagenet.sh to the path" \
       "where the FashionRecommendation test data is stored."
  exit 1
fi

if [ ! -d "$VAL_DATA_ROOT_SHOE" ]; then
  echo "Error: VAL_DATA_ROOT_SHOE is not a path to a directory: $VAL_DATA_ROOT_SHOE"
  echo "Set the VAL_DATA_ROOT_SHOE variable in create_imagenet.sh to the path" \
       "where the FashionRecommendation test data is stored."
  exit 1
fi

#GLOG_logtostderr=1 $TOOLS/convert_imageset \
#    --resize_height=$RESIZE_HEIGHT \
#    --resize_width=$RESIZE_WIDTH \
#    --shuffle \
#    $TRAIN_DATA_ROOT_TOP \
#    $DATA/train_top.txt \
#    $EXAMPLE/train_top_lmdb

echo "Creating train_top lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    $TRAIN_DATA_ROOT_TOP \
    $DATA/train_top.txt \
    $EXAMPLE/train_top_lmdb

echo "Creating train_bottom lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    $TRAIN_DATA_ROOT_BOTTOM \
    $DATA/train_bottom.txt \
    $EXAMPLE/train_bottom_lmdb

echo "Creating train_shoe lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    $TRAIN_DATA_ROOT_SHOE \
    $DATA/train_shoe.txt \
    $EXAMPLE/train_shoe_lmdb

echo "Creating test_top lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    $VAL_DATA_ROOT_TOP \
    $DATA/test_top.txt \
    $EXAMPLE/test_top_lmdb

echo "Creating test_bottom lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    $VAL_DATA_ROOT_BOTTOM \
    $DATA/test_bottom.txt \
    $EXAMPLE/test_bottom_lmdb

echo "Creating test_shoe lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    $VAL_DATA_ROOT_SHOE \
    $DATA/test_shoe.txt \
    $EXAMPLE/test_shoe_lmdb

echo "Done."
