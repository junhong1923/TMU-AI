import os
from glob import glob
import shutil
from natsort import natsorted as ns

def newFile_Name(dcm_path, count, tmp_path):
    old_fname = dcm_path.split("\\")[-1]
    old_num = (old_fname.split("-")[1]).split(".dcm")[0]
    new_num = int(old_num) - count
    new_fname = tmp_path + 'Image-' + str(new_num) + '.dcm'
    return new_fname

# src = r'C:\Users\James\Desktop\James\審查制\problem\#3-LungCT-Anno-v-000342\*\*\*'
src = r'C:\Users\James\Desktop\James\審查制\problem'
dst = r'C:\Users\James\Desktop\James\審查制\rename'

def main(src, dst):
    """ 把序列亂掉的dcm檔案 重新排序並複製到dst """
    for case in os.listdir(src):
        case_path = os.path.join(src, case)
        for date in os.listdir(case_path):
            date_path = os.path.join(case_path, date)
            for series in os.listdir(date_path):
                series_path = os.path.join(date_path, series)
                count_ls = []
                series_ls = os.listdir(series_path)
                sort_ls = ns(series_ls)
                for dcm in sort_ls:
                    # print(dcm)
                    tmp_num = (dcm.split("Image-")[1]).split(".dcm")[0] # dcm:Image-10.dcm
                    print('tmp_num', tmp_num)
                    if int(tmp_num) == 1:
                        print(f'{case} {series} is okay')
                        break
                    else:
                        count_ls.append(int(tmp_num))
                        min_num = min(count_ls)
                        count = min_num - 1
                        print('count', count)
                        dcm_path = os.path.join(series_path, dcm) # C:\Users\James\Desktop\James\審查制\problem\#3-LungCT-Anno-v-000342\Study-CT-20270218-183\Series-2\Image-10.dcm
                        print('Old', dcm_path)
                        tmp_path = os.path.join(dst, case, date, series) + "\\"
                        
                        if not os.path.exists(tmp_path):
                            os.makedirs(tmp_path)

                        new_fname = newFile_Name(dcm_path, count, tmp_path)
                        print('New', new_fname)
                        os.rename(dcm_path, new_fname)
                        print("-------------------------")
                    # break
                # break
            # break
        # break

# main(src, dst)

def main2(src, dst):
    """ 把改過序列的Series資料夾整包移動回原始資料 """
    tmp_path = src + "/*/*/*"
    for i in glob(tmp_path):
        tmp_path = i.split("rename\\")[1]
        # print(tmp_path)
        dst_path = os.path.join(dst, tmp_path)
        # print(dst_path)
        if os.path.exists(dst_path):
            print(f'remove old one : {dst_path}')
            shutil.rmtree(dst_path)
            print(f'copy new one: {i}')
            shutil.copytree(i, dst_path)
        print("------------------")
        # break

# src2 = r'D:\審查制影像_01\TMUH\RSNA_deID\VPN_450_v6_0903'
# src2 = r'D:\審查制影像_01\TMUH\RSNA_deID\Download_52_v7_0903'
# main2(dst, src2)

# 10/20
def main3(src):
    """把series-7裡面兩組不同series instance uid的影像分出來"""
    import pydicom
    
    def get_Tag_Set(src):
        tmp_set = set()
        for dcm in glob(src):
            ds = pydicom.dcmread(dcm)
            series_des = ds.SeriesDescription
            tmp_set.add(series_des)
        return tmp_set

    tmp_set = get_Tag_Set(src)
    for tag in tmp_set:
        print(f'this is tag: {tag}')
        tmp_path = src.split("\\Serie")[0] + "\\" + tag
        # print(tmp_path)
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)
        for dcm in glob(src):
            ds = pydicom.dcmread(dcm)
            series_des = ds.SeriesDescription
            if series_des == tag:
                tmp_dcm = dcm.split("\\")[-1]
                dst_path = os.path.join(tmp_path, tmp_dcm)
                # print(dst_path)
                shutil.copyfile(dcm, dst_path)
                print(f'{dcm} -> {dst_path}')

# src3 = r'C:\Users\James\Desktop\James\審查制\problem\Series-7\*'
# main3(src3)

def main4(src, dst):
    """ 把序列亂掉的dcm檔案 重新排序並複製到dst """
    for case in os.listdir(src):
        case_path = os.path.join(src, case)

        tmp_ls = os.listdir(case_path)
        sort_ls = ns(tmp_ls)
        count_len = len(sort_ls) # dcm numbers
        print(f'count_len: {count_len}')
        count = 1
        for dcm in sort_ls:
            dcm_path = os.path.join(case_path, dcm)
            tmp_num = (dcm.split("Image-")[1]).split(".dcm")[0]
            print(tmp_num)
            new_file_name = "Image-" + str(count) + ".dcm"
            dst_path = os.path.join(dst, case)
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            new_file_name_path = os.path.join(dst_path, new_file_name)
            print(new_file_name_path)
            if not os.path.exists(new_file_name_path):
                shutil.copyfile(dcm_path, new_file_name_path)
                print(f'{case}: {dcm} --> {new_file_name_path}')
            count += 1

            # break
        # break

# main4(src, dst)

def main5():
    import pydicom
    import os
    # import shutil
    # from glob import glob

    src = r'C:\Users\James\Desktop\James\demo\gary\LungS\LungS_for_demo\Data\dicom\testing_data(3923151407043)'
    for dcm in os.listdir(src):
        dcm_path = os.path.join(src, dcm)
        print(dcm_path)
        ds = pydicom.dcmread(dcm_path)
        print(ds.SeriesDescription)
        sd_folder = os.path.join(src, ds.SeriesDescription)
        if not os.path.exists(sd_folder):
            os.makedirs(sd_folder)
        new_path = os.path.join(sd_folder, dcm_path.split("\\")[-1])
        print(new_path)
        shutil.move(dcm_path, new_path)

        
        # break

# main5()

def main6():
    import os
    src = r'C:\Users\James\Desktop\James\demo\gary\LungS\LungS_for_demo\Data\05740118_testing_data\05740118\05740118_SE2_Lung__1mm'
    for i in os.listdir(src):

        i_path = os.path.join(src, i)
        print(i_path)
        new_path = i_path + ".dcm"
        print(new_path)
        os.rename(i_path, new_path)
        # break
main6()