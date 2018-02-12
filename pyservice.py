######################################
#####Copy files function #############
######################################

import os, sys
import filecmp
import re
import shutil
holderlist = []

def compareme(dir1, dir2):
    dircomp = filecmp.dircmp(dir1, dir2)
    only_in_one = dircomp.left_only
    diff_in_one = dircomp.diff_files
    dirpath = os.path.abspath(dir1)
    [holderlist.append(os.path.abspath(os.path.join(dir1, x))) for x in only_in_one]
    [holderlist.append(os.path.abspath(os.path.join(dir1, x))) for x in diff_in_one]
    if len(dircomp.common_dirs) > 0:
        for item in dircomp.common_dirs:
            compareme(os.path.abspath(os.path.join(dir1, item)), os.path.abspath(os.path.join(dir2, item)))
    return holderlist

def RCC():
    dir1 = "F:\Winservice\dir1"
    dir2 = "F:\Winservice\dir2"
    source_files = compareme(dir1, dir2)
    dir1 = os.path.abspath(dir1)
    destination_files = []
    createdir_bool = False
    for item in source_files:
        destination_dir = item.replace(dir1, dir2)
        destination_files.append(destination_dir)
        if os.path.isdir(item):
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
                createdir_bool = True
    if createdir_bool:
        destination_files = []
        source_files = []
        source_files = compareme(dir1, dir2)
        for item in source_files:
            destination_dir = item.replace(dir1, dir2)
            destination_files.append(destination_dir)
    # print ("update item:")
    # print (source_files)
    copy_pair = zip(source_files, destination_files)
    for item in copy_pair:
        if os.path.isfile(item[0]):
            shutil.copyfile(item[0], item[1])
#######################################################
##########Run Service#############
#######################################################
#encoding=utf-8
import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil


class TestService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SGSIService"
    _svc_display_name_ = "SGSI Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            RCC()
            # with open('F:\\TestService.log', 'a') as f:
            #     f.write('test service running...\n')
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(TestService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(TestService)
