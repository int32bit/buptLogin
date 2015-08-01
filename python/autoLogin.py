#!/usr/bin/python
#coding=utf-8
#vim ts=4
from httplib2 import Http
from urllib import urlencode
import argparse
import sys

class User:
    """
    User: a User obj
    user.name: The user's name
    user.id: The user's id
    user.password: The user's password
    """
    def __init__(self, name, id, password):
        self.__name__ = name
        self.__id__ = id
        self.__password__ = password
    def __str__(self):
        return "{0}\t{1}\t{2}".format(self.__name__, self.__id__, self.__password__)
    def __repr__(self):
        return self.__str__()
    def getUserName(self):
        return self.__name__
    def getId(self):
        return self.__id__
    def getPassword(self):
        return self.__password__

def getUsersFromFile(file = None):
    """
    File format:
    张三    2013xxxx    123456
    or
    2013xxxx    123456
    """
    users = list()
    if file is None:
        return users;
    # try to get all lines from the file
    with open(file, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if len(line) == 0 or line.startswith("#"):
            continue
        items = line.split()
        if len(items) < 2:
            continue
        if len(items) == 2:
            users.append(User("匿名", items[0], itmes[1]))
        else:
            users.append(User(items[0], items[1], items[2]))
    return users

def test():
    """
    To test current network state.
    """
    h = Http()
    resp, content = h.request("http://baidu.com")
    if resp["content-location"] == "http://10.3.8.211":
        return False
    return True

def login(user = None, auth_url = None):
    """
    Try to login, if success, return True.
    user: The user try to login, both user.id and user.password are required!
    auth_url: The auth url. the bupt, for example, is http://10.3.8.211
    """
    if user is None or auth_url is None:
        return False
    h = Http()
    data = {"DDDDD":user.getId(), "upass":user.getPassword(), "save_me":1, "R1":0}
    resp, content = h.request(auth_url, "POST", urlencode(data))
    return test()

def logout(url = "http://10.3.8.211/F.hml"):
    """
    Try to logout.
    url: The logout url, for example: http://10.3.8.211/F.hml"
    """
    if test():
        h = Http()
        resp, content = h.request(url)
    return not test()

def parse(args):
    """
    Parse the position arguments, the first argument(args[0]) should be ignored!
    """
    parser = argparse.ArgumentParser(add_help = True)
    parser.add_argument('-t',
            '--test',
            action='store_true',
            dest='test',
            default = False,
            help = 'Test current network state and exit.')
    parser.add_argument('-u',
            '--user',
            action='store',
            dest = 'user',
            default = '',
            help = 'Your account id, may be your classId.')
    parser.add_argument('-p',
            '--password',
            action='store',
            dest = 'password',
            default = '',
            help = 'Your account password.')
    parser.add_argument('-f',
            '--file',
            action='store',
            dest='file',
            default='accounts.data',
            help="Get account infomation from this file, 'account.data' by default.")
    parser.add_argument('-H',
            '--host',
            action='store',
            dest='host',
            default='http://10.3.8.211',
            help="The remote address, 'http://10.3.8.211' by default.")
    parser.add_argument('-c',
            '--logout',
            action='store_true',
            dest='logout',
            default=False,
            help="Logout")
    parser.add_argument('-v',
            '--version',
            action='version',
            version = '%(prog)s 1.0')
    result = parser.parse_args(args)
    if result.test:
        if test():
            print("OK!")
        else:
            print("Fail!")
        exit(0)
    if result.logout:
        succeed = logout()
        if succeed:
            print("Logout successfully.")
        else:
            print("Failed to logout!")
        exit(0)
    if test():
        print("The network is Ok, You shouldn't login again, now exit!")
        exit(0)
    url = result.host
    if len(result.user) > 0 and len(result.password) > 0:
        success = login(User('unknown', result.user, result.password), url)
        if success:
            print("OK!")
        else:
            print("Failed!")
        exit(0)
    users = getUsersFromFile(result.file)
    for user in users:
        print("{0} try to login...".format(user.getUserName()))
        success = login(user, url)
        if success:
            print("{0} succeed to login!".format(user.getUserName()))
            exit(0)
        else:
            print("{0} failed to login！".format(user.getUserName()))
            print("Try next account ...")
    print("Failed to login!")

# Remember: The first position argument should be ignored!
if __name__ ==  "__main__":
    parse(sys.argv[1:])
