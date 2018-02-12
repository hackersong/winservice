# 使用方法：python RTCopy.py dir1 dir2
# 程序会对比并复制dir1的文件到dir2

import os, sys
import filecmp
import re
import shutil
holderlist = []

#递归获取更新项函数
def compareme(dir1, dir2):
    dircomp = filecmp.dircmp(dir1, dir2)
    #源目录新文件或目录
    only_in_one = dircomp.left_only
    #不匹配文件，源目录文件已发生变化
    diff_in_one = dircomp.diff_files
    #定义源目录的绝对路径
    dirpath = os.path.abspath(dir1)
    #将更新文件名或目录追加到holderlist
    [holderlist.append(os.path.abspath(os.path.join(dir1, x))) for x in only_in_one]
    [holderlist.append(os.path.abspath(os.path.join(dir1, x))) for x in diff_in_one]
    #判断是否存在相同子目录，以便递归
    if len(dircomp.common_dirs) > 0:
        #递归子目录
        for item in dircomp.common_dirs:
            compareme(os.path.abspath(os.path.join(dir1, item)), os.path.abspath(os.path.join(dir2, item)))
        
    return holderlist

def main():
    dir1 = "dir1"
    dir2 = "dir2"
    #要求输入源目录和备份目录
    # if len(sys.argv) > 2:
    #     dir1 = sys.argv[1]
    #     dir2 = sys.argv[2]
    # else:
    #     print("请输入源目录和备份目录")
        #sys.exit()
        
        #下面的代码是测试代码，测试完毕后注释掉
        #-------------测试目录开始------------------
        #dir1 = "D:/data/dir1"
        #dir2 = "D:/data/dir2"
        #-------------测试目录结束------------------
    
    #对比源目录和备份目录
    source_files = compareme(dir1, dir2)
    dir1 = os.path.abspath(dir1)
    #备份目录路径加'/'
    #if not dir2.endswith('/'): dir2 = dir2 + '/'
    destination_files = []
    createdir_bool = False
    
    #遍历返回的差异文件或者目录清单
    for item in source_files:
        #将源目录差异路径清单对应替换成备份目录
        #destination_dir = re.sub(dir1, dir2, item)
        destination_dir = item.replace(dir1, dir2)
        #print destination_dir
        destination_files.append(destination_dir)
        #如果差异路径为目录并且不存在，则在备份目录中创建
        if os.path.isdir(item):
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
                #再次调用compareme函数标记
                createdir_bool = True
        
    #重新调用compareme函数，重新遍历新创建的目录内容    
    if createdir_bool:
        destination_files = []
        source_files = []
        #调用compareme函数
        source_files = compareme(dir1, dir2)
        #获取源目录差异路径清单，对用替换成备份目录
        for item in source_files:
            #destination_dir = re.sub(dir1, dir2, item)
            destination_dir = item.replace(dir1, dir2)
            destination_files.append(destination_dir)
    
    print ("update item:")
    #输出更新项列表清单
    print (source_files)
    #将源目录与备份目录文件清单拆分成元祖
    copy_pair = zip(source_files, destination_files)
    for item in copy_pair:
        #判断是否为文件，是则进行复制操作
        if os.path.isfile(item[0]):
            shutil.copyfile(item[0], item[1])
            
            
if __name__ == '__main__':
    main()
