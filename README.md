[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1wpeflhLHrVXP5SOizE8hnaJfd02DQe0h?usp=sharing)

This is a fork of ultralytics' YOLOv3 repo, used for a project on pedestrian detection.
## Pretrained Checkpoints

[assets3]: https://github.com/ultralytics/yolov3/releases
[assets5]: https://github.com/ultralytics/yolov5/releases

Model |size<br><sup>(pixels) |mAP<sup>val<br>0.5:0.95 |mAP<sup>test<br>0.5:0.95 |mAP<sup>val<br>0.5 |Speed<br><sup>V100 (ms) | |params<br><sup>(M) |FLOPS<br><sup>640 (B)
---   |---                   |---                     |---                      |---                |---                     |---|---              |---
[YOLOv3-tiny][assets3] |640  |17.6     |17.6     |34.8     |**1.2** | |8.8   |13.2
[YOLOv3][assets3]      |640  |43.3     |43.3     |63.0     |4.1     | |61.9  |156.3
[YOLOv3-SPP][assets3]  |640  |44.3     |44.3     |64.6     |4.1     | |63.0  |157.1
| | | | | | || |
[YOLOv5l][assets5]     |640  |**48.2** |**48.2** |**66.9** |3.7     | |47.0  |115.4


<details>
  <summary>Table Notes (click to expand)</summary>
  
  * AP<sup>test</sup> denotes COCO [test-dev2017](http://cocodataset.org/#upload) server results, all other AP results denote val2017 accuracy.  
  * AP values are for single-model single-scale unless otherwise noted. **Reproduce mAP** by `python test.py --data coco.yaml --img 640 --conf 0.001 --iou 0.65`  
  * Speed<sub>GPU</sub> averaged over 5000 COCO val2017 images using a GCP [n1-standard-16](https://cloud.google.com/compute/docs/machine-types#n1_standard_machine_types) V100 instance, and includes FP16 inference, postprocessing and NMS. **Reproduce speed** by `python test.py --data coco.yaml --img 640 --conf 0.25 --iou 0.45`  
  * All checkpoints are trained to 300 epochs with default settings and hyperparameters (no autoaugmentation). 
</details>


## Requirements

```pip install PyYAML==5.4.1 wandb```


## Inference

`detect.py` runs inference on a variety of sources, downloading models automatically from the [latest YOLOv3 release](https://github.com/ultralytics/yolov3/releases) and saving results to `runs/detect`.
```bash
$ python detect.py --source 0  # webcam
                            file.jpg  # image 
                            file.mp4  # video
                            path/  # directory
                            path/*.jpg  # glob
                            'https://youtu.be/NUsoVlDFqZg'  # YouTube video
                            'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream
```

To run inference on example images in `data/images`:
```bash
$ python detect.py --source data/images --weights yolov3.pt --conf 0.25
```
<img width="500" src="https://user-images.githubusercontent.com/26833433/100375993-06b37900-300f-11eb-8d2d-5fc7b22fbfbd.jpg">  
  
# Model
model = torch.hub.load('ultralytics/yolov3', 'yolov3')  # or 'yolov3_spp', 'yolov3_tiny'

# Dataset

Run ``get_citypersons.sh``
Then, run ``make_citypersons_labels.py`` to generate label `.txt` files
# Image
img = 'https://ultralytics.com/images/zidane.jpg'

# Inference
results = model(img)
results.print()  # or .show(), .save()
```


## Training

Run commands below to reproduce results on [COCO](https://github.com/ultralytics/yolov3/blob/master/data/scripts/get_coco.sh) dataset (dataset auto-downloads on first use). Training times for YOLOv3/YOLOv3-SPP/YOLOv3-tiny are 6/6/2 days on a single V100 (multi-GPU times faster). Use the largest `--batch-size` your GPU allows (batch sizes shown for 16 GB devices).
```bash
$ python train.py --data coco.yaml --cfg yolov3.yaml      --weights '' --batch-size 24
                                         yolov3-spp.yaml                            24
                                         yolov3-tiny.yaml                           64
```
<img width="800" src="https://user-images.githubusercontent.com/26833433/100378028-af170c80-3012-11eb-8521-f0d2a8d021bc.png">


## Citation

[![DOI](https://zenodo.org/badge/146165888.svg)](https://zenodo.org/badge/latestdoi/146165888)


## Todo
  - [ ] Create test set

  - [ ] Run baseline model
  
  - [ ] Run experiments
