#!/bin/bash
#set -x
declare -f showHelp
declare -f isReachable 
SERVER=10.3.8.211 # Change this value!
showHelp()
{
cat <<EOF
usage: $0 [-u username] [-p password] [-i ip] [-h][-t]
	-u username
	-p password
	-i remote server login IP
	-h display this help and exit
	-t test the current network state and exit
EOF
exit 1
}
isReachable()
{
    ADDR=${1:-baidu.com}
    ping -c 1 -w 2 $ADDR &>/dev/null
    return $?
}
parseOpts()
{
    while getopts ":u:p:i:ht" arg
    do
        case $arg in
            u)
                ID=$OPTARG
                ;;
            p)
                PASSWORD=$OPTARG
                ;;
            h)
                showHelp
                exit 0
                ;;
            i)
                SERVER=$OPTARG
                ;;
            t)
                if isReachable 
                then
                    echo "OK"
                else
                    echo "Faild"
                fi
                exit 0
                ;;
            :|?|*)
                showHelp
                exit 1
                ;;
        esac
    done
}
inputUserName()
{
    read -p "Please type your userId: " ID
}
inputPassword()
{
	stty -echo
	read -p"Please type your password: " PASSWORD
	stty echo
	echo
}
getRequest()
{
    if [ $# -lt 1 ]
    then
        echo "Request address required!"
        echo "Usage $0 address"
        exit 1
    fi
    ADDRESS=$1
    curl -X GET $ADDRESS
}
postRequest()
{
    if [ $# -lt 2]
    then
        echo "Both address and data are required!"
        echo "Usage $0 data address"
        echo "For example: postRequest 'a=1&b=2' example.com"
        exit 1
    fi
    DATA=$1
    ADDRESS=$2
    curl -X POST -d $DATA $ADDRESS
}
request()
{
    getRequest $@
}
login()
{
    if [ x == x$SERVER ]
    then
        echo "The address of server not set"
        exit 1
    fi
    if ! isReachable $SERVER
    then
        echo "Cann't connect to server!"
        exit 1
    fi
    [ x$ID == x ] && inputUserName
    [ x$PASSWORD == x ] && inputPassword
    postRequest "DDDDD=$ID&upass=$PASSWORD&save_me=1&R1=0" "$SERVER" &>/dev/null
}
main()
{
    parseOpts $@
    if isReachable baidu.com
    then
        echo "The current network is OK, You should't login again!"
        exit 0
    fi
    login
    if isReachable baidu.com
    then
        echo "OK"
        exit 0
    else
        echo "Failed"
        exit 1
    fi
}
main $@
