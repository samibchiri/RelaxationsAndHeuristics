#Sources:
# https://www.youtube.com/watch?v=V721K9M7PZM
# https://pchtsp.github.io/pytups/pulp.html


from pulp import *
from pulp import HiGHS
import pytups as pt
import highspy
import numpy as np
import bisect

f = open('Dataset3.txt', 'r').read()
f= f.replace("\n", " ")
f = f.split(" ",)

surglist=[]
for i in range(4,round((len(f))/2+2)):
    # print(f[i])
    index=i-4
    surglist.append([int(f[2*index+4]),int(f[2*index+5])])
    # surglist.append(int(f[2*index+5]))

num_rooms= int(f[0])
num_days= int(f[1])
num_surg= int(f[2])
cap= int(f[3])

sortedsurglist= sorted(surglist, key=lambda x:x[1], reverse=True)
print("Sorted",cap,sortedsurglist)

CapBuckets=[]
AvailibleSurg=[]

CutoffPercentile=0.2
HardCutoff=50

Cutoff=min(CutoffPercentile*num_surg,100)


BucketIndices=[]
for surg in sortedsurglist:
    AvailibleSurg.append(surg)

for i in range(num_rooms*num_days):
    CapBuckets.append(cap)
    BucketIndices.append([])

usedSurgList=[]
notUsedSurgList=[]
for i in range(len(AvailibleSurg)):
    notUsedSurgList.append(AvailibleSurg[i][0])

def PopulateBuckets(FillTolerance,GoodFillTolerance):
    for i in range(len(CapBuckets)):
        for j in range(len(AvailibleSurg)):

            tempSurg = AvailibleSurg[j][1]
            if ((num_surg-len(usedSurgList))>Cutoff and AvailibleSurg[j][0] not in usedSurgList):
                # print(j,CapBuckets[i],tempSurg,AvailibleSurg[j])
                # print("Check",AvailibleSurg[j][1],CapBuckets[i],[i,j])

                lowestBucketCap=100000
                StartDayIndex = int(np.floor(i / num_rooms) * num_rooms)
                for n in range(num_rooms):
                    if(CapBuckets[StartDayIndex+n]<lowestBucketCap):
                        lowestBucketCap=CapBuckets[StartDayIndex+n]



                if (tempSurg >= cap and cap == CapBuckets[i]):
                    # print("Pass1",[i,j])
                    CapBuckets[i] -= tempSurg
                    usedSurgList.append(AvailibleSurg[j][0])
                    BucketIndices[i].append(AvailibleSurg[j][0])
                    notUsedSurgList.remove(AvailibleSurg[j][0])
                elif (CapBuckets[i] - tempSurg >= lowestBucketCap):
                    # print("Pass2", [i, j])
                    CapBuckets[i] -= tempSurg
                    usedSurgList.append(AvailibleSurg[j][0])
                    BucketIndices[i].append(AvailibleSurg[j][0])
                elif (CapBuckets[i] - tempSurg >= FillTolerance and AvailibleSurg[j][0] not in usedSurgList):
                    # print("Pass3", [i, j])
                    CapBuckets[i] -= tempSurg
                    usedSurgList.append(AvailibleSurg[j][0])
                    BucketIndices[i].append(AvailibleSurg[j][0])
                    notUsedSurgList.remove(AvailibleSurg[j][0])
                elif (AvailibleSurg[j][0] not in usedSurgList):
                    j=CheckGoodNextFill(i, GoodFillTolerance,j)
                else:
                    print("Pass4", [i, j])

def CheckGoodNextFill(BucketIndex,GoodFillTolerance,currentIndex):

    remainingCap=CapBuckets[BucketIndex]
    lowestBucketCap = 100000
    StartDayIndex = int(np.floor(BucketIndex / num_rooms) * num_rooms)
    for n in range(num_rooms):
        if (CapBuckets[StartDayIndex + n] < lowestBucketCap):
            lowestBucketCap = CapBuckets[StartDayIndex + n]

    if(lowestBucketCap<0):
        remainingCap=CapBuckets[BucketIndex]-lowestBucketCap

    MiddleIndex=-1
    for i in range(len(AvailibleSurg)):
        if(AvailibleSurg[i][0] not in usedSurgList):
            if (remainingCap - AvailibleSurg[i][1])<=GoodFillTolerance:
                if((remainingCap-AvailibleSurg[i][1])>=0):
                    print("BiggestChosen",CapBuckets[BucketIndex], AvailibleSurg[i][1])
                    CapBuckets[BucketIndex]-=AvailibleSurg[i][1]
                    usedSurgList.append(AvailibleSurg[i][0])
                    BucketIndices[BucketIndex].append(AvailibleSurg[i][0])
                    notUsedSurgList.remove(AvailibleSurg[i][0])
                    return 0

            if(AvailibleSurg[i][1]<remainingCap/2 and MiddleIndex==-1):
                MiddleIndex=i
                # print("Middle",MiddleIndex,AvailibleSurg[i-1][1],AvailibleSurg[i][1],remainingCap/2)

    if(MiddleIndex==-1):
        return currentIndex

    for i in range(max(0,MiddleIndex-20), MiddleIndex):
        for j in range(MiddleIndex,min(MiddleIndex+20,len(AvailibleSurg))):
    # for i in range(0, MiddleIndex):
    #     for j in reversed(range(MiddleIndex, len(AvailibleSurg))):

            if (AvailibleSurg[i][0] not in usedSurgList and AvailibleSurg[j][0] not in usedSurgList):
                # print("CheckNotTooSmall",AvailibleSurg[j][1],sortedsurglist[round(-len(sortedsurglist)/5)][1],len(sortedsurglist)/5,sortedsurglist)
                if(AvailibleSurg[j][1]>sortedsurglist[round(-len(sortedsurglist)/5)][1]):
                    if (AvailibleSurg[i][1] < sortedsurglist[round(len(sortedsurglist) / 5)][1]):
                        if(remainingCap -(AvailibleSurg[i][1]+AvailibleSurg[j][1])<=GoodFillTolerance):
                            if(remainingCap -(AvailibleSurg[i][1]+AvailibleSurg[j][1])>=0):

                                print("MiddleChosen",remainingCap,GoodFillTolerance,AvailibleSurg[i][1],AvailibleSurg[j][1])
                                # print("LengthLists",len(usedSurgList),num_surg-len(notUsedSurgList))
                                CapBuckets[BucketIndex] -= AvailibleSurg[j][1]
                                usedSurgList.append(AvailibleSurg[j][0])
                                BucketIndices[BucketIndex].append(AvailibleSurg[j][0])
                                notUsedSurgList.remove(AvailibleSurg[j][0])
                                CapBuckets[BucketIndex] -= AvailibleSurg[i][1]
                                usedSurgList.append(AvailibleSurg[i][0])
                                BucketIndices[BucketIndex].append(AvailibleSurg[i][0])
                                notUsedSurgList.remove(AvailibleSurg[i][0])
                                return 0

    return currentIndex



PopulateBuckets(cap/5,0)

# PopulateBuckets(cap/5)

if(num_surg-len(usedSurgList)>HardCutoff):
    print("Relaxation1",len(usedSurgList),num_surg)
    PopulateBuckets(cap/5,1)

if(num_surg-len(usedSurgList)>HardCutoff):
    print("Relaxation2",len(usedSurgList),num_surg)
    PopulateBuckets(0,cap/200)

if(num_surg-len(usedSurgList)>HardCutoff):
    print("Relaxation3",len(usedSurgList),num_surg)
    PopulateBuckets(-cap/50,cap/200)

if(num_surg-len(usedSurgList)>HardCutoff):
    print("Relaxation4",len(usedSurgList),num_surg)
    PopulateBuckets(-cap/20,cap/200)

if(num_surg-len(usedSurgList)>HardCutoff):
    print("Relaxation5",len(usedSurgList),num_surg)
    PopulateBuckets(-cap/10,cap/200)

if(num_surg-len(usedSurgList)>HardCutoff):
    print("Relaxation6",len(usedSurgList),num_surg)
    PopulateBuckets(-cap/5,cap/100)



print("UsedSurg",usedSurgList,len(usedSurgList),num_surg)
print("CapBuckets",min(CapBuckets),CapBuckets)
print("NotUsedSurg",max(notUsedSurgList),notUsedSurgList)

total=0
totalCap=num_days*num_rooms*cap
for i in AvailibleSurg:
    total+=i[1]
print("TotalSum",total,totalCap,num_days*num_rooms)
print("BestCase",(total-totalCap)/(num_days*num_rooms))
print("RemainingSurg",num_surg,len(usedSurgList),num_surg-len(usedSurgList))

print("BucketIndices",BucketIndices)

FixedX_irt=[]

for i in range(num_surg):
    FixedX_irt.append([])
    for r in range(num_rooms):
        FixedX_irt[i].append([])
        for t in range(num_days):
            FixedX_irt[i][r].append(0)

# print("Numbs",num_surg,num_rooms,num_days)

for i in range(len(BucketIndices)):
    for j in range(len(BucketIndices[i])):
        # print("Wut",i,len(FixedX_irt[i][i%2]),[i,j],len(FixedX_irt))
        FixedX_irt[BucketIndices[i][j]-1][i%num_rooms][int(np.floor(i/num_rooms))]=1

# print("FixedIRT",FixedX_irt[4][1][0],FixedX_irt)

# for i in range(len(AvailibleSurg)):
#     if(AvailibleSurg[i][0] not in usedSurgList):
#         print("NotIn",AvailibleSurg[i][1],AvailibleSurg[i][0])


prob = LpProblem("Problem_1", LpMinimize)

# x= LpVariable.dicts("x", [1,2], lowBound=0, cat="Integer")

# print(x)


#Variables

num_rooms= int(f[0])
num_days= int(f[1])
num_surg= int(f[2])
cap= int(f[3])


#Decision Variables
IRT = pt.TupList((i, r, t) for i in range(num_surg) for r in range(num_rooms) for t in range(num_days))

X_irt = pulp.LpVariable.dicts(
    name="Decision", indices=IRT, lowBound=0, upBound=1, cat="Binary"
)


#Other Variables

RT= pt.TupList((r, t) for r in range(num_rooms) for t in range(num_days))

T = pt.TupList((t) for t in range(num_days))

O_rt = pulp.LpVariable.dicts(
    name="Overtime", indices=RT, lowBound=0, cat="Integer"
)
M_t = pulp.LpVariable.dicts(
    name="MaxOvertime", indices=T, lowBound=0, cat="Integer"
)

#Constraints


for r in range(num_rooms):
    for t in range(num_days):
        prob += pulp.lpSum(X_irt[i,r,t]*surglist[i][1] for i in range(num_surg))<= cap + O_rt[r,t]

for i in range(num_surg):
    prob += pulp.lpSum(X_irt[i,r,t] for r in range(num_rooms) for t in range(num_days))==1

for r in range(num_rooms):
    for t in range(num_days):
        prob+= M_t[t]>=O_rt[r,t]

#Heuristic Constraint


for i in range(num_surg):
    for r in range(num_rooms):
        for t in range(num_days):
            prob+= X_irt[i,r,t]>=FixedX_irt[i][r][t]

#Objective function
prob+= lpSum(M_t[t] for t in range(num_days))

status = prob.solve(HiGHS(msg=True))

print(status)

resultLog=""

resultLog+="Obj "+ str(round(pulp.value(prob.objective)))
resultLog+='\n'
resultLog+="Surgery Day OR"
resultLog+='\n'

for var in prob.variables():
    # print(f"{var.name} =",  "cat =", var.cat, var.varValue)
    # print(var.name[0])
    if(var.name[0]=="D"):
        if(var.varValue==1):
            newName=var.name.replace(")","").split("(")[1].split(",_")
            # print(newName)
            for i in range(len(newName)):
                if(i==0):
                    resultLog += str(int(newName[i]) + 1) + " "
                if(i==1):
                    resultLog+= newName[i+1]+" "
                if (i==2):
                    resultLog += newName[i-1] + " "
            resultLog+= '\n'



print(BucketIndices)
print(resultLog)

print(FixedX_irt[4][1][0])

with open('SolutionDataset1Group0.txt', 'w') as fp:
    fp.write(resultLog)