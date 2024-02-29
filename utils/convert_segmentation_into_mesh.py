import os
import sys
import argparse
import glob

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description="Convert a segmentation of type .nii.gz into a mesh of type obj with ImFusion workspace")

    arg_parser.add_argument(
        "--root_path_vertebrae",
        required=True,
        dest="root_path_vertebrae",
        help="Root path of the vertebrae folders"
    )

    arg_parser.add_argument(
        "--list_file_names",
        required=True,
        dest="txt_file",
        help="Txt file that contains all spines that contain all lumbar vertebrae"
    )

    args = arg_parser.parse_args()

    # iterate over spine IDS
    with open(args.txt_file) as file:
        spine_ids = [line.strip() for line in file]

    placeholders = ['Name', 'PathToFile', 'PathToSave']
    for spine_id in spine_ids:

        # get the paths for the segmentations of all vertebrae belonging to this spine
        unique_identifier = "*/**" + str(spine_id) + "*_msk*" + ".nii.gz"
        vert_segm_paths = sorted(glob.glob(os.path.join(args.root_path_vertebrae, unique_identifier), recursive=True))
        workspace_file_segm_to_mesh = "imfusion_workspaces/segmentation_to_mesh.iws"
        for vert_segm_path in vert_segm_paths:
            arguments_imfusion = ""
            base = os.getcwd()
            for p in placeholders:

                if p == 'PathToFile':
                    value = os.path.join(base,vert_segm_path)

                if p == 'Name':
                    vert_segm_name = os.path.basename(vert_segm_path)
                    value =vert_segm_name [:vert_segm_name.find('.nii.gz')]

                if p == 'PathToSave':
                    value = os.path.join(base,vert_segm_path.replace('.nii.gz','_msh.obj'))

                arguments_imfusion += p + "=" + value + " "

            print('ARGUMENTS: ', arguments_imfusion)
            os.system("ImFusionConsole" + " " + workspace_file_segm_to_mesh + " " + arguments_imfusion)
            print('################################################### ')





