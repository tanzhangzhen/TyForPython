# -*- coding:utf-8 -*-
import os,time
from dircache import listdir

def change_name(path):

    global i
    if not os.path.isdir(path) and not os.path.isfile(path):
        #print "非文件夹或者文件类型，不处理",path
        return False
    
    if os.path.isfile(path):
        #print "本次要处理的是文件",path
        file_path = os.path.split(path) #分割出目录与文件 
        lists = file_path[1].split('.') #分割出文件与文件扩展名
        file_ext = lists[-1] #取出后缀名(列表切片操作)
        img_ext = ['bmp','jpeg','gif','psd','png','jpg']#'bmp|jpeg|gif|psd|png|jpg'
        if file_ext in img_ext:
            i += 1 #注意这里的i是一个陷阱
            os.rename(path,file_path[0]+'/'+lists[0]+'_fc.'+file_ext)
            #print('ok---' + file_path[1])

    elif os.path.isdir(path):
        #print "本次要处理的是文件夹",path
        for x in os.listdir(path):
            #print os.path.join(path,x)
            i = i + 1
            change_name(os.path.join(path,x)) #'连接符'.join(list) 将列表组成字符串 
            #img_dir = 'D:\\xx\\xx\\images'
            #img_dir = img_dir.replace('\\','/')
            #change_name(img_dir)
    
    
if __name__ == '__main__':
    start = time.time()
    filepath = "../"#文件路径
    i = 0 #递归调用次数
    print "本次处理文件数" + str(len(listdir(filepath))) + str(listdir(filepath))
    change_name(filepath)
    print('总共处理了 %s 张图片'%(i))
    end = time.time()
    print('程序运行耗时:%0.2f'%(end - start))