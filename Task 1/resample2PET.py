"""
This file resamples CT and mask to PET dimension.
"""

import numpy as np
import pandas as pd
import os
join = os.path.join
import nibabel as nib
import scipy.ndimage
import shutil

def remove_DS_Store(path):
    if os.path.exists(join(path, '.DS_Store')):
        os.remove(join(path, '.DS_Store'))

label_path = 'path/to/labels'
img_path = 'path/to/images'
save_path = 'path/to/save'

remove_DS_Store(img_path)

for img_name in sorted(os.listdir(img_path)):
    if '_0000' in img_name:

        name = img_name.split('_0000')[0]

        pet_name = name + '_0001.nii.gz'
        pet_nii = nib.load(join(img_path, pet_name))
        pet = pet_nii.get_fdata()

        ct_nii = nib.load(join(img_path, img_name))
        ct = ct_nii.get_fdata()

        mask_name = name + '.nii.gz'
        mask_nii = nib.load(join(label_path, mask_name))
        mask = mask_nii.get_fdata()

        ct_factor = [pet.shape[0] / ct.shape[0], pet.shape[1] / ct.shape[1], pet.shape[2] / ct.shape[2]]
        mask_factor = [pet.shape[0] / mask.shape[0], pet.shape[1] / mask.shape[1], pet.shape[2] / mask.shape[2]]

        new_ct = scipy.ndimage.zoom(ct, ct_factor, order=3)
        new_mask = scipy.ndimage.zoom(mask, mask_factor, order=0)

        assert new_mask.shape == pet.shape
        assert new_ct.shape == pet.shape

        save_nii = nib.Nifti1Image(new_ct, pet_nii.affine, pet_nii.header)
        nib.save(save_nii, join(save_path, img_name))

        save_nii = nib.Nifti1Image(np.uint8(new_mask), pet_nii.affine, pet_nii.header)
        nib.save(save_nii, join(save_path, 'labelsTr', mask_name))

        shutil.copyfile(join(img_path, pet_name), join(save_path, pet_name))