This repo contains code used for HECKTOR 2022 (https://hecktor.grand-challenge.org/Overview/). 

Datasets are from https://hecktor.grand-challenge.org/Data/.

## Task 1

- Run *resample2PET.py* to convert CT images and masks to the same dimension of PET images
- Run *rename_image.py* to rename PET/CT images to match the name convention for nnU-Net input data
- Clone the nnU-Net repo https://github.com/MIC-DKFZ/nnUNet.git
- Preprocessing and train 3D full resolution U-Net models using nnUNetTrainerV2_Loss_DiceTopK10 as TRAINER_CLASS_NAME for 5 folds (following the steps: https://github.com/MIC-DKFZ/nnUNet#usage)
- Run inference for 5 folds (include --save_npz)
- Run ensembling
- Run *resample2CT.py* to convert segmentation to CT dimension
- Run *compute_agg_dsc.py* to calculate the aggregated DSC

## Task 2

- Run *merge.py* to merge primary tumor and lymph nodes into the same label
- Run *extract_features.py* to extract radiomics features from PET/CT images and mask, and merge with the clinical information
- Run *preprocessing.py* to preprocess the data by dropping certain features, applying logarithm, randomly splitting into training and test set
- Run *autogulon_predict.py* to train models and make prediction of RFS
- Run *compute_c_index.py* to compute the C index
