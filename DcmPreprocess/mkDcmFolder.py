import os
import shutil
import pydicom

src = r'C:\Users\Administrator\Desktop\371523099'

for dcm in os.listdir(src):
    dcm_path = os.path.join(src, dcm)
    ds = pydicom.dcmread(dcm_path)
    series_desc = ds.SeriesDescription

    folder_path = os.path.join(src, series_desc)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    new_dcm_path = os.path.join(src, folder_path, dcm)
    if not os.path.exists(new_dcm_path):
        shutil.move(dcm_path, new_dcm_path)
        print(f'{dcm} -> {series_desc}')
    
    # break