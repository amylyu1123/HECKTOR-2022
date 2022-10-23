"""
This file renames PET/CT images to match the name convention used for nnU-Net.
"""

import os
join = os.path.join

root_path = "path/to/images"

if os.path.exists(join(root_path, '.DS_Store')):
    os.remove(join(root_path, '.DS_Store'))

for img in os.listdir(root_path):
    if 'CT' in img:
        name = img.split('_CT')[0]
        os.rename(join(root_path, img), join(root_path, name + '0000.nii.gz'))
    elif 'PT' in img:
        name = img.split('_PT')[0]
        os.rename(join(root_path, img), join(root_path, name + '0001.nii.gz'))