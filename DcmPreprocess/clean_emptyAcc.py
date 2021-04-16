import os
import shutil
import pydicom


def cleanEmptyAcc():
    """ if EBM pacs software decrpyt mess(no accession number) dicom images, then use this function to arrange those dcm by their StudyInstanceUID """ 

    src = r'F:\00_BigData_Image_Dataset\#2_Lung_CT-ImgOnly\Decrypt_images\onDB-reLoad-20201230-v2-32738筆\temp'
    dst = r'F:\00_BigData_Image_Dataset\#2_Lung_CT-ImgOnly\Decrypt_images\onDB-reLoad-20201230-v2-32738筆\L-suiding\part59'

    for ele in os.listdir(src):
        ele_path = os.path.join(src, ele) # F:\00_BigData_Image_Dataset\#2_Lung_CT-ImgOnly\Decrypt_images\空acc混\01852e28.dcm
        if not os.path.isdir(ele_path):
            dcm_path = ele_path
            dcm = dcm_path.split('\\')[-1]
            ds = pydicom.dcmread(dcm_path)
            suid = ds.StudyInstanceUID
            suid_folder_path = os.path.join(dst, suid)
    #         print(suid_folder_path)
            if not os.path.exists(suid_folder_path):
                os.mkdir(suid_folder_path)
                dcm_dst = suid_folder_path + '\\' + dcm
    #             print(dcm_dst)
                shutil.move(dcm_path, dcm_dst)
            else:
                dcm_dst = suid_folder_path + '\\' + dcm
                shutil.move(dcm_path, dcm_dst)
    #         print(f'{dcm} --> {suid}')
        
        elif os.path.isdir(ele_path):
            print(f'{ele} has accession folder')
            acc = ele_path.split('\\')[-1]
            acc_dst = os.path.join(dst, str(acc))
            if not os.path.exists(acc_dst):
                shutil.copytree(ele_path, acc_dst)
                print(f'..{acc}..')
    #     break