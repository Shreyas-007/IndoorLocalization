
# coding: utf-8

# In[16]:


import iwlist
from time import sleep, gmtime, strftime
import time,os
import radioMap as radioMap
import numpy as np
from scipy.stats import mstats

testDict = dict()

for tries in range(1,11):

    # sleep(delay)
    terminate=False

    while not terminate: 
        print("----------------------Try "+str(tries)+"/10-------------------------------")
        #sleep(1)


        # data = open('Iwlist_wlp3s0_Params.txt','a')
        # data.flush()


        content = iwlist.scan(interface='wlp3s0')
        cells = iwlist.parse(content)
        #print(cells)	

        newDict = dict()
        newList = list()


        for dicts in cells:
            newDict = dict()
    #             newDict["Time"]=
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

        print "Data not captured. Pausing for 3s and recapturing data...."
        sleep(3)
    sleep(10)
        
#         testDict[tries]=newList




# In[17]:


newList[0]


# In[18]:


len(newList)


# In[21]:


for i in range(1,11):
    print(testDict[i][0])


# In[22]:


testDict


# In[23]:


testMap = dict()

for k,v in testDict.iteritems():
    tmpList=list()
    for n in v:
        tmpList.append((n['Signal Level'],n['MAC Address']))
    testMap[k]=tmpList


# In[24]:


testMap


# In[27]:


len(testMap[1])


# In[28]:


# list all the unique AP's in entire data capture set
uniqueSet = set()


for k,v in testMap.iteritems():
    for i in v:
        uniqueSet.add(i[1])
            
uniqueAps = list(uniqueSet)


# In[80]:


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
    
#     comment starts here
for k,v in mList.iteritems():
    for e in arr:
        if v==e:
            npArr = np.array(v)
            mean = round(np.mean(npArr),2)
            stddev = round(np.std(npArr),2)
            mode = int(mstats.mode(v)[0][0])
            fDict[k] = [mean,stddev,mode]
                
# comment ends here

    #     arr = arr[:30]

#     newDict=dict()
#     for k,v in mList.iteritems():
#         npArr = np.array(v)
# #                 fltArr = [float(x) for x in v]
#         mean = round(np.mean(npArr),2)
#         stddev = round(np.std(npArr),2)
#         mode = int(mstats.mode(v)[0][0])
# #                 print fltArr
# #                 mode = round(mode(v),2)
#         newDict[k] = [mean,stddev,mode]


# In[81]:


mList


# In[82]:


fDict


# In[83]:


# tLocMap = dict()

# for k,v in newDict.iteritems():
#     if len(k)<17:
#         continue
#     tLocMap[k]=v


# In[89]:


radioMap=radioMap.radioMap


# In[90]:


mac = fDict.keys()


# In[91]:


mac


# In[92]:


countDict = dict()

for k,v in radioMap.iteritems():
    count=0
    for k2,v2 in v.iteritems():
        if k2 in mac:
            count=count+1
    countDict[k]=count


# In[93]:


countDict


# In[94]:


big=0

for k,v in countDict.iteritems():    
    if(v>big):
        result=(k,v)
        big=v


# In[96]:


macthingAp = list()
for k,v in countDict.iteritems():    
    if(v<=big):
        result=(v,k)
    macthingAp.append(result)


# In[97]:


sorted(macthingAp,reverse=True)


# In[98]:


a = [x[1] for x in sorted(macthingAp,reverse=True)[:10]]


# In[99]:


a


# In[102]:


radioMap[118]


# In[110]:


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


# In[111]:


mEucl


# In[120]:



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
#     d1 = np.amin(m1)
    d1 = min(mean)
    d2 = min(stddev)
    d3 = min(mode)
#     d2 = np.amin(m2)
#     d3 = np.amin(m3)
    distDict[k]=[d1,d2,d3]


# In[121]:


mean


# In[122]:


distDict


# In[127]:


meanD = list()
stdD = list()
modeD = list()

for x in distDict.values():
    meanD.append(x[0])
    stdD.append(x[1])
    modeD.append(x[2])
    
meanD
print min(meanD)
print  min(stdD)
print min(modeD)


# In[128]:


closestMatch=list()
for k,v in distDict.iteritems():
    if(min(mean)==v[0] or min(stdD)==v[1] or min(modeD)==v[2]):
        closestMatch.append(k)
    


# In[129]:


closestMatch


# In[131]:


print(closestMatch)

for k,v in distDict.iteritems():
	print(k,v)

