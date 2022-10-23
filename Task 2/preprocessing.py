"""
This file preprocesses the data from csv with extracted features.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

df = pd.read_csv('path/to/extracted_feature.csv')

gender = pd.get_dummies(df['Gender'])
df = pd.concat([df, gender], axis=1)
df = df.loc[df['Task 2'] == 1]
df = df.drop(['Gender', 'CenterID', 'Weight', 'Tobacco', 'Alcohol', 'Performance status', 'HPV status', 'Surgery', 'Task 1', 'Task 2'], axis=1)

# apply logarithm
columns = ['original_shape_MeshVolume', 'original_shape_SurfaceArea', 'original_shape_VoxelVolume', 'CT_original_firstorder_Energy', 
'PET_original_firstorder_Energy', 'CT_original_firstorder_TotalEnergy', 'PET_original_firstorder_TotalEnergy', 'CT_original_gldm_LargeDependenceHighGrayLevelEmphasis', 
'CT_original_glszm_LargeAreaEmphasis', 'PET_original_glszm_LargeAreaEmphasis', 'CT_original_glszm_LargeAreaHighGrayLevelEmphasis', 
'PET_original_glszm_LargeAreaHighGrayLevelEmphasis', 'PET_original_glszm_LargeAreaLowGrayLevelEmphasis', 'PET_original_glszm_ZoneVariance', 
'PET_original_ngtdm_Coarseness']
for column in columns:
    df[column] = np.log10(df[column].replace(0, np.nan)).replace(np.nan, 0)

# split the data: 80% training, 20% for testing
train, test = train_test_split(df, test_size=0.2, random_state=42)
y_train = train['RFS']
X_train = train.drop(['RFS', 'PatientID'], axis=1)

y_test = test['RFS']
X_test = test.drop(['RFS', 'PatientID'], axis=1)

# print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

train.to_csv('path/to/training_set.csv', index=False)
test.to_csv('path/to/test_set.csv', index=False)
