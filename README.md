北邮命令行上网认证
=================
使用北邮校园网时能够在终端下进行认证的脚本程序

用法
====

使用./autoLogin.py -h 查看帮助信息。

```sh
usage: ./autoLogin.sh [-u username] [-p password] [-s ip] [-h][-t]
	-u username
	-p password
	-s suthentication server
	-h display this help and exit
	-t test the current network if available and exit
usage: autoLogin.py [-h] [-t] [-u USER] [-p PASSWORD] [-f FILE] [-H HOST] [-c]
                    [-v]

optional arguments:
  -h, --help            show this help message and exit
  -t, --test            Test current network state and exit.
  -u USER, --user USER  Your account id, may be your classId.
  -p PASSWORD, --password PASSWORD
                        Your account password.
  -f FILE, --file FILE  Get account information from this file, 'account.data'
                        by default.
  -H HOST, --host HOST  The remote address, 'http://10.3.8.211' by default.
  -c, --logout          Logout
  -v, --version         show program's version number and exit
```

版本
====
包括两个版本，一个是python版本，需要安装httplib2库，另一个是sh脚本版本。
