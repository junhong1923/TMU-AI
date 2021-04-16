import os
import pandas as pd

def Query(suid_ls):
    content = "("+ str(suid_ls) + ")"
    content = content.replace('[', '') ; content = content.replace(']', '') 
    q_1 = 'select img.image_file,s.accession_number,ser.modality from study1 as s,series1 as ser,image1 as img where s.study_uid in '
    q_2 = content
    q_3 = ' and s.study_uid_id = ser.study_uid_id and ser.series_uid_id = img.series_uid_id'
    query = q_1 + q_2 + q_3
    return query

def Write_txt_xlsx(part_count, suid_count, txt_dst_path, xlsx_dst_path, query, acc_ls, suid_ls):
    # part_count += 1
    txt_file_name = 'Decrypt_part' + str(part_count) + '_' + str(suid_count) + '.txt'
    txt_file_path = os.path.join(txt_dst_path, txt_file_name)
        
    csv_file_name = 'Decrypt_part' + str(part_count) + '_' + str(suid_count) + '.xlsx'
    csv_file_path = os.path.join(xlsx_dst_path, csv_file_name)
        
    if not os.path.exists(txt_file_path):
        # print('wirting')
        with open(txt_file_path, mode='w') as file:
            file.write(query)
    else:
        print('already done')
    if not os.path.exists(csv_file_path):
        acc_df = pd.DataFrame(data=acc_ls, columns=['acc'])
        acc_df.to_excel(csv_file_path, index=False)
    else:
        print('already done')

    # acc_ls.clear(), suid_ls.clear()

def main(ls_src, outPut_path):
    df = pd.read_csv(ls_src)
    txt_path = os.path.join(outPut_path, 'decrypt_txt')
    if not os.path.exists(txt_path):
        os.mkdir(txt_path)
    xlsx_path = os.path.join(outPut_path, 'decrypt_xlsx')
    if not os.path.exists(xlsx_path):
        os.mkdir(xlsx_path)

    suid_count, t_count = 0, 0
    suid_ls = []

    for i in range(len(df)):
        suid = df['study_uid'].iloc[i]

        suid_ls.append(suid)
        suid_count += 1
        
        if len(suid_ls) % 500 == 0:
            query = Query(suid_ls)

            t_count += 1 # record how many part
            txt_file_name = 'Decrypt_part' + str(t_count) + '_' + str(suid_count) + '.txt'
            txt_file_path = os.path.join(txt_path, txt_file_name)
            
            csv_file_name = 'Decrypt_part' + str(t_count) + '_' + str(suid_count) + '.xlsx'
            csv_file_path = os.path.join(xlsx_path, csv_file_name)
            
            if not os.path.exists(txt_file_path):
                # print('wirting')
                with open(txt_file_path, mode='w') as file:
                    file.write(query)
            
            if not os.path.exists(csv_file_path):
                acc_df = pd.DataFrame(data=suid_ls, columns=['suid'])
                acc_df.to_excel(csv_file_path, index=False)
            
            suid_ls.clear()
            
    #         break
    #     break

    # 最後一個part要額外處理
    print(len(suid_ls))
    query = Query(suid_ls)        
    t_count += 1
    txt_file_name = 'Decrypt_part' + str(t_count) + '_' + str(suid_count) + '.txt'
    txt_file_path = os.path.join(txt_path, txt_file_name)

    xlsx_file_name = 'Decrypt_part' + str(t_count) + '_' + str(suid_count) + '.xlsx'
    xlsx_file_path = os.path.join(xlsx_path, xlsx_file_name)

    if not os.path.exists(txt_file_path):
        # print('wirting')
        with open(txt_file_path, mode='w') as file:
            file.write(query)

    if not os.path.exists(xlsx_file_path):
        acc_df = pd.DataFrame(data=suid_ls, columns=['suid'])
        acc_df.to_excel(xlsx_file_path, index=False)


if __name__ == '__main__':
    # ls_src = r'C:\Users\TMU_AIMC\Documents\資料庫\LungCT\Hans語法查詢結果\onDB-reLoad-20201230-v2-32738.csv'
    # outPut_path = r'C:\Users\TMU_AIMC\Desktop\xnat\解密\ct\onDB-reLoad-20201230-v2-32738'
    ls_src = r'C:\Users\TMU_AIMC\Documents\資料庫\Xray\onDB-reLoad-20210105-xray-81690.csv'
    outPut_path = r'C:\Users\TMU_AIMC\Desktop\xnat\解密\xray\onDB-reLoad-20210105-xray-81690'
    main(ls_src, outPut_path)