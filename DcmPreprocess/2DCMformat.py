import os


def DCMformat():
    src = 'F:\心臟鈣化_LDCT\score_5'
    for dirpath, dirname, files in os.walk(src, topdown=False):
        for file in files:
            if not ".dcm" in file:
                tmp_path = os.path.join(dirpath, file)

                new_name = tmp_path + ".dcm"
                print(f"{tmp_path} -> {new_name}")
                os.rename(tmp_path, new_name)
            # break
        # break

def changePID():
    import pydicom

    # src = 'F:\心臟鈣化_LDCT\score_5'
    # src = 'I:\study\score_1'
    src = 'F:\心臟鈣化_LDCT\心臟鈣化(score4-5)'

    count = 0
    for dirpath, dirname, files in os.walk(src, topdown=False):
        for file in files:
            if ".dcm" in file:
                dcm_path = os.path.join(dirpath, file)
                print(dcm_path)
                acc = dcm_path.split("\\")[4] # 要改這邊
                print("                        ", acc)

                ds = pydicom.dcmread(dcm_path)
                ds.PatientID = ds.PatientName = acc # 不一定是acc，反正改成資料夾名稱，使之不會重複患者
                ds.save_as(dcm_path)
                count += 1
                # print("==========================")

        #     break
        # break
    print(count)

changePID()