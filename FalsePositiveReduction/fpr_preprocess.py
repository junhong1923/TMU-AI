import os
import numpy as np
import pandas as pd
import SimpleITK as sitk
from code_not_in_use import myPreproc as P
from glob import glob
import matplotlib.pyplot as plt
import time

# data_src = "/data/LIDC_Luna/LIDC_Luna/subset9_58/*"
data_src = "/data/LIDC_Luna/LIDC_Luna/train_543/*"
label_csv = "labelled.csv"
label_df = pd.read_csv(label_csv, index_col="suid")

dst = "/data/FPR_classifier/cube_64_v1/"

second = time.time()

j = 32
width = 50
fail_ls, s_ls = [], []
count_nodule = 0 # count total nodule numbers
for case_path in glob(data_src):
    # print(case_path)
    img_array, suid, origin, spacing = P.get_dicom_array_and_info(case_path)
    lungwin_array = P.lumTrans(img_array)
    img_re = P.resample(lungwin_array, spacing[::-1], mode='nearest', order=1)
    img_pad = np.pad(img_re, ((width,width),(width,width),(width,width)), mode='minimum')
    print(suid)
    print('Img shape', img_array.shape) # (194, 512, 512) (z, y, x)
    print('Resample Img shape', img_re.shape)
    print('Padding Img shape', img_pad.shape)
    print('Origin:', origin) # x,y,z
    print('Spacing:', spacing) # x,y,z

    save_folder = os.path.join(dst, suid)
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    pred_coord = label_df.loc[suid]
    if len(pred_coord) != 1:
        count = 0 # count predicted nodule in one suid
        for i in range(len(pred_coord)):
            pred_x, pred_y, pred_z = pred_coord["x"].iloc[i], pred_coord["y"].iloc[i], pred_coord["z"].iloc[i]
            c = pred_coord["class"].iloc[i]
            # print('Pred coord', pred_x, pred_y, pred_z, "Class:", c)
            voxelCoord = P.worldToVoxelCoord((pred_x, pred_y, pred_z), origin, spacing)
            # print('Voxel coord', voxelCoord) #  x, y, z

            # x_pad, y_pad, z_pad = int(pred_x + width), int(pred_y + width), int(pred_z + width)
            # cube = img_pad[z_pad-j:z_pad+j, y_pad-j:y_pad+j, x_pad-j:x_pad+j]

            # z1, z2 = int(voxelCoord[2])-j + width, int(voxelCoord[2])+j + width
            # x1, x2 = int(voxelCoord[0])-j + width, int(voxelCoord[0])+j + width
            # y1, y2 = int(voxelCoord[1])-j + width, int(voxelCoord[1])+j + width

            # z1, z2 = int(round(voxelCoord[2])-j + width), int(round(voxelCoord[2])+j + width)
            # x1, x2 = int(round(voxelCoord[0])-j + width), int(round(voxelCoord[0])+j + width)
            # y1, y2 = int(round(voxelCoord[1])-j + width), int(round(voxelCoord[1])+j + width)

            z1, z2 = int(round(voxelCoord[2])*spacing[2] -j + width), int(round(voxelCoord[2])*spacing[2] +j + width)
            x1, x2 = int(round(voxelCoord[0])*spacing[0] -j + width), int(round(voxelCoord[0])*spacing[0] +j + width)
            y1, y2 = int(round(voxelCoord[1])*spacing[1] -j + width), int(round(voxelCoord[1])*spacing[1] +j + width)

            cube = img_pad[z1:z2, y1:y2, x1:x2]


            # assert cube.shape == (2*j, 2*j, 2*j), cube.shape
            cube_fname = save_folder + "/cube_" + str(count) + "_" + str(c) + ".npy"
            if cube.shape == (2*j, 2*j, 2*j):

                if not os.path.exists(cube_fname):
                    # print(f"save cube npy -> {cube_fname}")
                    np.save(cube_fname, cube)
                    count_nodule += 1

            else:
                print(f"{cube_fname} has wrong shape:{cube.shape}")
                fail_ls.append(cube_fname)

            count += 1
            print("----------")
#             break
    else:
        s_ls.append(suid)

    print("-------------------------------------------")

#     break
end = time.time()
print("Taking ", (end - second)/60, " mins")
print("Total nodule detected:", count , "done cube count: ", count_nodule)
pd.DataFrame(fail_ls).to_csv("err_shape_ls.csv", index=False)
print('single nodule case: \n', s_ls)
print('error shape case: \n', fail_ls)
