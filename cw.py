import io
import random
import re
import math
Problems = []
iteration=1000
Pop_size=100
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
        self.knapsack_list=[knapsack(capacity)]
        self.number_knapsack=0
        self.my_solution=None
class knapsack:
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
class solution:
    def __init__(self,problem,number_knapsack=0):
        self.problem=problem
        self.knapsacks=[knapsack(problem.knapsack_list[0].capacity)]
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
        number=re.findall('[0-9]+',data[index+1])
        Numberofitems=int(number[1])
        capacity=int(number[0])
        bestsloution=int(number[2])
        items=[]
        for j in range(1, Numberofitems+1):
            weight=re.findall('[0-9]+',data[index+j+1])
            weight=int(weight[0])
            items.append(Item(weight,j))
        Problems.append(problem(name,capacity,Numberofitems,items,bestsloution))
        index+=Numberofitems+1
def WithoutLimit(problem):
    total_weight=sum([item.weight for item in problem.items])
    packNum=math.ceil(total_weight/problem.knapsack_list[0].capacity)
    return packNum
def fitness(solution):
    solution.fitness=sum([pow(knapsack.getWeight()/knapsack.capacity,k) for knapsack in solution.knapsacks])/solution.number_knapsack
def firstGeneration(problem):
    sol_1=solution(problem)
    for item in problem.items:
        if sol_1.knapsacks[sol_1.number_knapsack].getWeight()+item.weight<=problem.knapsack_list[0].capacity:
            sol_1.knapsacks[sol_1.number_knapsack].add(item)
        else:
            sol_1.number_knapsack+=1
            sol_1.knapsacks.append(knapsack(problem.knapsack_list[0].capacity))
            sol_1.knapsacks[sol_1.number_knapsack].add(item)
    fitness(sol_1)
    sol_2=solution(problem)
    items_in_order=sorted(problem.items,key=lambda x:x.weight,reverse=True)
    for item in items_in_order:
        if sol_2.knapsacks[sol_2.number_knapsack].getWeight()+item.weight<=problem.knapsack_list[0].capacity:
            sol_2.knapsacks[sol_2.number_knapsack].add(item)
        else:
            sol_2.number_knapsack+=1
            sol_2.knapsacks.append(knapsack(problem.knapsack_list[0].capacity))
            sol_2.knapsacks[sol_2.number_knapsack].add(item)
    fitness(sol_2)
    return sol_1,sol_2
def Fit_process(solution,items):
    for item in items:
        for bag in solution.knapsacks:
            if bag.getWeight()+item.weight<=bag.capacity:
                bag.add(item)
                items.remove(item)
                break        
def First_Fit(solution,items):
    for item in items:
        for bag in solution.knapsacks:
            if bag.getWeight()+item.weight<=bag.capacity:
                bag.add(item)
                items.remove(item)
                break
    if len(items)>0:
        add_knapsack=knapsack(solution.problem.knapsack_list[0].capacity)
        add_knapsack.add(items[0])
        items.remove(items[0])
        solution.knapsacks.append(add_knapsack)
        solution.number_knapsack=len(solution.knapsacks)
        First_Fit(solution,items)

def crossover(sol_1,sol_2):
    cross_point1=random.randint(0,len(sol_1.knapsacks)-1)
    if cross_point1==0:
        cross_point1+=1
    cross_part1=sol_1.knapsacks[:cross_point1]
    child=solution(sol_1.problem)
    item_in_cross_part1=[]
    Sol2_knapsack=[]
    for knapsack in sol_2.knapsacks:
        Sol2_knapsack.append(knapsack)
    Del_item=[]
    for knapsack in cross_part1:
        item_in_cross_part1+=knapsack.getItems()
    for item in item_in_cross_part1:
        for Knapsack in Sol2_knapsack:
            if item in Knapsack.getItems():
                for ITEM in Knapsack.getItems():
                    if ITEM not in item_in_cross_part1:
                        Del_item.append(ITEM)
                Sol2_knapsack.remove(Knapsack)
    for knapsack in cross_part1:
        child.knapsacks.append(knapsack)
    for knapsack in Sol2_knapsack:
        child.knapsacks.append(knapsack)
    First_Fit(child,Del_item)
    child.number_knapsack=len(child.knapsacks)
    fitness(child)
    return child
def mutation(solution):
    number_of_mutation=math.ceil(solution.number_knapsack*0.1)
    for i in range(number_of_mutation):
        range_index=random.randint(0,len(solution.knapsacks)-1)
        items=solution.knapsacks[range_index].getItems()
        solution.knapsacks.remove(solution.knapsacks[range_index])
    solution.number_knapsack=len(solution.knapsacks)
    First_Fit(solution,items)
    fitness(solution)
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
        child=crossover(parent1,parent2)
        if random.random()<0.1:
            mutation(child)
        population.append(child)
        if len(population)>populationsize:
            population.sort(key=lambda x:x.fitness,reverse=True)
            population=population[:populationsize]
    best_solution=population[0]
    return best_solution
def main():
    dataProcess('test.txt')
    for problem in Problems:
        best_solution=geneticAlgorithm(problem)
        print('Problem:',problem.name)
        print('Best solution:',best_solution.fitness)
        print('Number of knapsacks:',best_solution.number_knapsack)
        print('Best solution for now:',problem.Best_solution)
        print('---------------------------------')

if __name__ == '__main__':
    main()