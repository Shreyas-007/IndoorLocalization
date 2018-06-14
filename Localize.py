'''
Created : 11/11/2017
Authors : Shreyas Jayaram, Bhaskar Bishnoi
'''

import iwlist
from time import sleep, gmtime, strftime
import time,os
import radioMap as radioMap
import numpy as np
from scipy.stats import mstats

testDict = dict()

for tries in range(1,11):

    terminate=False

    while not terminate: 
        print("----------------------Try "+str(tries)+"/10-------------------------------")
        content = iwlist.scan(interface='wlp3s0')
        cells = iwlist.parse(content)
        
        newDict = dict()
        newList = list()

        for dicts in cells:
            newDict = dict()
            newDict["Try"]=str(tries)

            for key, value in dicts.items():
                if key=="mac":
                    newDict["MAC Address"]=value
                if key=="signal_level_dBm":
                    newDict["Signal Level"]=value
                if key=="cellnumber":
                    newDict["Cell Number"]=value
            newList.append(newDict)
            testDict[tries]=newList

        if len(newList)>5:
            terminate=True
            break

        print("Data not captured. Pausing for 3s and recapturing data....")
        sleep(3)
    sleep(10)

testMap = dict()

for k,v in testDict.iteritems():
    tmpList=list()
    for n in v:
        tmpList.append((n['Signal Level'],n['MAC Address']))
    testMap[k]=tmpList

# list all the unique AP's in entire data capture set
uniqueSet = set()

for k,v in testMap.iteritems():
    for i in v:
        uniqueSet.add(i[1])
            
uniqueAps = list(uniqueSet)

mList=dict()
fDict=dict()

for a in uniqueAps:
    tempList=list()
    for v in testMap.values():
        for n in v:
            if(n[1]==a):
                tempList.append(int(n[0]))

    if len(tempList)>1:
        mList[a]=tempList

arr = mList.values()
arr.sort(key=len,reverse=True)
arr = arr[:30]
    
for k,v in mList.iteritems():
    for e in arr:
        if v==e:
            npArr = np.array(v)
            mean = round(np.mean(npArr),2)
            stddev = round(np.std(npArr),2)
            mode = int(mstats.mode(v)[0][0])
            fDict[k] = [mean,stddev,mode]
                
radioMap=radioMap.radioMap

mac = fDict.keys()
countDict = dict()

for k,v in radioMap.iteritems():
    count=0
    for k2,v2 in v.iteritems():
        if k2 in mac:
            count=count+1
    countDict[k]=count

big=0

for k,v in countDict.iteritems():    
    if(v>big):
        result=(k,v)
        big=v

macthingAp = list()
for k,v in countDict.iteritems():    
    if(v<=big):
        result=(v,k)
    macthingAp.append(result)

a = [x[1] for x in sorted(macthingAp,reverse=True)[:10]]

from math import sqrt

mEucl = dict()

for loc in a:
    euclDist=dict()
    tempDict = radioMap[loc]
    for k,v in tempDict.iteritems():
        for k2,v2 in fDict.iteritems():
            if k2==k:
                euclDist[k]=[sqrt(abs(pow(v2[0],2)-pow(v[0],2))),sqrt(abs(pow(v2[1],2)-pow(v[1],2))),sqrt(abs(pow(v2[2],2)-pow(v[2],2)))]
    mEucl[loc]=euclDist

distDict=dict()

for k,v in mEucl.iteritems():
    
    mean=list()
    stddev=list()
    mode=list()
    
    for x in v.values():
        mean.append(x[0])
        stddev.append(x[1])
        mode.append(x[2])

    m1 = np.array(mean)
    m2 = np.array(stddev)
    m3 = np.array(mode)

    d1 = min(mean)
    d2 = min(stddev)
    d3 = min(mode)

    distDict[k]=[d1,d2,d3]

meanD = list()
stdD = list()
modeD = list()

for x in distDict.values():
    meanD.append(x[0])
    stdD.append(x[1])
    modeD.append(x[2])
    
print min(meanD)
print  min(stdD)
print min(modeD)

closestMatch=list()
for k,v in distDict.iteritems():
    if(min(mean)==v[0] or min(stdD)==v[1] or min(modeD)==v[2]):
        closestMatch.append(k)
    
