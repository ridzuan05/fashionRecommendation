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

bool DirectoryExists( const char* pzPath )
{
    if ( pzPath == NULL) return false;

    DIR *pDir;
    bool bExists = false;

    pDir = opendir (pzPath);

    if (pDir != NULL)
    {
        bExists = true;    
        (void) closedir (pDir);
    }

    return bExists;
}

int main()
{
  ofstream myfile;
  // myfile.open ("/home/tonghe2/fashionRecommendation/data/clean_brokenImgs/cleaner/results/broken_imgs.txt");  
  myfile.open ("/local2/home/tong/fashionRecommendation/data/clean_brokenImgs/cleaner/results/broken_imgs.txt");
  int corrupted_count=0;
  // const char* PATH = "/home/tonghe2/fashionRecommendation/data/clean_brokenImgs/cleaner/data"; 
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
        // const char* PATH_sub_temp = "/home/tonghe2/fashionRecommendation/data/clean_brokenImgs/cleaner/data/";
        const char* PATH_sub_temp = "/local2/home/tong/fashionRecommendation/data/Polyvore_large/1120_users/images/";
        // const char* savePath_temp = "/home/tonghe2/test/";
        const char* savePath_temp = "/local/tong/fashionRecommendation/data/images/";
        std::string temp2(PATH_sub_temp);
        std::string savePath_temp2(savePath_temp);
        temp2.append(entry->d_name);
        savePath_temp2.append(entry->d_name);

        if(DirectoryExists(savePath_temp2.c_str())==false)
        {
          const char* mkdir_temp0 = "mkdir ";
          std::string mkdir_temp1(mkdir_temp0);
          mkdir_temp1.append(savePath_temp);
          mkdir_temp1.append(entry->d_name);
          system(mkdir_temp1.c_str());
        }

        // const char* temp1 = "";
        const char* temp1 = "/items_append/full";
        temp2.append(temp1);
        const char* PATH_sub = temp2.c_str();

        //check is this user has items_append/
        if(DirectoryExists(PATH_sub)==true)
        {
          DIR *dir_sub = opendir(PATH_sub);
          const char* temp0 = "/";
          const char* savePath_temp3 = "/";
          temp2.append(temp0);
          savePath_temp2.append(savePath_temp3);
          PATH_sub = temp2.c_str();
          const char* savePath_temp4 = savePath_temp2.c_str();
          std::cout << PATH_sub << std::endl; //each user path
          struct dirent *entry_sub = readdir(dir_sub);
          while(entry_sub != NULL)
          {
            std::string invalid_sub(entry_sub->d_name);
            if(invalid_sub.compare(".")!=0 && invalid_sub.compare("..")!=0)
            {
              std::string temp3(PATH_sub);
              std::string savePath_temp5(savePath_temp4);

              temp3.append(entry_sub->d_name);
              savePath_temp5.append(entry_sub->d_name);
              const char* PATH_img = temp3.c_str(); //each item path of this user
              const char* savePath = savePath_temp5.c_str();
              cv::Mat im0 = cv::imread(PATH_img,CV_LOAD_IMAGE_COLOR);
              if(!im0.data)
              {
                corrupted_count++;
                printf("\n%s---%d\n", PATH_img, corrupted_count);
                myfile << PATH_img << "\n";
              }
              else
              {
                cv::Mat cv_img = cv::Mat(224,224,CV_8UC3,cv::Scalar(255,255,255));
                cv::Mat temp;

                //resize accoridng to the longer edge
                if(im0.cols < im0.rows){
                  //resize
                  cv::resize(im0, temp, cv::Size(floor(im0.cols*224/im0.rows), 224));             
                  //cropping
                  temp.copyTo(cv_img(cv::Rect(floor((224-temp.cols)/2),0,temp.cols,224)));
                }
                else{
                  //resize
                  cv::resize(im0, temp, cv::Size(224, floor(im0.rows*224/im0.cols)));
                  //cropping
                  temp.copyTo(cv_img(cv::Rect(0,floor((224-temp.rows)/2),224,temp.rows)));
                }

                //save the new img (or replace the old img)
                cv::imwrite(savePath,cv_img);
              }
            }
            entry_sub = readdir(dir_sub);
          }
          closedir(dir_sub);
        }
      }
    }         
    entry = readdir(dir);
  }
  closedir(dir);
  myfile.close();

  std::cout << std::endl;
  std::cout << "corrupted_count = " << corrupted_count << std::endl;
  std::cout << std::endl;

  cv::waitKey(0);
  return 0;
}
