#Sources:
# https://www.youtube.com/watch?v=V721K9M7PZM
# https://pchtsp.github.io/pytups/pulp.html


from pulp import *
import pytups as pt

f = open('Dataset1.txt', 'r').read()
f= f.replace("\n", " ")
f = f.split(" ",)

surglist=[]
for i in range(4,round((len(f))/2+2)):
    print(f[i])
    index=i-4
    surglist.append([int(f[2*index+4]),int(f[2*index+5])])
    # surglist.append(int(f[2*index+5]))

sortedsurglist= sorted(surglist, key=lambda x:x[1])
print(sortedsurglist)

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

status = prob.solve()

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
                if(i!=0):
                    resultLog+= newName[i]+" "
                else:
                    resultLog += str(int(newName[i])+1) + " "
            resultLog+= '\n'

print(resultLog)

with open('SolutionDataset1Group0.txt', 'w') as fp:
    fp.write(resultLog)