#!/usr/bin/env python
# -*- coding:utf-8 -*-
###
# File: create_sql.py
# Created Date: Tuesday, October 27th 2020, 4:10:30 pm
# Author: Brian Van Benschoten     Email: bvanbenschoten@presidio.com
# Company:  Presidio
# -----
# Last Modified: Wednesday October 28th 2020 2:30:15 pm
# Modified By: Brian Van Benschoten
# -----
# Insert History line  ctrl-alt-C, ctrl-alt-C. (do it twice)
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
# 2020-10-28	BVB	use the SQL logic from this github example for PHP : https://github.com/moki74/cucm-appuser-devices/blob/master/cucmappuser.php
###
from __future__ import print_function, unicode_literals
import sys, os, logging, platform, argparse, re
from datetime import datetime

def fullStamp (date_sep = '-', time_sep = '-'):
    """
    Returns str of full date_and_time-stamp YYYY-MM-DDTHH-MM-SS.
    
    accepts two str arguments:  date_sep and time_sep
    date_sep defaults to '-'   time_sep defaults to '-'
    """
    
    stamp = datetime.now().strftime('%Y'+date_sep+'%m'+date_sep+'%d'+'T'+'%H'+time_sep+'%M'+time_sep+'%S')
    return stamp

input_file_name = 'devices.txt'
output_file_name = 'sql_output_add'
output_file_name_remove = 'sql_output_Rm-assoc'
output_directory = 'output'
file_timestamp = fullStamp()
output_file_name = output_file_name + "_" + file_timestamp + ".txt"
output_file_name = os.path.join(output_directory, output_file_name)
output_file_name_remove = output_file_name_remove  + "_" + file_timestamp + ".txt"
output_file_name_remove = os.path.join(output_directory, output_file_name_remove)

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

app_user = ""
device = ""
device_string = ""

with open(input_file_name, 'r') as i:
    device_list = i.read().split('\n')
    
#  ----------- POPULATE THE CUCM APPLICATION USER(S) THAT YOU NEED TO ASSOCIATE USERS WITH ------------    
app_users_list = ['DAL_RMCM', 'WFM_REC01']
counter = 1
## not sure of the limit of the number of devices that can be included in a single SQL command
## tested with 16 device 2020-10-27-BV
for device in device_list:
    if counter < len(device_list):
        device_string = device_string + f"'{device}'" + ","
        counter += 1
    else:
        # don't add comma after the last device in the list
        device_string = device_string + f"'{device}'"
    
# sql command to run at CUCM CLI.  the last part (and d.pkid not in (select fkdevice........) stops error when trying to 
# associate devices that are ALREADY associated with the application user.
# successful output from the sql command will print "Rows: XX" at the CUCM CLI.  This represents the number of NEW device associations

for app_user in app_users_list:
    output_string = (f"run sql insert into applicationuserdevicemap (fkapplicationuser, fkdevice, tkuserassociation) select au.pkid, d.pkid, 1 from applicationuser au cross join device d where au.name = '{app_user}' and d.name in ({str(device_string)}) and d.pkid not in (select fkdevice from applicationuserdevicemap where fkapplicationuser = au.pkid)")
    output_string_delete = (f"run sql delete from applicationuserdevicemap where fkapplicationuser = (select pkid from applicationuser au where au.name = '{app_user}') and fkdevice in (select pkid from device d where d.name in ({str(device_string)}))")
    print (f'\nAssociate Device String: \n {output_string}\n')
    print (f'\nDISassociate Device String: \n {output_string_delete}\n')
    # write out the Associate devices from app user SQL command
    with open (output_file_name, 'a+') as f:
        f.write(output_string + '\n')
    
    # write out the DISassociate devices from app user SQL command
    with open (output_file_name_remove, 'a+') as f:
        f.write(output_string_delete + '\n')
