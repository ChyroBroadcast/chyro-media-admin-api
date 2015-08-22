#!/bin/bash

##		Chyro API Model
##				Copyright (c) 2015:
##						Chyro Conseil <support@chyro.tv>
##					Licensed Under MIT license
##
##    Install WGet
##


##
##      SETUP
##


## Credentials
host="HOSY" #  Host, like preprod.mycompany.chyro.fr (without http://)
user="USER" # Login with API read/write
passwd="PASS" # Password

## Files
res="/tmp/search_result_api.json" # File result
auth="/tmp/auth_api.json" # Auth file result. Can be generic
cookie="/tmp/chyro_cookie_api.txt" # Cookie. Can be temporary

# Logs
LOG="/tmp/log_script.log"
WGET="/usr/bin/wget"

##
##      PURGE
##
if [ -f $cookie ]; then
        rm $cookie
fi
if [ -f $auth ]; then
        rm $auth
fi
if [ -f $res ]; then
        rm $res
fi

##
##      MAIN CODE
##
$WGET -o $LOG -O $auth --cookies=on --keep-session-cookies --save-cookies $cookie "http://$host/api/auth/gettoken/format/json?user=$user&password=$passwd"
if [ -f $auth ]; then
        token=$(cat $auth | cut -d ':' -f 2 | cut -d '"' -f 2)
        if [ "$token" != "false" ]; then
                $WGET -o $LOG -O $res --cookies=on  --load-cookies $cookie --keep-session-cookies "http://$host/api/search/program/format/json?query={title=test}&token=$token"
                echo "Ok ! Result : $res"
        else
                echo "Login/Pass failed !"
        fi
fi
