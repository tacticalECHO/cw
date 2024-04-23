import copy
import io
import random
import re
import math
import time
Problems = []
iteration=1000
Pop_size=100
k=2
Prim_rate=0.98
Low_rate=0.9

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
def firstGeneration(problem):
    sol_1=solution(problem)
    First_Fit(sol_1,problem.items)
    fitness(sol_1)
    sol_2=solution(problem)
    Best_Fit(sol_2,problem.items)
    fitness(sol_2)
    return sol_1,sol_2
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
def Crossover_Prime(sol_1,sol_2):
    Great_knapsack=[]
    small_knapsack=[]
    itemInGreaterKnapsack=[]
    for knapsack in sol_1.knapsacks:
        if knapsack.getWeight()>=math.floor(knapsack.capacity*Prim_rate):
            Great_knapsack.append(knapsack)
            itemInGreaterKnapsack+=knapsack.getItems()
    for knapsack in sol_2.knapsacks:
        if knapsack.getWeight()<math.floor(knapsack.capacity*Low_rate):
            small_knapsack.append(knapsack)
    sol2=sol_2.knapsacks
    item_to_knapsack={}
    Knapsack_to_delete=set()
    for Kna in sol2:
        for item in Kna.getItems():
            item_to_knapsack[item.id]=Kna
    for Aknapsack in Great_knapsack:
        for item in Aknapsack.getItems():
            if item.id in item_to_knapsack:
                Knapsack_to_delete.add(item_to_knapsack[item.id])
    for Bkna_small in small_knapsack:
        Knapsack_to_delete.add(Bkna_small)
    for Bknapsack in Great_knapsack:
        sol2.append(Bknapsack)
    for Cknapsack in Knapsack_to_delete:
        sol2.remove(Cknapsack)
    items_to_delete=set()
    for Dknapsack in Knapsack_to_delete:
        for item in Dknapsack.getItems():
            items_to_delete.add(item)
    diff=set(items_to_delete-set(itemInGreaterKnapsack))
    child=solution(sol_1.problem)
    child.knapsacks=sol2
    First_Fit(child,diff)
    child.number_knapsack=len(child.knapsacks)
    fitness(child)
    return child       

def mutation(solution):
    number_of_mutation=math.ceil(solution.number_knapsack*0.1)
    items=[]
    for i in range(number_of_mutation):
        range_index=random.randint(0,len(solution.knapsacks)-1)
        items+=solution.knapsacks[range_index].getItems()
        solution.knapsacks.remove(solution.knapsacks[range_index])
    First_Fit(solution,items)
    solution.number_knapsack=len(solution.knapsacks)
    fitness(solution)
    return solution

def selection(population):
    selection_population=[]
    count=0
    population.sort(key=lambda x:x.fitness)
    sum_fitness=sum([solution.fitness for solution in population])
    while(count<2):
        for solution in population:
            random_number=random.random()
            if random_number<=solution.fitness/sum_fitness:
                selection_population.append(solution)
                count+=1
                break
    return selection_population[0],selection_population[1]

def geneticAlgorithm(problem):
    populationsize=Pop_size
    best_solution=None
    sol_1,sol_2=firstGeneration(problem)
    population=[sol_1,sol_2]
    for i in range(iteration):
        parent1,parent2=selection(population)
        child1=Crossover_Prime(parent1,parent2)
        child2=Crossover_Prime(parent2,parent1)
        if random.random()<0.1:
            child1=mutation(child1)
        if random.random()<0.1:
            child2=mutation(child2)
        population.append(child1)
        population.append(child2)
        if len(population)>populationsize:
            population.sort(key=lambda x:x.number_knapsack,reverse=True)
            population=population[:populationsize]
    population.sort(key=lambda x:x.number_knapsack)
    best_solution=population[0]
    return best_solution

    
def SimulatedAnnealing(problem):
    T=100
    T_min=0.1
    alpha=0.9
    current_solution=solution(problem)
    current_solution.number_knapsack=0
    current_solution.knapsacks=[Knapsack(problem.knapsack_list[0].capacity)]
    items_list=copy.deepcopy(problem.items)
    First_Fit(current_solution,items_list)
    best_solution=copy.deepcopy(current_solution)
    while T>T_min:
        i=0
        while i<10:
            new_solution=copy.deepcopy(current_solution)
            new_solution.number_knapsack=0
            new_solution.knapsacks=[Knapsack(problem.knapsack_list[0].capacity)]
            items_list=copy.deepcopy(problem.items)
            random.shuffle(items_list)
            First_Fit(new_solution,items_list)
            fitness(new_solution)
            if new_solution.number_knapsack<best_solution.number_knapsack:
                best_solution=new_solution
            if new_solution.number_knapsack<current_solution.number_knapsack:
                current_solution=new_solution
            else:
                delta=new_solution.number_knapsack-current_solution.number_knapsack
                if random.random()<math.exp(-delta/T):
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
    dataProcess('binpack3.txt')
    timeStart = time.time()
    for problem in Problems:
        #best_solution=SimulatedAnnealing(problem)
        best_solution=geneticAlgorithm(problem)
        best_solution.number_knapsack=len(best_solution.knapsacks)
        #print('Problem:',problem.name)
        #print('Best solution:',best_solution.fitness)
        #print('Number of knapsacks:',best_solution.number_knapsack)
        #print('Best solution for now:',problem.Best_solution)
        #for knapsack in best_solution.knapsacks:
            #print('Knapsack:')
            #print('Weight:',knapsack.getWeight())
            #for item in knapsack.getItems():
                #print(item.id,end=' ')
        #print('---------------------------------')
        problem.my_solution=best_solution
    PrintToFile('output.txt')
    timeEnd = time.time()
    print('Time:',timeEnd-timeStart)


if __name__ == '__main__':
    main()