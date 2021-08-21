
import csv
import glob
import os
from tqdm import tqdm
from shutil import copy
import time



# script parameters
original_names = ['myleft', 'myright', 'yourleft', 'yourright']
name_mapping = {'myleft': 'left', 'myright': 'right', 'yourleft': 'left', 'yourright': 'right'}
dataset_root = '/data/home/bedward/hand-detection/datasets/egohands_2classes'
new_dataset_root = '/data/home/bedward/hand-detection/datasets/egohands_2classes_converted'

# script code
def create_mapping_from_names(names):
    mapping = dict([(name, str(index)) for index, name in enumerate(names)])
    return mapping

def create_index_mapping(original_names, name_mapping):
    print(f"original names: {original_names}")
    original_mapping = create_mapping_from_names(original_names)
    print(f"original mapping: {original_mapping}")
    print(f"name mapping: {name_mapping}")
    new_names = sorted(list(set([name for name in name_mapping.values()])))
    print(f"new names: {new_names}")
    new_mapping = create_mapping_from_names(new_names)
    print(f"new mapping: {new_mapping}")
    old_index_to_new_index = dict([(original_mapping[old_name], new_mapping[new_name]) for old_name, new_name in name_mapping.items()])
    print(f"old index to new index: {old_index_to_new_index}")
    return new_names, old_index_to_new_index

def convert_label(old_path, new_dir, index_mapping):
    new_lines = []
    with open(old_path, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=' ')
        for label in reader:
            # print(f"old label: {label}")
            old_index = label[0]
            new_index = index_mapping[old_index]
            label[0] = new_index
            # print(f"new label: {label}")
            new_lines.append(' '.join(label))
        
    label_name = old_path.split(os.path.sep)[-1]
    new_path = os.path.join(new_dir, label_name)
    with open(new_path, 'w') as f:
        for index, line in enumerate(new_lines):
            if index != len(new_lines)-1:
                line = line+'\n'
            f.write(line)
        # print(new_lines)
            
def get_labels_in_dir(dir_path):
    return glob.glob(f"{dir_path}/*.txt")

def get_images_in_dir(dir_path):
    return glob.glob(f"{dir_path}/*.jpg")

def gather_data_folders(root):
    folders = []
    if os.path.isdir(os.path.join(root, 'train')):
        folders.append('train')
    if os.path.isdir(os.path.join(root, 'valid')):
        folders.append('valid')
    if os.path.isdir(os.path.join(root, 'test')):
        folders.append('test')
    print(f"data folders: {folders}")
    return folders
    
def convert_folder(root, new_root, folder, index_mapping):
    print(f"converting {folder}")
    os.mkdir(os.path.join(new_root, folder))
    old_images_dir = os.path.join(root, folder, 'images')
    new_images_dir = os.path.join(new_root, folder, 'images')
    os.mkdir(new_images_dir)
    print(f"copying images...")
    for image in tqdm(get_images_in_dir(old_images_dir)):
        copy(image, new_images_dir)

    print(f"converting labels...")
    old_labels_dir = os.path.join(root, folder, 'labels')
    new_labels_dir = os.path.join(new_root, folder, 'labels')
    os.mkdir(new_labels_dir)
    for label in tqdm(get_labels_in_dir(old_labels_dir)):
        convert_label(old_path=label, new_dir=new_labels_dir, index_mapping=index_mapping)
        
    print(f"done converting {folder}")
    
def export_summary(new_root, data_folders, new_names):
    print(f"writing data.yaml")
    with open(os.path.join(new_root, 'data.yaml'), 'w') as f:
        for data_folder in data_folders:
            f.write(f'{data_folder}: ./{data_folder}/images\n')
        f.write('\n')
        f.write(f'nc: {len(new_names)}\n')
        f.write(f'names: {new_names}')

def convert(root, new_root, original_names, name_mapping):
    started = time.time()
    if os.path.isdir(new_root):
        print(f"failure: new root already exists!")
        return
    os.mkdir(new_root)
    data_folders = gather_data_folders(root)

    new_names, index_mapping = create_index_mapping(original_names, name_mapping)

    for folder in data_folders:
        convert_folder(root, new_root, folder, index_mapping)

    export_summary(new_root, data_folders, new_names)
    print(f"done converting dataset in {time.time() - started} seconds")
    

convert(root=dataset_root, new_root=new_dataset_root, original_names=original_names, name_mapping=name_mapping)