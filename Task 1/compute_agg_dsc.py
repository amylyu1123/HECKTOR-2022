"""
This file computes aggregated DSC.
"""

import numpy as np
import os
join = os.path.join
import nibabel as nib
from collections import OrderedDict

def remove_DS_Store(path):
    if os.path.exists(join(path, '.DS_Store')):
        os.remove(join(path, '.DS_Store'))

result_path = 'path/to/segmentation'
refer_path = 'path/to/labels'

remove_DS_Store(result_path)
remove_DS_Store(refer_path)

label_tolerance = OrderedDict({'GTVp': 1, 'GTVn': 2})

results = sorted(os.listdir(result_path))
references = sorted(os.listdir(refer_path))

agg_dsc = []

for i in range(1, 3):
    numerator, denominator = None, None

    for contour_name in results:
        result_nii = nib.load(join(result_path, contour_name))
        result_arr = result_nii.get_fdata()

        refer_nii = nib.load(join(refer_path, contour_name))
        refer_arr = refer_nii.get_fdata()

        organ_arr_result = np.where(result_arr == i, 1, 0)
        organ_arr_refer = np.where(refer_arr == i, 1, 0)

        curr_numerator = np.sum(np.multiply(organ_arr_result, organ_arr_refer))
        curr_denominator = np.sum(organ_arr_result + organ_arr_refer)

        if numerator is None:
            numerator = curr_numerator
            denominator = curr_denominator
        else:
            numerator += curr_numerator
            denominator += curr_denominator

    agg_dsc.append(2 * numerator / denominator)

print("agg_dsc_GTVp: " + str(agg_dsc[0]))
print("agg_dsc_GTVn: " + str(agg_dsc[1]))
print("average: " + str((agg_dsc[0] + agg_dsc[1]) / 2))
