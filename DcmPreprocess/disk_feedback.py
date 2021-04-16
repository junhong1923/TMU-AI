import psutil
import time
import os
import requests
#line notify function
def lineNotifyMessage(token, msg):
    headers = {
          "Authorization": "Bearer " + token, 
          "Content-Type" : "application/x-www-form-urlencoded"
      }
	
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code
	
  # 修改為你要傳送的訊息內容
message = 'RSNA Finished!'
  # 修改為你的權杖內容
token = 'YT4Q3pP1a7CITf7vkiOgTES0VjZKKKSefPtbYysfyTw'


#disk speed feedback

read_spd_E = 11
write_spd_E = 11
#loop
while int(read_spd_E) + int(write_spd_E)> 15:
        
    iocnt1 = psutil.disk_io_counters(perdisk=True)['PhysicalDrive1']
    time.sleep(5)
    iocnt2 = psutil.disk_io_counters(perdisk=True)['PhysicalDrive1']
    # print(iocnt1.read_count)
    # print(iocnt2.read_count)
    # print('Block written {0}'.format(iocnt2.write_count - iocnt1.write_count))
    read_spd_E = format(iocnt2.read_count - iocnt1.read_count)
    write_spd_E = format(iocnt2.write_count - iocnt1.write_count)
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('disk:0')
    print('time:',now_time)
    print('read:',read_spd_E)
    print('wtire:',write_spd_E)
    # print(psutil.disk_partitions(all=False))
    # print('Block written {0}')
    if int(read_spd_E) + int(write_spd_E) <= 15:
        lineNotifyMessage(token, message)
    time.sleep(60)
