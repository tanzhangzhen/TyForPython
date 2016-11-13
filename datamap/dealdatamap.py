# -*- coding=utf-8 -*-

import xml.etree.ElementTree as ET
import codecs
import os

"""
    2016-11-13 15:35 tzz
    #1、读取需要处理的文件，替换头部
    #2、处理后的文件写入临时文件中，接下来直接修改临时文件(不改变源文件)
    #3、遍历节点，处理数据
    #4、写入文件
    # tag节点名称cell attrib属性  cell的属性 {Value:"ajirdm"}
"""
    
def dealxmlTree(filename,newPrcscd):
    #xml读取临时文件
    tree = ET.parse(filename)
    root = tree.getroot()#取根节点
    
    #写入文件使用 将table节点添加到tables节点下
    tablesNodes = ET.Element(root.tag,root.attrib)#向需要写入的文件添加源节点
    tablesOld = ET.Element(root.tag,root.attrib)
    tablesNew = ET.Element(root.tag,root.attrib)
    
    tableOld = ET.SubElement(tablesOld, "table",{"Name":"ECI_TO_AFA_HEAD"})
    tablesOld.extend(tableOld)
    
    tableNew = ET.SubElement(tablesNew, "table",{"Name":"ECI_TO_AFA_HEAD"})
    tablesNew.extend(tableNew)
    
    #递归遍历节点
    sunroot(root, newPrcscd, tablesNodes, tableOld, tableNew)
    
    #写文件
    writeXmlFile(tablesNodes, tempFileName)
    writeXmlFile(tablesOld, datamapOld)
    writeXmlFile(tablesNew, datamapNew)
    
def writeXmlFile(tree, fileName):
    ET.ElementTree(tree).write(fileName, "GB2312", True, None, "xml")
    
def sunroot(root, newPrcscd, tablesNodes, tableOld, tableNew):
    i = 0 #计数变量
    flagChildNode = 0 #是否找到的通讯码prcscd标识
    cellSet = [] #通讯码相关一整块cell集合
    tradeFlag = '2' #勾兑变量
    
    if len(root) > 0:
        for childnode in root:
            i = i + 1
            for key in childnode.attrib:
                if childnode.attrib[key] in newPrcscd:
                    tree1["temp"]  =  childnode.attrib[key]#中间变量，保存cell的值，会从上往下依次读cell
                    cellSet.append(childnode.attrib[key])
                    flagChildNode = 1 #cell子节点找到标识，接下来会循环装这个prcscd的其他节点
            if flagChildNode == 1:
                cellSet.append(childnode.attrib[key]) #通讯码相关一整块cell装入集合

                #if i == 3 and childnode.attrib[key] == 'params':  #前置模板  
                #if i == 4 and childnode.attrib[key] == 'regfly':  #前置交易码
                #if i == 5 and childnode.attrib[key] == '01':  #渠道标识sysid
                #if i == 8 and childnode.attrib[key] == '0':  #勾兑标识      
                    #tree1["changePrcscd"].append(tree1["temp"])
                    #childnode.attrib[key] = tradeFlag #修改勾兑标识
                #if i == 9 and childnode.attrib[key] == '0':  #通讯去向cnttohst
                #if i == 11:  #通讯名称 提入借记复核错账处理
                    #tree1["changePrcscd"].append(childnode.attrib[key])
                    #tree1["change"].append(childnode.attrib[key])
                    #tree1["changePrcscd"].append(tree1["temp"]+" "+childnode.attrib[key].decode('utf-8').encode('gbk'))
                if i > 11:
                    rowOld = ET.SubElement(tableOld,"Row",{})
                    tableOld.extend(rowOld)
                    rowNew = ET.SubElement(tableNew,"Row",{})
                    tableNew.extend(rowNew)
                    j = 0
                    for x in cellSet:
                        j += 1
                        if j  ==  8:
                            valueNew = ET.SubElement(rowNew, childnode.tag,{'Value':tradeFlag})
                            rowNew.extend(valueNew)
                        else:
                            valueNew = ET.SubElement(rowNew, childnode.tag,{'Value':x})
                            rowNew.extend(valueNew)
                            
                        valueOld=ET.SubElement(rowOld, childnode.tag, {'Value':x})
                        rowOld.extend(valueOld)
                        
                    #当通讯码相关一整块cell集合处理完毕，找到通讯码的标识置为0 cell集合置空
                    flagChildNode  =  0 
                    cellSet = [] 
                    
            tableNodes = ET.SubElement(tablesNodes, childnode.tag, childnode.attrib)
            tablesNodes.extend(tableNodes)
            sunroot(childnode, newPrcscd, tableNodes, tableOld, tableNew)
        
            
if(__name__  ==  '__main__'):
    
    filepath = "../"#"/Users/tanzhangzhen/Downloads/workspace/TyForPython/"

    #读文件获取要处理的通讯码
    filePrcscd = filepath + "prcscd.txt"
    cntfile = open(filePrcscd, "r")
    contents = cntfile.read();
    newPrcscd = contents.split('\r\n')
    print "需要处理的通讯码个数" + str(len(newPrcscd)) + str(newPrcscd)
    cntfile.close()
    
    #codecs读取要处理的文件,读入时解码之后 替换头部为utf-8的(因为python只能处理utf-8格式的文件)
    fileDatamap = filepath + "datamap.map"
    readFileForText  =  codecs.open(fileDatamap, 'r', 'gb2312')#先读入文件再decode、encode不如直接codecs.open读入时解码
    text = readFileForText.read().encode('utf-8') #print text
    text = text.replace('GB2312','utf-8')
    readFileForText.close()
    
    #定义临时文件用于写入刚才替换头部的临时文件
    tempFileName = filepath + "datamap_ty.map"
    tempFile = open(tempFileName, 'w')
    tempFile.write(text)
    tempFile.close()
    
    datamapOld = filepath + "datamapOld.map"
    datamapNew = filepath + "datamapNew.map"
    
    #处理数据
    tree1 = {}
    tree1["changePrcscd"] = []
    dealxmlTree(tempFileName, newPrcscd)
    print "处理的通讯码个数" +str(len(tree1["changePrcscd"])) + str(tree1["changePrcscd"])
