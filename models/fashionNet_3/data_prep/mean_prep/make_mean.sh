EXAMPLE=/local2/home/tong/fashionRecommendation/models/fashionNet_3/data_prep/lmdb_data
DATA=/local2/home/tong/fashionRecommendation/models/fashionNet_3/data_prep/mean_prep
TOOLS=/local2/home/tong/caffe-master/build/tools

echo "Creating top_mean.binaryproto ..."
$TOOLS/compute_image_mean $EXAMPLE/train_p_top_lmdb \
  $DATA/top_mean.binaryproto

echo "Creating bot_mean.binaryproto ..."
$TOOLS/compute_image_mean $EXAMPLE/train_p_bot_lmdb \
  $DATA/bot_mean.binaryproto

echo "Creating sho_mean.binaryproto ..."
$TOOLS/compute_image_mean $EXAMPLE/train_p_sho_lmdb \
  $DATA/sho_mean.binaryproto

echo "Done."