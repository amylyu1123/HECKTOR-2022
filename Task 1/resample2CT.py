"""
This file resamples segmentation to CT dimension.
"""

import numpy as np
import os
join = os.path.join
import nibabel as nib
import scipy.ndimage

def remove_DS_Store(path):
    if os.path.exists(join(path, '.DS_Store')):
        os.remove(join(path, '.DS_Store'))

seg_path = 'path/to/segmentation'
img_path = 'path/to/images'
save_path = 'path/to/save'

remove_DS_Store(seg_path)

for mask_name in sorted(os.listdir(seg_path)):
    ct_name = mask_name.split('.nii.gz')[0] + '_0000.nii.gz'

    ct_nii = nib.load(join(img_path, ct_name))
    ct = ct_nii.get_fdata()

    mask_nii = nib.load(join(seg_path, mask_name))
    mask = mask_nii.get_fdata()

    mask_factor = [ct.shape[0] / mask.shape[0], ct.shape[1] / mask.shape[1], ct.shape[2] / mask.shape[2]]
    new_mask = scipy.ndimage.zoom(mask, mask_factor, order=0)

    assert new_mask.shape == ct.shape

    save_nii = nib.Nifti1Image(np.uint8(new_mask), ct_nii.affine, ct_nii.header)
    nib.save(save_nii, join(save_path, mask_name))

