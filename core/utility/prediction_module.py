#set nnUNet_raw=../../datasets/CT_Data/CT/nnUNet_raw
#set nnUNet_preprocessed=../../datasets/CT_Data/CT/nnUNet_preprocessed
#set nnUNet_results=../../datasets/CT_Data/CT/nnUNet_results

#cmd /c set_environment_variables.bat

from nnunetv2.paths import nnUNet_results, nnUNet_raw
import torch
import os
from batchgenerators.utilities.file_and_folder_operations import join
from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor


def get_model_path(base_path: str):
    return nnUNet_results + "/" +base_path


def predict(input_file, output_file, model_path, checkpoint_name='checkpoint_best.pth', folds = 2):
    print("Starting predictions...")
    # if __name__ == '__main__':
        # instantiate the nnUNetPredictor
    predictor = nnUNetPredictor(
        tile_step_size=0.5,
        use_gaussian=True,
        use_mirroring=True,
        perform_everything_on_device=True,
        device=torch.device('cuda', 0),
        verbose=False,
        verbose_preprocessing=False,
        allow_tqdm=True
    )

    # initializes the network architecture, loads the checkpoint
    predictor.initialize_from_trained_model_folder(
        model_path,
        use_folds=(folds,),
        checkpoint_name=checkpoint_name,
    )

    print("nnUNet model is initialized")
    # variant 2, use list of files as inputs. Note how we use nested lists!!!
    predictor.predict_from_files([[input_file]],
                            [output_file],
                            num_processes_preprocessing=1,
                            num_processes_segmentation_export=1,)
    print("Prediction completed...")


# if __name__ == '__main__':
# input_file = '../../CT Segmentation/nnUNet/test/test/la_015_0000.nii.gz'
# output_file = '../../CT Segmentation/nnUNet/test/test/predict/la_015_0000_pred.nii.gz'
# print(os.listdir("../../data"))
# input_file = '../../data/user2-SE00001_AHFP_Hjerte_20221130172341_14_phb/org-user2-SE00001_AHFP_Hjerte_20221130172341_14_phb.nii.gz'
# output_file = '../../data/user2-SE00001_AHFP_Hjerte_20221130172341_14_phb/seg-user2-SE00001_AHFP_Hjerte_20221130172341_14_phb.nii.gz'
# model_path = nnUNet_results + '/Dataset004_Heart/nnUNetTrainer__nnUNetPlans__2d'
# folds = 2
# checkpoint_name='checkpoint_best.pth'

# predict(input_file, output_file, model_path, checkpoint_name, folds)
# 