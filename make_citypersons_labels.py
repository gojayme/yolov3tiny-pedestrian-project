import os

from scipy import io as scio
import numpy as np
import cv2

root_dir = 'yolov3/data/citypersons/leftImg8bit/'
all_img_path = os.path.join(root_dir)
# all_anno_path = os.path.join(root_dir, 'annotations')
types = ['train','val']
rows, cols = 1024, 2048
image_datas = {}
for t in types:
  # anno_path = os.path.join(all_anno_path, 'anno_'+t+'.mat')
  anno_path = os.path.join('yolov3/data/citypersons/annotations/anno_' +t+'.mat')
  image_data = []
  annos = scio.loadmat(anno_path)
  index = 'anno_'+t+'_aligned'
  valid_count = 0
  iggt_count = 0
  box_count = 0
  for l in range(len(annos[index][0])):
    anno = annos[index][0][l]
    cityname = anno[0][0][0][0]
    imgname = anno[0][0][1][0]
    gts = anno[0][0][2]
    # img_path = os.path.join(all_img_path,t + '/'+ cityname+'/'+imgname)
    img_path = os.path.join(all_img_path,t + '/' +imgname)
    img_name = imgname
    boxes = []
    ig_boxes = []
    vis_boxes = []
    for i in range(len(gts)):
      label, x1, y1, w, h = gts[i, :5]
      x1, y1 = max(int(x1), 0), max(int(y1), 0)
      w, h = min(int(w), cols - x1 -1), min(int(h), rows - y1 -1)
      xv1, yv1, wv, hv = gts[i, 6:]
      xv1, yv1 = max(int(xv1), 0), max(int(yv1), 0)
      wv, hv = min(int(wv), cols - xv1 - 1), min(int(hv), rows - yv1 - 1)

      if label == 1 and h>=50:
        box = np.array([int(x1), int(y1), int(x1)+int(w), int(y1)+int(h)])
        boxes.append(box)
        vis_box = np.array([int(xv1), int(yv1), int(xv1)+int(wv), int(yv1)+int(hv)])
        vis_boxes.append(vis_box)
      else:
        ig_box = np.array([int(x1), int(y1), int(x1)+int(w), int(y1)+int(h)])
        ig_boxes.append(ig_box)
    boxes = np.array(boxes)
    vis_boxes = np.array(vis_boxes)
    ig_boxes = np.array(ig_boxes)

    if len(boxes)>0:
      valid_count += 1
    annotation = {}
    annotation['filepath'] = img_path
    box_count += len(boxes)
    iggt_count += len(ig_boxes)
    annotation['bboxes'] = boxes
    annotation['vis_bboxes'] = vis_boxes
    annotation['ignoreareas'] = ig_boxes
    annotation['img_name'] = img_name
    image_data.append(annotation)
  image_datas[t] = image_data
def convert(size, box):
  ''' box[0] is x min
      box[1] is y min
      box[2] is x max
      box[3] is y max '''
  dw = 1./(size[1])
  dh = 1./(size[0])
  
  x_min,y_min,x_max,y_max = box
  x_center = (x_min + x_max)/2.0
  y_center = (y_min + y_max)/2.0
  width = x_max - x_min
  height = y_max - y_min
  x_center = (x_center)*dw
  y_center = (y_center)*dh
  #x_center = (x_center-1)*dw
  #y_center = (y_center-1)*dh
  width = width*dw
  height = height*dh
  return (x_center,y_center,width,height)


for t,image_data in image_datas.items():
  for d in image_data:
    boxes = d['vis_bboxes']
    image = cv2.imread(d['filepath'])
    txtfile = open(f"yolov3/data/citypersons/leftImg8bit/{t}/{d['img_name'][:-4]}.txt",mode='w')
    for box in boxes:
      x,y,w,h = convert(image.shape,box)
      txtfile.write(' '.join(['0', str(x), str(y), str(w), str(h)]) + '\n')
    txtfile.close()