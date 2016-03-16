#include <opencv2/highgui/highgui.hpp>
#include <opencv2/core/core.hpp>
#include <opencv/cv.hpp>
#include <dirent.h>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>

using namespace cv;
using namespace std;

int main()
{
  ofstream myfile;
  myfile.open ("/local2/home/tong/fashionRecommendation/data/clean_brokenImgs/cleaner/results/broken_imgs.txt");
  int corrupted_count=0;
  const char* PATH = "/local2/home/tong/fashionRecommendation/data/Polyvore_large/1120_users/images";
  DIR *dir = opendir(PATH);
  struct dirent *entry = readdir(dir);
  while (entry != NULL)
  {
    if (entry->d_type == DT_DIR)
    {
      std::string invalid0(entry->d_name);
      if(invalid0.compare(".")!=0 && invalid0.compare("..")!=0)
      {
        const char* PATH_sub_temp = "/local2/home/tong/fashionRecommendation/data/Polyvore_large/1120_users/images/";
        std::string temp2(PATH_sub_temp);
        temp2.append(entry->d_name);
        const char* temp1 = "/items/full";
        temp2.append(temp1);
        const char* PATH_sub = temp2.c_str();
        DIR *dir_sub = opendir(PATH_sub);
        const char* temp0 = "/";
        temp2.append(temp0);
        PATH_sub = temp2.c_str();
        std::cout << PATH_sub << std::endl;
        struct dirent *entry_sub = readdir(dir_sub);
        while(entry_sub != NULL)
        {
          std::string invalid_sub(entry_sub->d_name);
          if(invalid_sub.compare(".")!=0 && invalid_sub.compare("..")!=0)
          {
            std::string temp3(PATH_sub);
            temp3.append(entry_sub->d_name);
            const char* PATH_img = temp3.c_str();
            std::cout << PATH_img << std::endl;
            cv::Mat im0 = cv::imread(PATH_img,CV_LOAD_IMAGE_COLOR);
            if(!im0.data)
            {
              corrupted_count++;
              printf("\n%s---%d\n", PATH_img, corrupted_count);
              myfile << PATH_img << "\n";
            }
          }
          entry_sub = readdir(dir_sub);
        }
        closedir(dir_sub);
      }
    }         
    entry = readdir(dir);
  }
  closedir(dir);
  myfile.close();

  #if 0
    cv::Mat im0 = cv::imread("/home/tonghe2/f7fe11857d2852532f9f0df3e2d0b3e1f1687484.jpg", CV_LOAD_IMAGE_COLOR);
    cv::Mat im1 = cv::imread("/home/tonghe2/ffed7c6d6906aa04a8faec4cd6b08ebb804f420f.jpg", CV_LOAD_IMAGE_COLOR);
    if(im0.data)
      cv::imshow("broken jpg",im0);
    else
      std::cout << "Broken data found!" << std::endl;
    if(im1.data)
      cv::imshow("broken jpg",im1);
  #endif

  std::cout << std::endl;
  std::cout << "corrupted_count = " << corrupted_count << std::endl;
  std::cout << std::endl;
  cv::waitKey(0);
  return 0;
}
