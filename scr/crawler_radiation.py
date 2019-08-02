#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 20:40:36 2019
@author: Yulong WANG
"""

from __future__ import unicode_literals
import os
import time
import arrow
import requests
import datetime
import numpy as np
from bs4 import BeautifulSoup

# https://www.data.jma.go.jp/gmd/env/data/radiation/data/geppo/201502/DR201502_tat.txt
# https://www.data.jma.go.jp/gmd/env/data/radiation/data/geppo/201502/DF201502_sap.txt
# https://www.data.jma.go.jp/gmd/env/data/radiation/data/geppo/201503/DL201503_fua.txt
# https://www.data.jma.go.jp/gmd/env/data/radiation/data/geppo/201412/DR201412_ish.txt
# https://www.data.jma.go.jp/gmd/env/data/radiation/data/geppo/201708/DR201708_mnm.txt

def getData(code1, code2, year, month):
    url_base = "https://www.data.jma.go.jp/gmd/env/data/radiation/data/geppo/"
    html = url_base + year + month + '/' + code1 + year + month + '_' + code2 + '.txt'
    response = requests.get(html, stream=True)
    soup = BeautifulSoup(response.content, 'html.parser')
    #body = soup.find('body',{'data-gr-c-s-loaded':'ture'})
    #data = response#.content
    return soup

def makeDir(path):
    if os.path.isdir(path):
        print('Folder exsiting.')
        pass
    else:
        print('Folder creating.')
        os.mkdir(path)
    return None

def clearFile(path, file):
    if os.path.isfile(path + file + '.dat'):
        os.remove(path + file + '.dat')
    return None

def writeFile(time, value, path, name):
    fid = open(path + name + '.txt', 'a')
    fid.write('{} '.format(value))
    fid.close()
    return None

def months(str1,str2):
    year1=str1.year
    year2=str2.year
    month1=str1.month
    month2=str2.month
    num=(year1-year2)*12+(month1-month2)
    return num

if __name__=="__main__":
    start = time.time() 
    code1list = np.array([\
                         ('直達日射','DR'), \
                         ('散乱日射','DL'), \
                         ('下向き赤外放射','DF'), \
                         ]) 
    code2list = np.array([\
                         #('札幌','SAPPORO','sap'), \
                         ('つくば(館野)','TSUKUBA','tat'), \
                         #('福岡','FUKUOKA','fua'), \
                         #('石垣島','ISHIGAKIJIMA','ish'), \
                         #('南鳥島','MINAMITORISHIMA','mnm'), \
                         ]) 
    timelist = ['201401','201812']
    
    t0 = datetime.datetime.strptime(timelist[0],'%Y%m')
    t1 = datetime.datetime.strptime(timelist[1],'%Y%m')
    
    for i in range(len(code1list)):
        name1 = code1list[i][0]
        code1 = code1list[i][1]
        for j in range(len(code2list)):
            name2 = code2list[j][0]
            code2 = code2list[j][2]
            path = '../data/'
            print(name1 + '_' + name2 + ':')
            # makeDir(path)
            #clearFile(path, file)
            tt = arrow.get(str(t0), 'YYYY-MM-DD HH:mm:ss')
            for k in range(months(t1,t0) + 1):
                mm = tt.shift(months=+k).format("YYYYMM")
                file = code1 + '_' + mm + '_' + code2
                print('   ' + mm + ' ...')
                value = getData(code1, code2, mm[0:4], mm[4:7])
                writeFile(mm,value,path,file)
    total_time = time.time() - start
    print(u"Total time is：%f seconds" % total_time)
