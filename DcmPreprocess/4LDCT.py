import os
from glob import glob
import shutil
import pydicom
import pandas as pd



def getDCMinfo(dcm_path):
    ds = pydicom.dcmread(dcm_path)
    try:
        pid = ds.PatientID
    except:
        pid = "None"
    try:
        acc = ds.AccessionNumber
    except:
        acc = "None"
    try:
        ser_num = ds.SeriesNumber
    except:
        ser_num = "None"
    try:
        ser_des = ds.SeriesDescription
    except:
        ser_des = "None"
    try:
        stu_des = ds.StudyDescription
    except:
        stu_des = "None"
    try:
        stu_uid = ds.StudyInstanceUID
    except:
        stu_uid = "None"
    try:
        manu = ds.Manufacturer
    except:
        manu = "None"
    try:
        thick = ds.SliceThickness
    except:
        thick = 'None'
    try:
        age = ds.PatientAge
    except:
        age = "None"
    try:
        inN = ds.InstanceNumber
    except:
        inN = "None"
    info = [pid, acc, ser_des, manu, thick, stu_uid, age, stu_des, ser_num, inN]

    return info

def renameDCM(DCMinfo, dcm_path):
    inN = DCMinfo[-1]
    if int(inN) < 10:      
        dcmName = 'Image000{}.dcm'.format(inN)        
    elif int(inN) >= 10 & int(inN) < 100:    
        dcmName = 'Image00{}.dcm'.format(inN)    
    elif int(inN) >= 100:   
        dcmName = 'Image0{}.dcm'.format(inN)
    else:  
        dcmName = 'Image{}.dcm'.format(inN)

    return dcmName

def mvDCM(DCMinfo, case_path, dcm_path):
    # stu_des = DCMinfo[2].replace(" ", "_").replace(".", "") # TMUH
    stu_des = DCMinfo[2].replace(" ", "").replace(":", "_") # SHH
    
    if "crop" not in stu_des:
        folder_path = os.path.join(case_path, stu_des)
    elif "crop" in stu_des:
        folder_path = os.path.join(case_path, "S" + str(DCMinfo[-2]) + "0_cropped")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    dcmName = renameDCM(DCMinfo, dcm_path)
    dcm_dst = os.path.join(folder_path, dcmName)
    # print(dcm_dst)
    if not os.path.exists(dcm_dst):
        shutil.move(dcm_path, dcm_dst)
    else:
        print(f'..........{dcm_dst} exits.............')

def wrCSV(all_info, save=True):    
    import pandas as pd # ,"InstanceNumber"
    import numpy as np
    wrData = np.delete(np.array(all_info), -1, axis=1) # 刪除陣列的最後一行(Instance number)
    headers = ["PatientID","AccessionNumber","SeriesDescription","Manufacturer","SliceThickness","StudyInstanceUID","PatientAge","StudyDescription","SeriesNumber"]
    df = pd.DataFrame(data=set(tuple(l) for l in wrData), columns=headers) # np array 不能直接丟到 set
    if save:
        df.to_excel("I:/program/James/LDCT/DCMinfo_cardio_newcase.xlsx", index=False)

def main(data_src):
    all_info = []
    # for case in os.listdir(data_src):
    #     case_path = os.path.join(data_src, case)
    #     for ele in os.listdir(case_path):
    #         ele_path = os.path.join(case_path, ele)
    #         if ".dcm" in ele_path: # 還沒整理好的資料夾
    #             # print(ele_path)
    #             info = getDCMinfo(ele_path)
    #             all_info.append(info)
    #             print(info)
    #             mvDCM(info, case_path, ele_path)
    #             # break
    #         else:
    #             if os.path.isdir(ele_path):
    #                 for dcm in os.listdir(ele_path)[:2]:
    #                     dcm_path = os.path.join(ele_path, dcm)
    #                     info2 = getDCMinfo(dcm_path)
    #                     print(info2)
    #                     all_info.append(info2)
                # continue
                # break
        # break

# FOR 心鈣+LDCT資料，抓tag、看規律
    for i in range(1, 6):
        tmp_i = f"score_{i}"
        for case in os.listdir(os.path.join(data_src, tmp_i)):
            print(case)
            for s1 in os.listdir(os.path.join(data_src, tmp_i, case)):
                print(s1)
                for s2 in os.listdir(os.path.join(data_src, tmp_i, case, s1)):
                    print(s2)
                    for dcm in os.listdir(os.path.join(data_src, tmp_i, case, s1, s2)):
                        print(dcm)
                        info = getDCMinfo(os.path.join(data_src, tmp_i, case, s1, s2, dcm))
                        all_info.append(info)
                        print(info)
                        # break
        # break
    
    wrCSV(all_info, save=True)

# data_src = r'G:\TMUData\LDCT\TMUH'
# data_src = r'G:\TMUData\LDCT\TMUH_LDCT(含lung_RADS)'
# data_src = r'G:\TMUData\LDCT\SHH'
data_src = r'I:\study\DeID-Study-v2' # 心鈣的資料也整理出tag

if __name__ == "__main__":
    main(data_src)