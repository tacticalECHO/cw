import copy
import random
import re
import math
import time
import itertools
Problems = []
mutation_rate_N=0.3
k=2
class Item:
    def __init__(self,weight,id):
        self.weight=weight
        self.id=id
class problem:
    def __init__(self,name,capacity,numberofitems,items,Best_solution):
        self.name=name
        self.numberofitems=numberofitems
        self.items=items
        self.Best_solution=Best_solution
        self.knapsack_list=[Knapsack(capacity)]
        self.number_knapsack=0
        self.my_solution=None
class Knapsack:
    def __init__(self,capacity):
        self.capacity=capacity
        self.items=[]
    def add(self,item):
        self.items.append(item)
    def getWeight(self):
        return sum([item.weight for item in self.items])
    def getItems(self):
        return self.items
    def remove(self,item):
        self.items.remove(item)
    def clear(self):
        self.items=[]
class solution:
    def __init__(self,problem,number_knapsack=0):
        self.problem=problem
        self.knapsacks=[Knapsack(problem.knapsack_list[0].capacity)]
        self.fitness=0
        self.number_knapsack=number_knapsack     
def ReadFile(filename):
    with open(filename, 'r') as f:
        return f.read()
def dataProcess(filename):
    data=ReadFile(filename).split('\n')
    Num_Problem = int(data[0])
    index=0
    for i in range(1,Num_Problem+1):
        index+=1
        name=data[index]
        name=name.replace(' ','')
        number=re.findall('[0-9]+',data[index+1])
        Numberofitems=int(number[1])
        capacity=int(number[0])
        bestsloution=int(number[2])
        items=[]
        for j in range(1, Numberofitems+1):
            weight=re.findall('[0-9]+',data[index+j+1])
            weight=int(weight[0])
            items.append(Item(weight,j-1))
        Problems.append(problem(name,capacity,Numberofitems,items,bestsloution))
        index+=Numberofitems+1
def fitness(solution):
    solution.fitness=sum([pow(knapsack.getWeight()/knapsack.capacity,k) for knapsack in solution.knapsacks])/solution.number_knapsack
def Best_Fit(solution, items):
    items_in_order=sorted(items,key=lambda x:x.weight,reverse=True)
    for item in items_in_order:
        best_knapsack = None
        min_remain = float('inf')
        for knapsack in solution.knapsacks:
            remain = knapsack.capacity - knapsack.getWeight()
            if remain >= item.weight and remain < min_remain:
                best_knapsack = knapsack
                min_remain = remain

        if best_knapsack is not None:
            best_knapsack.add(item)
        else:
            new_knapsack = Knapsack(solution.problem.knapsack_list[0].capacity)
            new_knapsack.add(item)
            solution.knapsacks.append(new_knapsack)
            solution.number_knapsack = len(solution.knapsacks)  
def First_Fit(solution,items):
    items_in_order=sorted(items,key=lambda x:x.weight,reverse=True)
    for item in items_in_order:
        for knapsack in solution.knapsacks:
            if knapsack.getWeight()+item.weight<=knapsack.capacity:
                knapsack.add(item)
                break
        else:
            new_knapsack=Knapsack(solution.problem.knapsack_list[0].capacity)
            new_knapsack.add(item)
            solution.knapsacks.append(new_knapsack)
            solution.number_knapsack=len(solution.knapsacks)

def swap_items_solution(solution):
    kn_not_full=[kn for kn in solution.knapsacks if kn.getWeight()<kn.capacity]
    if len(kn_not_full)<2:
        return
    kn1=random.choice(kn_not_full)
    item1=random.choice(kn1.getItems())
    for kn in kn_not_full:
        if kn!=kn1:
            for item2 in kn.getItems():
                if item1.weight<item2.weight<=item1.weight*1.05 and kn1.getWeight()-item1.weight+item2.weight<=kn1.capacity:
                    kn.add(item1)
                    kn1.add(item2)
                    kn.remove(item2)
                    kn1.remove(item1)
                    return
def mutation(solution):
    number_of_mutation=math.ceil(solution.number_knapsack*mutation_rate_N)
    Kn_in_order_weight=sorted(solution.knapsacks,key=lambda x:x.getWeight())
    items=[]
    for i in range(number_of_mutation):
        items+=Kn_in_order_weight[i].getItems()
        solution.knapsacks.remove(Kn_in_order_weight[i])
        swap_items_solution(solution)
    Best_Fit(solution,items)
    solution.number_knapsack=len(solution.knapsacks)
    fitness(solution)
    return solution
    
def shift_item_large_knapsack(solution):
    kn_sorted=sorted(solution.knapsacks,key=lambda x:x.getWeight())
    maximum=kn_sorted[0]
    not_full_kn=[kn for kn in solution.knapsacks if kn.getWeight()<kn.capacity]
    if len(not_full_kn)==0:
        return
    change_kn=random.choice(not_full_kn)
    item_in_maximum=max(maximum.getItems(),key=lambda x:x.weight)
    item_in_change_kn=min(change_kn.getItems(),key=lambda x:x.weight)
    if change_kn!=maximum:
        if maximum.getWeight()-item_in_maximum.weight+item_in_change_kn.weight<=maximum.capacity and change_kn.getWeight()-item_in_change_kn.weight+item_in_maximum.weight<=change_kn.capacity:
            maximum.remove(item_in_maximum)
            change_kn.remove(item_in_change_kn)
            maximum.add(item_in_change_kn)
            change_kn.add(item_in_maximum)        
def Clear_null_knapsack(solution):
    for knapsack in solution.knapsacks:
        if len(knapsack.getItems())==0:
            solution.knapsacks.remove(knapsack)
    
def SimulatedAnnealing(problem):
    T=100
    T_min=0.1
    alpha=0.9
    current_solution=solution(problem)
    current_solution.number_knapsack=0
    current_solution.knapsacks=[Knapsack(problem.knapsack_list[0].capacity)]
    items_list=copy.deepcopy(problem.items)
    Best_Fit(current_solution,items_list)
    best_solution=copy.deepcopy(current_solution)
    while T>T_min:
        i=0
        while i<10:
            new_solution=copy.deepcopy(current_solution)
            mutation(new_solution)
            shift_item_large_knapsack(new_solution)
            swap_items_solution(new_solution)
            Clear_null_knapsack(new_solution)
            new_solution.number_knapsack=len(new_solution.knapsacks)
            delta_E=new_solution.number_knapsack-current_solution.number_knapsack
            if delta_E<0:
                current_solution=new_solution
                if current_solution.number_knapsack<best_solution.number_knapsack:
                    best_solution=copy.deepcopy(current_solution)
            else:
                if random.random()<math.exp(-delta_E/T):
                    current_solution=new_solution
            i+=1
        T*=alpha
    return best_solution
def PrintToFile(filename):
    with open(filename, 'w') as f:
        f.write(str(len(Problems))+'\n')
        for problem in Problems:
            f.write(problem.name+'\n')
            f.write(" "+"obj=   "+str(problem.my_solution.number_knapsack)+" 	 "+str(problem.my_solution.number_knapsack-problem.Best_solution)+'\n')
            for knapsack in problem.my_solution.knapsacks:
                #f.write(str(knapsack.getWeight())+' ')
                for item in knapsack.getItems():
                    f.write(str(item.id)+' ')
                f.write('\n')
    with open(filename+'copy', 'w') as f:
        f.write(str(len(Problems))+'\n')
        for problem in Problems:
            f.write(problem.name+'\n')
            f.write(" "+"obj=   "+str(problem.my_solution.number_knapsack)+" 	 "+str(problem.my_solution.number_knapsack-problem.Best_solution)+'\n')
            for knapsack in problem.my_solution.knapsacks:
                f.write(str(knapsack.getWeight())+' ')
                for item in knapsack.getItems():
                    f.write(str(item.id)+' '+str(item.weight)+' ')
                f.write('\n')
def main():
    dataProcess('test.txt')
    timeStart = time.time()
    for problem in Problems:
        best_solution=SimulatedAnnealing(problem)
        problem.my_solution=best_solution
    PrintToFile('output.txt')
    timeEnd = time.time()
    print('Time:',timeEnd-timeStart)
if __name__ == '__main__':
    main()