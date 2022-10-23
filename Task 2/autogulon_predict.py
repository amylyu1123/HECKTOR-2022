"""
This file trains the model and makes prediction using autugluon.tabular: https://auto.gluon.ai/stable/tutorials/tabular_prediction/tabular-quickstart.html

"""

from autogluon.tabular import TabularDataset, TabularPredictor
import pandas as pd
import autogluon.core as ag

train_data = TabularDataset('path/to/training_set.csv')
test_data = TabularDataset('path/to/test_set.csv')
id, label = 'PatientID', 'RFS'

predictor = TabularPredictor(label=label, eval_metric='mean_absolute_percentage_error').fit(train_data.drop(columns=[id]), 
                                                                                            presets='best_quality', 
                                                                                            auto_stack=True)

preds = predictor.predict(test_data.drop(columns=[id]))
result = pd.DataFrame({id:test_data[id], label:preds})

perf = predictor.evaluate_predictions(y_true=test_data[label], y_pred=preds, auxiliary_metrics=True)
predictor.fit_summary()
predictor.feature_importance(data=train_data)
predictor.leaderboard(test_data, silent=True)

result = pd.DataFrame({'PatientID': test_data['PatientID'], 'RFS_true': test_data['RFS'], 'RFS_pred': preds})
result.to_csv('path/to/prediction.csv', index=False)