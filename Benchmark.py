#Sources:
# https://www.youtube.com/watch?v=V721K9M7PZM
# https://pchtsp.github.io/pytups/pulp.html


from pulp import *
import pytups as pt

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

CutoffPercentile=0.5
HardCutoff=10

Cutoff=min(CutoffPercentile*num_surg,50)


BucketIndices=[]
for surg in sortedsurglist:
    AvailibleSurg.append(surg)
    BucketIndices.append([])

for i in range(num_rooms*num_days):
    CapBuckets.append(cap)

usedSurgList=[]


# print("LenCapBucjet",len(CapBuckets))

#
# for i in range(len(CapBuckets)):
#     for j in range(len(AvailibleSurg)):
#         # print("Bucket",i,j,Cutoff)
#         tempSurg=AvailibleSurg[j][1]
#         if((num_surg-len(usedSurgList))>Cutoff and AvailibleSurg[j][0] not in usedSurgList):
#             # print(j,CapBuckets[i],tempSurg,AvailibleSurg[j])
#             # print("Pass0",AvailibleSurg[j][1],CapBuckets[i],[i,j])
#             if (tempSurg >= cap and cap==CapBuckets[i]):
#                 # print("Pass1",[i,j])
#                 CapBuckets[i] -= tempSurg
#                 usedSurgList.append(AvailibleSurg[j][0])
#             elif(i%2==1 and CapBuckets[i]-tempSurg>=CapBuckets[i-1]):
#                 # print("Pass2", [i, j])
#                 CapBuckets[i] -= tempSurg
#                 usedSurgList.append(AvailibleSurg[j][0])
#             # if (i > 150):
#             #     print("Check", AvailibleSurg[j][1], CapBuckets[i], [i, j])
#             elif (CapBuckets[i] - tempSurg >= cap / 5):
#                 # print("Pass3", [i, j])
#                 # if (i > 150):
#                 #     print("Pass3", AvailibleSurg[j][1], CapBuckets[i], [i, j])
#                 CapBuckets[i] -= tempSurg
#                 usedSurgList.append(AvailibleSurg[j][0])
#             # else:
#             #     print("Pass4", [i, j])





def PopulateBuckets(FillTolerance):
    print("Relaxation1",len(usedSurgList),num_surg)
    for i in range(len(CapBuckets)):
        for j in range(len(AvailibleSurg)):
            tempSurg = AvailibleSurg[j][1]
            if ((num_surg-len(usedSurgList))>Cutoff and AvailibleSurg[j][0] not in usedSurgList):
                # print(j,CapBuckets[i],tempSurg,AvailibleSurg[j])
                # print("Check",AvailibleSurg[j][1],CapBuckets[i],[i,j])
                if (tempSurg >= cap and cap == CapBuckets[i]):
                    # print("Pass1",[i,j])
                    CapBuckets[i] -= tempSurg
                    usedSurgList.append(AvailibleSurg[j][0])
                elif (i % 2 == 1 and CapBuckets[i] - tempSurg >= CapBuckets[i - 1]):
                    # print("Pass2", [i, j])
                    CapBuckets[i] -= tempSurg
                    usedSurgList.append(AvailibleSurg[j][0])
                elif (CapBuckets[i] - tempSurg >= FillTolerance):
                    # print("Pass3", [i, j])
                    CapBuckets[i] -= tempSurg
                    usedSurgList.append(AvailibleSurg[j][0])
                # else:
                #     print("Pass4", [i, j])

PopulateBuckets(cap/5)

if(num_surg-len(usedSurgList)>HardCutoff):
    PopulateBuckets(0)

if(num_surg-len(usedSurgList)>HardCutoff):
    PopulateBuckets(-cap/50)

if(num_surg-len(usedSurgList)>HardCutoff):
    PopulateBuckets(-cap/20)

if(num_surg-len(usedSurgList)>HardCutoff):
    PopulateBuckets(-cap/10)

if(num_surg-len(usedSurgList)>HardCutoff):
    PopulateBuckets(-cap/5)


notUsedSurgList=[]
for i in range(len(AvailibleSurg)):
    if(AvailibleSurg[i][0] not in usedSurgList):
        notUsedSurgList.append(AvailibleSurg[i][0])
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

# for i in range(len(AvailibleSurg)):
#     if(AvailibleSurg[i][0] not in usedSurgList):
#         print("NotIn",AvailibleSurg[i][1],AvailibleSurg[i][0])


prob = LpProblem("Problem_1", LpMinimize)

x= LpVariable.dicts("x", [1,2], lowBound=0, cat="Integer")

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

for i in range(num_surg):
    prob += pulp.lpSum(X_irt[i,r,t] for r in range(num_rooms) for t in range(num_days))==1

for r in range(num_rooms):
    for t in range(num_days):
        prob += O_rt[r,t]>=0

for t in range(num_days):
    prob += M_t[t] >= 0

#Objective function
prob+= lpSum(M_t[t] for t in range(num_days))
#
# status = prob.solve()
#
# print(status)
#
# resultLog=""
#
# resultLog+="Obj "+ str(round(pulp.value(prob.objective)))
# resultLog+='\n'
# resultLog+="Surgery Day OR"
# resultLog+='\n'
#
# for var in prob.variables():
#     # print(f"{var.name} =",  "cat =", var.cat, var.varValue)
#     # print(var.name[0])
#     if(var.name[0]=="D"):
#         if(var.varValue==1):
#             newName=var.name.replace(")","").split("(")[1].split(",_")
#             # print(newName)
#             for name in newName:
#                 resultLog+= name+" "
#             resultLog+= '\n'
#
# # print(resultLog)
#
# with open('SolutionDataset1Group0.txt', 'w') as fp:
#     fp.write(resultLog)