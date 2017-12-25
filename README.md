# convert the format of the [caltech pedestrian dataset](http://www.vision.caltech.edu/Image_Datasets/CaltechPedestrians) to the format that [yolo](https://pjreddie.com/darknet/yolo) understands

1. Convert the `.seq` video files to `.png` frames by running `$ python convert_seqs.py` with [convert_seqs.py](https://github.com/mitmul/caltech-pedestrian-dataset-converter/blob/master/scripts/convert_seqs.py). You should end up with an images folder containing all the video frames and they follow the naming convention `(train|test)[0-9]+_V[0-9]+_[0-9]+`.
2. Convert the `.vbb` annotation files to a `.json` file by running `$ python convert_annotations.py` with [convert_annotations.py](https://github.com/mitmul/caltech-pedestrian-dataset-converter/blob/master/scripts/convert_annotations.py). The json has the following structure:
```js
{
    "set00": {
        "V000": {
            "frames": {
                "0": [
                    "pos": [x, y, w, h],
                    "lbl": "LABELNAME",
                    ...
                ],
                ...
            },
            ...
        },
        ...
    },
    ...
}
```
3. Run `$ python generate-annotations-for-yolo.py` from this repo. It iterates over the images, parses their names to take the according information from the annotations.json file, creates a `labels` folder with a text file for each image containing a line for each ground truth object and `train.txt` and `test.txt` files with the paths to the images.
4. TODO: how to adjust `.data` and `.cfg` yolo files
