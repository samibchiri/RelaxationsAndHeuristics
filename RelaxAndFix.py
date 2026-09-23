#Sources:
# https://www.youtube.com/watch?v=V721K9M7PZM
# https://pchtsp.github.io/pytups/pulp.html


from pulp import *
import pytups as pt

f = open('Dataset2.txt', 'r').read()
f= f.replace("\n", " ")
f = f.split(" ",)

surglist=[]
for i in range(4,round((len(f))/2+2)):
    # print(f[i])
    index=i-4
    surglist.append([int(f[2*index+4]),int(f[2*index+5])])
    # surglist.append(int(f[2*index+5]))

sortedsurglist= sorted(surglist, key=lambda x:x[1])
print("SortedList",sortedsurglist)





def ILPFormulation(IntSurgeryList,HeuristicBound):


    prob = LpProblem("Problem_1", LpMinimize)

    x= LpVariable.dicts("x", [1,2], lowBound=0, cat="Continuous")

    # print(x)


    #Variables

    num_rooms= int(f[0])
    num_days= int(f[1])
    num_surg= int(f[2])
    cap= int(f[3])


    #Decision Variables
    IRT = pt.TupList((i, r, t) for i in range(num_surg) for r in range(num_rooms) for t in range(num_days))

    if(len(IntSurgeryList)>0):
        X_irt = pulp.LpVariable.dicts(
            name="Decision", indices=IRT, lowBound=0, upBound=1, cat="Integer"
        )
    else:
        X_irt = pulp.LpVariable.dicts(
            name="Decision", indices=IRT, lowBound=0, upBound=1, cat="Continuous"
        )


    #Other Variables

    RT= pt.TupList((r, t) for r in range(num_rooms) for t in range(num_days))

    T = pt.TupList((t) for t in range(num_days))

    I = pt.TupList((i) for i in range(num_surg))

    O_rt = pulp.LpVariable.dicts(
        name="Overtime", indices=RT, lowBound=0, cat="Continuous"
    )
    M_t = pulp.LpVariable.dicts(
        name="MaxOvertime", indices=T, lowBound=0, cat="Continuous"
    )

    F_irt = pulp.LpVariable.dicts(
        name="Forcing", indices=IRT, lowBound=0, upBound=1, cat="Binary"
    )

    M=10
    #Constraints


    for r in range(num_rooms):
        for t in range(num_days):
            prob += pulp.lpSum(X_irt[i,r,t]*surglist[i][1] for i in range(num_surg))<= cap + O_rt[r,t]

    for i in range(num_surg):
        prob += pulp.lpSum(X_irt[i,r,t] for r in range(num_rooms) for t in range(num_days))==1
        if(len(IntSurgeryList)>0):
            if(IntSurgeryList[i]!=0):
                prob+= X_irt[i,IntSurgeryList[i][1],IntSurgeryList[i][2]]>=1

        prob+= pulp.lpSum(F_irt[i,r,t] for r in range(num_rooms) for t in range(num_days))==1

        for r in range(num_rooms):
            for t in range(num_days):
                # prob+= X_irt[i,r,t]>= surglist[i][1]/cap - M*(1-F_irt[i,r,t])
                prob += X_irt[i, r, t] >= HeuristicBound- M * (1 - F_irt[i, r, t])


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

    IntegerSurgeryList=[]
    ContSurgeryList=[]

    CountZeros=num_surg
    for i in range(num_surg):
        IntegerSurgeryList.append(0)
        ContSurgeryList.append([])

    for var in prob.variables():
        # print(var.name[0])
        # print(f"{var.name} =",  "cat =", var.cat, var.varValue)
        if(var.name[0]=="D"):
            index=int(var.name.replace(")","").split("(")[1].split(",_")[0])
            newName = var.name.replace(")", "").split("(")[1].split(",_")
            if(var.varValue==1):
                # print(newName)
                for name in newName:
                    resultLog+= name+" "
                IntegerSurgeryList[index]=[int(newName[0]),int(newName[1]),int(newName[2])]
                resultLog+= '\n'
                CountZeros-=1
            elif(var.varValue>0):
                ContSurgeryList[index].append([var.varValue,int(newName[0]),int(newName[1]),int(newName[2])])

    # print(resultLog)
    # print(IntegerSurgeryList)
    if(0 in IntegerSurgeryList):
        print("Count",CountZeros,"Total",num_surg)
        return [IntegerSurgeryList,ContSurgeryList]
    else:
        return round(pulp.value(prob.objective))


HeuristicBoundList=[]
FinalResults=[]
for i in range(5):
    newHeuristic=0.7+i/5*0.3
    newHeuristic=1
    HeuristicBoundList.append(newHeuristic)
    FinalResults.append([newHeuristic])
    # HeuristicBoundList.append(0.95)
print("HeuristicBoundList",HeuristicBoundList)


for j in range(len(HeuristicBoundList)):

    IntSurgeryList = []
    for i in range(2):
        print("NewHeuristic",j,HeuristicBoundList[j])
        result = ILPFormulation(IntSurgeryList,HeuristicBoundList[j])
        # print("Result",result)
        if type(result)==int:
            FinalResults[j].append(result)
        else:
            IntSurgeryList=result[0]
            ContSurgeryList=result[1]
            print("ContList",ContSurgeryList)
            print("IntList",IntSurgeryList)

            for k in range(len(IntSurgeryList)):
                if(IntSurgeryList[k]==0):
                    for item in ContSurgeryList[k]:
                        print("Item",item)
                        if(item[0]>=HeuristicBoundList[j]):
                            IntSurgeryList[k]=[item[1],item[2],item[3]]
            print("NewIntList",IntSurgeryList)

print("FinalResults",FinalResults)