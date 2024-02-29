# DataGeneration_VertShapeCompletion
This repository implements the synthetic data generation pipeline described in the paper "Shape Completion in the Dark:Completing Vertebrae Morphology from 3D Ultrasound"
published at IPCAI 2024.

## Install and Download
1. Install python requirements
   1. Install Anaconda 
   2. Create environment and activate it 
   ```
    conda create -n synthDataGen python=3.9
    conda activate synthDataGen
    pip install -r requirements.txt
   ```
2. Download the VerSe20 dataset: https://osf.io/t98fz/
3. Make sure you have ImFusion 

##  Usage

3. Preprocess VerSe20 by
   1. Finding all datasets that have lumbar vertebrae:
   ```
    python utils/get_spines_lumbar_vertebrae.py --root_path_spines sample_data/spines --list_file_names sample_data/spines/lumbar_spines.txt
   ```
   2. Separating the .nii.gz files of a whole spines into segmentations of vertebrae 
   ```
    python utils/separate_spine_into_vertebrae.py --list_file_names sample_data/spines/lumbar_spines.txt --root_path_vertebrae sample_data/vertebrae --root_path_spines sample_data/spines
   ```
   3. Generate meshes of the spine segmentations and of the vertebrae segmentations 
   ```
   python utils/convert_segmentation_into_mesh.py ----root_path_vertebrae sample_data/vertebrae --list_file_names sample_data/spines/lumbar_spines.txt
   ```
4. Apply the synthetic data generation pipeline 
    Note: if you want to work with different curvatures of the spines, use the data augmentation 
    through deformation showcased here: https://github.com/miruna20/DataGeneration_CT-US-Registration/tree/main/SpineDeformation
    ```
    cd polluted_pcds_generation
    python 00_polluted_pcds_pipeline.py with the corresponding flags 
    ```

## Inputs and prerequisites
- The folder structure must be as follows 
    - root_path_spines directory:
        <root_path_spines>/<spine_id>/ folders are already created for each spine id
    - root_path_vertebrae:
        <root_path_vertebrae>/<spine_id>/<spine_id>*_msh.obj --> mesh files of individual vertebrae are used for deformation
        --> to separate spine segmentations(e.g from VerSe2020 dataset) into vertebrae segmentations and transform segmentation to mesh check 
            - utils/separate_spine_into_vertebrae.py
            - utils/convert_segmentation_into_mesh.py

## Pipeline steps              
Pipeline steps for one spine and it's corresponding vertebrae (can be previously deformed)

For deformation computation please check: https://github.com/miruna20/DataGeneration_CT-US-Registration/tree/main/SpineDeformation

1. Shift initial spine, merge shifted with original 
        => initial spine, shifted spine, merged spine 
2. Raycast each of the above spines from 3 camera positions which will be above the spinous
processes of L1, L2, L3, L4, L5. For each spine merge the 5 obtained pcds
    - for this we need the exact camera poses from which we will raycast
    => raycasted pcd initial spine, raycasted pcd shifted spine, raycasted pcd merged spine 
3. Account for US artefacts by loading all 3 prev obtained pcds and removing the shadowing 
obtained by overlapping of the shifted on the initial 
    => shadowed pcd

