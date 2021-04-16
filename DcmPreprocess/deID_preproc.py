import os
import shutil
import pydicom


def Patient_info_mod(dcm_path, ds):
    """ modify dcm tag, PatientName and PatientID --> StudyInstanceUID """
    suid = ds.StudyInstanceUID
    ds.PatientName = ds.PatientID = suid
    ds.save_as(dcm_path)

def main(src, dst, tmp_ls):
    """ use for loop in tmp_ls to find those dcm images you need to exclude, and then move them to dst place """
    fail_ls = []
    for dirpath, dirname, files in os.walk(src, topdown=False):
        for file in files:
            dcm_path = os.path.join(dirpath, file)
            try:
                ds = pydicom.dcmread(dcm_path)
                # Patient_info_mod(dcm_path, ds) # 2021/01/23 這版只要拉出不要的，不用改
                series_desc = ds.SeriesDescription
                # if series_desc.lower() in tmp_ls: # v1
                for i in tmp_ls:
                    if i in series_desc.lower():
                        # part = dcm_path.split("L-suiding\\")[1].split("\\")[-3]
                        # case = dcm_path.split("L-suiding\\")[1].split("\\")[-2]
                        # mv_path = os.path.join(dst, i, part, str(case))

                        dataset = dcm_path.split("巨量計畫_20210114\\")[1].split("\\")[-5]
                        case = dcm_path.split("巨量計畫_20210114\\")[1].split("\\")[-4]
                        mv_path = os.path.join(dst, i, dataset, str(case))
                        print(dataset, case, i)
                        if not os.path.exists(mv_path):
                            print(mv_path)
                            os.makedirs(mv_path)
                        shutil.move(dcm_path, mv_path)
                        # break # 2021/01/23 這版只要拉出不要的，不用改
                
            except:
                fail_ls.append(dcm_path)
                # print(f'rm {dcm_path}...')
                # os.remove(dcm_path)

            # break
        # break
    print(f'fail: {len(fail_ls)}')

if __name__ == '__main__':
    # src = r'F:\00_BigData_Image_Dataset\#2_Lung_CT-ImgOnly\Decrypt_images\onDB-reLoad-20201230-v2-32738筆\L-suiding'
    # dst = r'F:\00_BigData_Image_Dataset\#2_Lung_CT-ImgOnly\Decrypt_images\onDB-reLoad-20201230-v2-32738筆\remove'
    src = r'I:\00_BigData_Image_Dataset_DeID\#3_Lung_CT-withAnno_DeID\巨量計畫_20210114'
    dst = r'I:\00_BigData_Image_Dataset_DeID\#3_Lung_CT-withAnno_DeID\remove'
    # 合作製大量解密LungCT
    # tmp_ls = ['dose report', 'dose record', 'dose info' ,'screen save', 'crop', '5  ce', '5 ce',
    #      'patient protocol', 'lung analysis', 'summary', 'brain', 'calcium']

    # 庭瑋整理的LungCT
    tmp_ls = ['dose report', 'dose record', 'dose info' ,'screen save', 'patient protocol', 'lung analysis', 'mip']

    main(src, dst, tmp_ls)
            