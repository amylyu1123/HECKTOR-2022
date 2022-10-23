"""
This file merges primary tumor and lymph nodes into the same label.
"""

import os
import numpy as np
import nibabel as nib
join = os.path.join

root_path = 'path/to/labels'
save_path = 'path/to/save'

if os.path.exists(join(root_path, '.DS_Store')):
    os.remove(join(root_path, '.DS_Store'))

for contour_name in sorted(os.listdir(root_path)):
    mask_nii = nib.load(join(root_path, contour_name))
    mask = mask_nii.get_fdata()
    mask[mask == 2] = 1

    save_nii = nib.Nifti1Image(np.uint8(mask), mask_nii.affine, mask_nii.header)
    nib.save(save_nii, join(save_path, contour_name))