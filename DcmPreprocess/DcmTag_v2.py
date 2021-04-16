import os
from glob import glob
import pandas as pd
import pydicom

def get_dcm_tag(dcm_path, info_ls):
    ds = pydicom.dcmread(dcm_path)
    try:
        manufacturer = ds.Manufacturer
    except:
        manufacturer = 'NA'
    try:
        slice_thickness = ds.SliceThickness
    except:
        slice_thickness = 'NA'
    try:
        slice_location = ds.SliceLocation
    except:
        slice_location = 'NA'
    try:
        kernel = ds.ConvolutionKernel
    except:
        kernel = 'NA'
    try:
        filter_type = ds.FilterType
    except:
        filter_type = 'NA'
    try:
        patient_locatioin = ds.PatientPosition
    except:
        patient_locatioin = 'NA'
    try:
        rescale_type = ds.RescaleType
    except:
        rescale_type = 'NA'
    try:
        intercept = ds.RescaleIntercept
    except:
        intercept = 'NA'
    try:
        slope = ds.RescaleSlope
    except:
        slope = 'NA'
        
    info_ls.append((manufacturer,
            slice_thickness, slice_location, kernel, filter_type,
            patient_locatioin, rescale_type, intercept, slope))
    
    return info_ls

def main():
    """ this code is for CAC project, record dcm tag info. such as slice thickness, spacing and so on...
        however, teacher Lin has already done this part, so ignore this DcmTag_v2.py
    """ 
    path_src = r'I:\study\心鈣_LDCT_deID_v2\score_5'
    dst = r'I:\study\心鈣_LDCT_deID_v2\dcm_info'
    cac_ls, lungwin_ls, soft_ls = [], [], []

    for case in os.listdir(path_src):
        print(case)
        cac_path = os.path.join(path_src, case, 'Cardiac-CT\\CaSc\\*')
        lungwin_path = os.path.join(path_src, case, 'LDCT\\lung-window\\*')
        soft_path = os.path.join(path_src, case, 'LDCT\\soft-tissue\\*')
        
        cac_dcm = glob(cac_path)[0]
        lungwin_dcm = glob(lungwin_path)[0]
        soft_dcm = glob(soft_path)[0]

        # get dcm tag info.
        cac_ls = get_dcm_tag(cac_dcm, cac_ls)
        lungwin_ls = get_dcm_tag(lungwin_dcm, lungwin_ls)
        soft_ls = get_dcm_tag(soft_dcm, soft_ls)
        # break

    headers = ["manufacturer","slice_thickness","slice_location","kernel","filter_type","patient_locatioin","rescale_type","intercept","slope"]
    cac = pd.DataFrame(data=cac_ls, columns=headers, index=os.listdir(path_src))
    lungwin = pd.DataFrame(data=lungwin_ls, columns=headers, index=os.listdir(path_src))
    soft = pd.DataFrame(data=soft_ls, columns=headers, index=os.listdir(path_src))

    cac.to_excel(os.path.join(dst, 'cac_score5.xlsx'))
    lungwin.to_excel(os.path.join(dst, 'lungwin_score5.xlsx'))
    soft.to_excel(os.path.join(dst, 'soft_score5.xlsx'))
    
if __name__ == '__main__':
    main()