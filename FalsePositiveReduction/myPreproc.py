import os
import numpy as np
import scipy.io as sio
import SimpleITK as sitk
# import matplotlib.pyplot as plt
from scipy import ndimage, misc
from scipy.ndimage.interpolation import zoom

def func_ROIMat2Numpy(file_name):
    data = sio.loadmat(file_name)
    row, col, slice = \
    data['Data_roi']['row'][0][0][0][0], data['Data_roi']['col'][0][0][0][0], data['Data_roi']['slicenum'][0][0][0][0]
    mask_proc = np.zeros((row, col, slice))
    mask = data['Data_roi']['roiimageMask'][0][0][0]
    # 將有標記內容的 layer 填入對應的位置    
    for i in range(len(mask)):
        if len(mask[i]) > 0:  
            if len(mask[i][0]) > 0:
                temp_mask = mask[i][0][0]                
                # temp_mask[temp_mask != 0] = 1   
                # 需要這樣加工才行@@
                temp_mask = np.rot90(temp_mask)                
                temp_mask = np.flip(temp_mask, axis=1)
                temp_mask = np.flip(temp_mask, axis=0)
                mask_proc[:, :, i] = temp_mask
    return mask_proc

def func_Numpy2Nifti(data, file_name, affine=None):
    if not affine:
        img = nib.Nifti1Image(data, affine)
    else:
        img = nib.Nifti1Image(data, np.eye(4))
    nib.save(img, file_name)

def load_deep_seed_npy(npy_src, suid): # 讀取deepseed產生的npy
    ori_npy_path = npy_src + '\\' + str(suid) + '_origin.npy'
    ori_npy = np.load(ori_npy_path) # z,x,y
    spacing_npy_path = npy_src + '\\' + str(suid) + '_spacing.npy'
    spacing_npy = np.load(spacing_npy_path)
    return ori_npy, spacing_npy

def imgs_swap(imgs): #轉換軸
    imgs_swap1 = imgs.swapaxes(0,2)
    imgs_swap2 = imgs_swap1.swapaxes(1,2)
    return imgs_swap2

def resample(imgs, spacing_npy, mode='nearest', order=0):
    new_spacing = resolution = np.array([1,1,1])
    new_shape = np.round(imgs.shape * spacing_npy / new_spacing)
    true_spacing = spacing_npy * imgs.shape / new_shape # 目前沒用到這個變數
    resize_factor = new_shape / imgs.shape
#     imgs = zoom(imgs, resize_factor, mode='nearest', order=1 # deepseed預設
    imgs = zoom(imgs, resize_factor, mode=mode, order=order) # 換成img用order1、mask用order0
    return imgs

def func_LoadSeriesDCM(path):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(path) # Hu correction will be automatically done
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    dcm = sitk.GetArrayFromImage(image)
    return dcm

def get_dicom_array_and_info(path):
    """  honghu version 
    note: shape of sitk img: (z, y, x)
    """
    series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(path)
    if not series_IDs:
        raise IOError("ERROR: given directory \"" + path + "\" does not contain a DICOM series.")

    series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(path, series_IDs[0])

    series_reader = sitk.ImageSeriesReader()
    series_reader.SetFileNames(series_file_names)
    series_reader.MetaDataDictionaryArrayUpdateOn()
    series_reader.LoadPrivateTagsOn()
    itk_img = series_reader.Execute()

    seriesuid = series_reader.GetGDCMSeriesIDs(path)[0]
    img_array = sitk.GetArrayFromImage(itk_img) # z,y,x
    origin = np.array(itk_img.GetOrigin()) # x,y,z
    spacing = np.array(itk_img.GetSpacing()) # x,y,z

    return img_array, seriesuid, origin, spacing

def worldToVoxelCoord(worldCoord, origin, spacing):
    """ deepseed轉換predict出的座標為真實座標
        predict出來的是world，這邊轉成voxel
    """
    stretchedVoxelCoord = np.absolute(worldCoord - origin)
    # stretchedVoxelCoord = worldCoord - origin
    voxelCoord = stretchedVoxelCoord / spacing
    return voxelCoord # z,y,x 方向還是要看input的座標、ori、spacing決定

def my_rot90(m, k=1, axis=2):
# """Rotate an array k*90 degrees in the counter-clockwise direction around the given axis"""
    m = np.swapaxes(m, 2, axis)
    m = np.rot90(m, k)
    m = np.swapaxes(m, 2, axis)
    return m

# 以下為做成cube需要的function
def padding(label_arr, clean_arr, width):
#     lab_pad = np.pad(label_arr, ((width,width),(width,width),(width,width)), mode='constant', constant_values=0)
    lab_pad = np.pad(label_arr, ((width,width),(width,width),(width,width)), mode='minimum')
    clean_pad = np.pad(clean_arr, ((0,0), (width,width),(width,width),(width,width)), mode='minimum')
    return lab_pad, clean_pad

def lumTrans(img):
    lungwin = np.array([-1200.,600.])
    newimg = (img-lungwin[0]) / (lungwin[1]-lungwin[0])
    newimg[newimg<0] = 0
    newimg[newimg>1] = 1
    newimg = (newimg*255).astype('uint8')
    return newimg

def plt_3d(img, threshold=-300):
    import matplotlib.pyplot as plt
    from skimage import measure
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    # Position the scan upright, 
    # so the head of the patient would be at the top facing the camera
    p = img.transpose(2,1,0) # z,y,x transpose to x,y,z
    print(p.shape)
    # Lewiner marching cubes algorithm to find surfaces in 3d volumetric data
    verts, faces, normals, values = measure.marching_cubes_lewiner(p)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    t = np.linspace(0,1,faces.shape[0])
    mesh = Poly3DCollection(verts[faces], facecolors=plt.cm.cmap_d['bone'](t),alpha=0.6) # viridis, bone, gray

    mesh.set_edgecolor('0.2')
    ax.add_collection3d(mesh)

    ax.set_xlim(0, p.shape[0])
    ax.set_ylim(0, p.shape[1])
    ax.set_zlim(0, p.shape[2])

    plt.show()

def augmentation(arr):
    # Flipping
    flip = ndimage.rotate(arr, 180, axes=(0,2), reshape=False) # y軸不動，z倒過來

    # Rotating 72 degree at each rotate
    rotate1 = ndimage.rotate(arr, 72, axes=(1,2), reshape=False)
    rotate2 = ndimage.rotate(arr, 144, axes=(1,2), reshape=False)
    rotate3 = ndimage.rotate(arr, 216, axes=(1,2), reshape=False)
    rotate4 = ndimage.rotate(arr, 288, axes=(1,2), reshape=False)

    return [flip, rotate1, rotate2, rotate3, rotate4]

def rotCoord(image, xy, angle):
    im_rot = ndimage.rotate(image,angle, reshape=False) 
    org_center = (np.array(image.shape[:2][::-1])-1)/2.
    rot_center = (np.array(im_rot.shape[:2][::-1])-1)/2.
    org = xy-org_center
    a = np.deg2rad(angle)
    new = np.array([org[0]*np.cos(a) + org[1]*np.sin(a),
            -org[0]*np.sin(a) + org[1]*np.cos(a) ])

    return new+rot_center

def getRotCoord(image, coord):
    (x0,z0) = rotCoord(image[:,coord[0][1],:], np.array([coord[0][2], coord[0][0]]), angle=180) # flip
    (x1,y1) = rotCoord(image[coord[0][0],:,:], np.array([coord[0][2], coord[0][1]]), angle=72)
    (x2,y2) = rotCoord(image[coord[0][0],:,:], np.array([coord[0][2], coord[0][1]]), angle=72*2)
    (x3,y3) = rotCoord(image[coord[0][0],:,:], np.array([coord[0][2], coord[0][1]]), angle=72*3)
    (x4,y4) = rotCoord(image[coord[0][0],:,:], np.array([coord[0][2], coord[0][1]]), angle=72*4)

    # (x0,z0) = rotCoord(image[:,coord[0][1],:], np.array([coord[2], coord[0]]), angle=180) # flip
    # (x1,y1) = rotCoord(image[coord[0][0],:,:], np.array([coord[2], coord[1]]), angle=72)
    # (x2,y2) = rotCoord(image[coord[0][0],:,:], np.array([coord[2], coord[1]]), angle=72*2)
    # (x3,y3) = rotCoord(image[coord[0][0],:,:], np.array([coord[2], coord[1]]), angle=72*3)
    # (x4,y4) = rotCoord(image[coord[0][0],:,:], np.array([coord[2], coord[1]]), angle=72*4)


    return [(x0,z0), (x1,y1), (x2,y2), (x3,y3), (x4,y4)] 

def getRotCube(rot_arr_ls, rot_coord_ls, tmp_coord, j, width, mode='minimum'):
    rot_cube_ls = []
    for i, item in enumerate(rot_arr_ls):
        # cname = "cube"
        img_rot_pad = np.pad(item, ((width,width),(width,width),(width,width)), mode='minimum')
        if i == 0: # flip y軸不動、z軸倒過來
            re_y1, re_y2 = tmp_coord[0][1] - j + width, tmp_coord[0][1] + j + width
            re_x1, re_x2 = round(rot_coord_ls[i][0] - j + width), round(rot_coord_ls[i][0] + j + width)
            re_z1, re_z2 = round(rot_coord_ls[i][1] - j + width), round(rot_coord_ls[i][1] + j + width)
            rot_cube = img_rot_pad[re_z1:re_z2, re_y1:re_y2, re_x1:re_x2]
        else: # 一般rotate z軸不動
            re_z1, re_z2 = tmp_coord[0][0] - j + width, tmp_coord[0][0] + j + width
            re_x1, re_x2 = round(rot_coord_ls[i][0] - j + width), round(rot_coord_ls[i][0] + j + width)
            re_y1, re_y2 = round(rot_coord_ls[i][1] - j + width), round(rot_coord_ls[i][1] + j + width)
            rot_cube = img_rot_pad[re_z1:re_z2, re_y1:re_y2, re_x1:re_x2]
        rot_cube_ls.append(rot_cube)

    return rot_cube_ls

def saveCube(cube, cube_fname, count_nodule, flag, j, fail_ls):
    # assert cube.shape == (2*j, 2*j, 2*j), cube.shape
    
    if cube.shape == (2*j, 2*j, 2*j):
        if not os.path.exists(cube_fname):
            # print(f"save cube npy -> {cube_fname}")
            np.save(cube_fname, cube)
            if flag == 0:
                count_nodule += 1
    else:
        print(f"{cube_fname} has wrong shape:{cube.shape}")
        fail_ls.append(cube_fname)

    return count_nodule