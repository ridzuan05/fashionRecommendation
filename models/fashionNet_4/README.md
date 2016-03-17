*Brief description: Siamese Training

*Procedures:
 1) for each user, how to prepare posi-posi input outfit pair: pick out N nearest edges from G(posi outfit, VGG_Vec_distance), N is the number of posi_outfits of this user, all posi outfit mush appear as the left outfit (dominant outfit) for at least one time;
 2) for each user's each posi outfit, how to prepare posi-neg input outfit pair: a) K-means for all outfits from all users, i.e. 20 categories; b) pick 3 outfits from farest (cluster center distance from the cluster center of this posi outfit) 5 clusters respectively, thus posi-neg ratio is 1-15;
 3) Siamese Training;
 4) Testing (from Serge fashion Siamese ICCV 2015): a) pool outfit K-means into 20 clusters; b) pick 5 outfits, which are cloest form the cluster center, from the nearest cluster; c) select the one with shortest distance between its OutfitVec-Query Cluster Center;
