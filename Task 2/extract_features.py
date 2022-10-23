"""
This file use Pyradiomics package to extract radiomics features from PET/CT with mask.
The code was modified from: https://github.com/AIM-Harvard/pyradiomics/blob/master/notebooks/PyRadiomicsExample.ipynb
"""

import os
import pandas as pd
join = os.path.join
from collections import OrderedDict

import radiomics
from radiomics import featureextractor  # This module is used for interaction with pyradiomics

imagePath = 'path/to/images'
maskPath = 'path/to/mask'

clinical_df = pd.read_csv('path/to/hecktor2022_clinical_info_training.csv')

ids = clinical_df['PatientID'].to_list()

data = []
result_df = None

# Instantiate the extractor
extractor = featureextractor.RadiomicsFeatureExtractor()

print('Extraction parameters:\n\t', extractor.settings)
print('Enabled filters:\n\t', extractor.enabledImagetypes)
print('Enabled features:\n\t', extractor.enabledFeatures)

for name in ids:
    labelPath = join(maskPath, name + '.nii.gz')
    ctPath = join(imagePath, name + '_0000.nii.gz')
    petPath = join(imagePath, name + '_0001.nii.gz')

    # print(name)
    ct_result = extractor.execute(ctPath, labelPath)
    pet_result = extractor.execute(petPath, labelPath)

    combined_result = OrderedDict()
    combined_result['PatientID'] = name

    if result_df is None:
        data.append('PatientID')
        for key in ct_result.keys():
            data.append('CT_' + key)
            data.append('PET_' + key)
        result_df = pd.DataFrame(columns=data)

    for key in ct_result.keys():
        combined_result['CT_' + key] = ct_result[key]
        combined_result['PET_' + key] = pet_result[key]

    result_df = result_df.append(combined_result, ignore_index=True)

result_df = pd.merge(result_df, clinical_df, how='inner', left_on='PatientID', right_on = 'PatientID')

result_df.to_csv('path/to/extracted_feature.csv', index=False, na_rep='NaN')