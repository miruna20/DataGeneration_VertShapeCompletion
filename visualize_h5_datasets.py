import numpy as np
import h5py
import open3d as o3d
import math
import argparse

if __name__ == "__main__":

    # example setup
    # lumbar vertebrae from verse2020 training samples
    # inputs_inference = "/home/miruna20/Documents/Thesis/Dataset/VerSe2020/vertebrae_train_lumbar.h5"
    # results_inference_path = "/home/miruna20/Documents/Thesis/Code/VRCNet/lumbar_vertebrae_verse2020_dataset/training_dataset/results.h5"
    # nr_partial_pcds_per_sample = 16

    arg_parser = argparse.ArgumentParser(description="Visualize the input dataset and the predicted completions")
    arg_parser.add_argument(
        "--path_input_dataset",
        required=True,
        dest="path_input_dataset",
        help="Path to the input dataset e.g /home/miruna20/Documents/Thesis/Dataset/VerSe2020"
             "/vertebrae_test_lumbar_subsample.h5 This is usually the testing dataset, since we use it for testing "
             "and would like to visualize the results on it. "
    )
    arg_parser.add_argument(
        "--path_result_dataset",
        required=False,
        dest="path_result_dataset",
        help="Path to the results dataset e.g /home/miruna20/Documents/Thesis/Dataset/VerSe2020"
             "/vertebrae_test_lumbar_subsample.h5 This contains the completion point clouds predicted by the network. "
    )

    arg_parser.add_argument(
        "--nr_partial_pcds_per_sample",
        required=True,
        dest="nr_partial_pcds_per_sample",
        help="Number of partial point clouds per sample. This should correspond to the number that has been generated "
             "by the rendering script "
    )
    arg_parser.add_argument(
        "--sequential_visualization",
        action="store_true",
        help="Visualize the 3 point clouds (partial pc, completion, gt) one after the other (sequentially). Otherwise "
             "visualize them in one view "
    )

    args = arg_parser.parse_args()

    # read input dataset
    inputs_inference = h5py.File(args.path_input_dataset, 'r')
    complete_pcds = np.array(inputs_inference['complete_pcds'][()])
    incomplete_pcds = np.array(inputs_inference['incomplete_pcds'][()])
    labels = np.array(inputs_inference['labels'][()])
    number_samples_per_class = np.array(inputs_inference['number_per_class'])
    datasets_ids = np.array(inputs_inference['datasets_ids'])

    print("Shape of complete pcds: " + str(complete_pcds.shape))
    print("Shape of incomplete pcds: " + str(incomplete_pcds.shape))
    print("Number of samples per class: " + str(number_samples_per_class))

    # if results are available also read the results dataset
    emd_flag = False
    if (args.path_result_dataset != None):
        results = h5py.File(args.path_result_dataset, 'r')

        results_array = np.array(results['results'][()])

        # get metrics
        factor = 10000
        try:
            emd = np.array(results['emd'][()])
            emd_arch = np.array(results['emd_arch'][()])
            emd_flag = True
        except:
            print("No emd available for this dataset")
        cd_t = np.array(results['cd_t'][()])
        cd_t_arch = np.array(results['cd_t_arch'][()])
        cd_p = np.array(results['cd_p'][()])
        cd_p_arch = np.array(results['cd_p_arch'][()])
        f1 = np.array(results['f1'][()])
        f1_arch = np.array(results['f1_arch'][()])

        if (emd_flag):
            print("Average emd: " + str(np.average(emd) * factor))
            print("Average emd for the arch : " + str(np.average(emd_arch) * factor))
        print("Average cd_t: " + str(np.average(cd_t) * factor))
        print("Average cd_t_arch: " + str(np.average(cd_t_arch) * factor))
        print("Average cd_p: " + str(np.average(cd_p) * factor))
        print("Average cd_p_arch: " + str(np.average(cd_p_arch) * factor))
        print("Average f1: " + str(np.average(f1)))
        print("Average f1_arch: " + str(np.average(f1_arch)))

    step = 1
    for i in range(0, incomplete_pcds.shape[0], step):

        pc_partial = o3d.geometry.PointCloud()
        pc_partial.points = o3d.utility.Vector3dVector(incomplete_pcds[i])

        pc_gt = o3d.geometry.PointCloud()
        pc_gt.points = o3d.utility.Vector3dVector(complete_pcds[math.floor(i / int(args.nr_partial_pcds_per_sample))])

        # from the results
        if (args.path_result_dataset != None):
            print("Visualizing: " + str(datasets_ids[i]) + " red: partial pcd, blue: gt pcd, green: completed pcd")
            print("index: " + str(i) + ", label: " + str(labels[i]))
            if (emd_flag):
                print("emd:" + str(emd[i] * factor))
                print("emd_arch:"  + str(emd_arch[i] * factor))
            print("cd_t:" + str(cd_t[i] * factor))
            print("cd_t_arch:" + str(cd_t_arch[i] * factor))
            #print("cd_p:" + str(cd_p[i] * factor))
            #print("cd_p_arch:" + str(cd_p_arch[i] * factor))
            print("f1:" + str(f1[i]))
            #print("f1_arch:" + str(f1_arch[i]))

            pc_result = o3d.geometry.PointCloud()
            pc_result.points = o3d.utility.Vector3dVector(results_array[i])

        pc_partial.paint_uniform_color([1, 0, 0])
        pc_gt.paint_uniform_color([0, 1, 0])
        coord_sys = o3d.geometry.TriangleMesh.create_coordinate_frame()

        if (args.path_result_dataset != None):
            pc_result.paint_uniform_color([0, 0, 1])
            coord_sys = o3d.geometry.TriangleMesh.create_coordinate_frame()
            o3d.visualization.draw_geometries([pc_partial,pc_gt,pc_result])

        else:
            print("Visualizing: " + str(datasets_ids[i]) + " red: partial pcd, blue: complete pcd")
            #print(str(datasets_ids[i]))
            o3d.visualization.draw_geometries([pc_partial, pc_gt])
