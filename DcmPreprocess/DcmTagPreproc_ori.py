import os
import pandas as pd
import pydicom

""" 最初版本，依據清單來改dcm的tag """
ls_path = r'C:\Users\james\Desktop\CT_Hans(整理過)_v2_0909.xlsx'
df = pd.read_excel(ls_path, sheet_name='3', index_col='accession_number')

data_src = r'F:\00_BigData_Image_Dataset\#2_Lung_CT-ImgOnly\Decrypt_images\CT_hans_0909\LungCT-2nd-1-9'
fail_ls = []
count = 0
for dirpath, dirname, files in os.walk(data_src, topdown=False):
    for file in files:
        if '.dcm' in file:
            try:
                dcm_path = os.path.join(dirpath, file)
                acc = dcm_path.split('\\')[-2]
                # if str.isdigit(acc):     
                #     suid = df.loc[int(acc)]['study_uid']
                # else:
                #     suid = df.loc[str(acc)]['study_uid']
                print(f'case: {acc}')
                
                suid = df.loc[acc]['study_uid']
#                 print(suid)
                ds = pydicom.dcmread(dcm_path)
                new_pid = ds.PatientName = str(suid)
                new_pname = ds.PatientID = str(suid)
                print(f'new pname: {new_pid}\nnew pid: {new_pname}')
                ds.save_as(dcm_path)
                count += 1
                print(count)
            except:
                fail_ls.append(acc)
                print(f'..... {acc} fail.....')
#                 raise
#         break
#     break

print(count)

if len(fail_ls)>0:
    fail_df = pd.DataFrame(data=fail_ls, columns=['fail case'])
    fail_df.to_csv(r'C:\Users\james\Desktop\xray_fail_modify_tag_1-9-1.csv', index=False)
    print(fail_df)
else:
    print('all done no fail')

def lineMe():
    """ by Clay, if jobs done then send line notification """ 
    import requests
    def lineNotifyMessage(token, msg):
        headers = {
            "Authorization": "Bearer " + token, 
            "Content-Type" : "application/x-www-form-urlencoded"
        }
        
        payload = {'message': msg}
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
        return r.status_code
        
    # 修改為你要傳送的訊息內容
    message = 'Code is finished!'
    # 修改為你的權杖內容
    token = 'YT4Q3pP1a7CITf7vkiOgTES0VjZKKKSefPtbYysfyTw'

    lineNotifyMessage(token, message)