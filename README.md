# convert the format of the [caltech pedestrian dataset](http://www.vision.caltech.edu/Image_Datasets/CaltechPedestrians) to the format that [yolo](https://pjreddie.com/darknet/yolo) uses

This repo is a mix of
- https://github.com/mitmul/caltech-pedestrian-dataset-converter
- https://pjreddie.com/media/files/voc_label.py

## dependencies

- opencv
- numpy
- scipy

## how to

1. Convert the `.seq` video files to `.png` frames by running `$ python generate-images.py`. They will end up in the `images` folder.
3. Squared images work better, which is why you can convert the 640x480 frames to 640x640 frames by running `$ python squarify-images.py`
3. Convert the `.vbb` annotation files to `.txt` files by running `$ python generate-annotation.py`. It will create the `labels` folder that contains the `.txt` files named like the frames and the `train.txt` and `test.txt` files that contain the paths to the images.
4. Adjust `.data` yolo file
5. Adjust `.cfg` yolo file: take e.g. `yolo-voc.2.0.cfg` and set `height = 640`, `width = 640`, `classes = 2`, and in the final layer `filters = 35` ([`= (classes + 5) * 5)`](https://github.com/AlexeyAB/darknet))

## folder structure
```
|- caltech
|-- annotations
|-- test06
|--- V000.seq
|--- ...
|-- ...
|-- train00
|-- ...
|- caltech-for-yolo (this repo, cd)
|-- generate-images.py
|-- generate-annotation.py
|-- images
|-- labels
|-- test.txt
|-- train.txt
```
