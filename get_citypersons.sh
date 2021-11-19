
mkdir data/citypersons
wget --keep-session-cookies --save-cookies=cookies.txt --post-data 'username=ppp12354&password=Cityscapes1@&submit=Login' https://www.cityscapes-dataset.com/login/
wget --load-cookies cookies.txt --content-disposition https://www.cityscapes-dataset.com/file-handling/?packageID=3
unzip leftImg8bit_trainvaltest.zip -d data/citypersons
rm leftImg8bit_trainvaltest.zip
git clone https://github.com/CharlesShang/Detectron-PYTORCH.git
cp -r Detectron-PYTORCH/data/citypersons/annotations data/citypersons/annotations
rm -rf Detectron-PYTORCH
mv data/citypersons/leftImg8bit/val/*/* data/citypersons/leftImg8bit/val/
mv data/citypersons/leftImg8bit/test/*/* data/citypersons/leftImg8bit/test/
mv data/citypersons/leftImg8bit/train/*/* data/citypersons/leftImg8bit/train/
mkdir data/citypersons/leftImg8bit/train/labels data/citypersons/leftImg8bit/val/labels /content/yolov3/data/citypersons/leftImg8bit/test/labels