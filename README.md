# yolov5-dataset-class-merger
This tool modifies a dataset in YOLO V5 format by merging multiple classes into a single class. This can be useful when using a specific dataset for a more generic task. 
For example: a dataset that contains annotations for left hand, right hand, but we only care about a hand

# How to use
Modify the script parameters at the top of main.py

- Current class names:
```
original_names = ['myleft', 'myright', 'yourleft', 'yourright']
```

- The name mapping that you wish to perform on the dataset (each existing class name, and the corresponding new name in the converted dataset):
```
name_mapping = {'myleft': 'left', 'myright': 'right', 'yourleft': 'left', 'yourright': 'right'}
```

- Existing dataset's root folder
```
dataset_root = '/data/home/usr/datasets/dataset1'
```

- New dataset root folder (must not exist!)
```
new_dataset_root = '/data/home/usr/datasets/dataset1_2classes'
```
