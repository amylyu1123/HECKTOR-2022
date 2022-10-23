"""
This file computes the C index.
"""

from lifelines.utils import concordance_index
import pandas as pd

endpoint_df = pd.read_csv('path/tp/hecktor2022_endpoint_training.csv')
data_df = pd.read_csv('path/to/prediction.csv')

df = pd.merge(data_df, endpoint_df, how='inner', on='PatientID')

event_indicator_ori = df['Relapse']
df['Relapse'] = df['Relapse'].map({1: True, 0: False}) 
event_indicator = df['Relapse']
events = df['RFS_true']

preds = df['RFS_pred']
print('C-index: ', concordance_index(events, preds, event_indicator_ori))

