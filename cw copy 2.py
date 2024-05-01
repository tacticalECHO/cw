import copy
import random
import re
import math
import sys
import time
import itertools
Problems = []
iteration=100
Pop_size=100
mutation_rate=0.1
mutation_rate_N=0.2
k=2
Prim_rate=0.98
Low_rate=0.9
# Genetic Algorithm Parameters
#-----------------------------------------------------------------------------------------------------------------------
# PSO Parameters
PSO_population_size=10 
PSO_w=0.5
PSO_c1=1.6
PSO_c2=2.5
PSO_iteration=50
PSO_mutation_rate_N=0.3
#-----------------------------------------------------------------------------------------------------------------------
# Genetic Algorithm
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
def Crossover_Prime(fsol_1,fsol_2):
    sol_1=copy.deepcopy(fsol_1)
    sol_2=copy.deepcopy(fsol_2)
    child=solution(sol_1.problem)
    GreatGene_in_sol_1=[]
    item_in_great_gene=[]
    for kn in sol_1.knapsacks:
        if kn.getWeight()>=kn.capacity*Prim_rate:
            GreatGene_in_sol_1.append(kn)
            item_in_great_gene+=kn.getItems()
    item_to_knapsack={}
    for kn in GreatGene_in_sol_1:
        for item in kn.getItems():
            item_to_knapsack[item.id]=kn
    kn_to_delete=set()
    for kn in sol_2.knapsacks:
        for item in kn.getItems():
            if item.id in item_to_knapsack:
                kn_to_delete.add(kn)
                break
    item_in_detele=[]
    for kn in kn_to_delete:
        item_in_detele+=kn.getItems()
        sol_2.knapsacks.remove(kn)
    diff_item=set(item_in_detele)-set(item_in_great_gene)
    child.knapsacks=copy.deepcopy(sol_2.knapsacks)
    First_Fit(child,list(diff_item))
    child.number_knapsack=len(child.knapsacks)
    fitness(child)
    return child
def firstGeneration(problem):
    sol_1=solution(problem)
    First_Fit(sol_1,problem.items)
    fitness(sol_1)
    sol_2=solution(problem)
    Best_Fit(sol_2,problem.items)
    fitness(sol_2)
    return sol_1,sol_2
def mutation(solution):
    number_of_mutation=math.ceil(solution.number_knapsack*mutation_rate_N)
    items=[]
    for i in range(number_of_mutation):
        swap_items_solution(solution)
        shift_item_large_knapsack(solution)
        range_index=random.randint(0,len(solution.knapsacks)-1)
        items+=solution.knapsacks[range_index].getItems()
        solution.knapsacks.remove(solution.knapsacks[range_index])
    Best_Fit(solution,items)
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
        if random.random()<mutation_rate:
            child1=mutation(child1)
        if random.random()<mutation_rate:
            child2=mutation(child2)
        population.append(child1)
        population.append(child2)
        if len(population)>populationsize:
            population.sort(key=lambda x:x.number_knapsack,reverse=True)
            population=population[:populationsize]
    population.sort(key=lambda x:x.fitness)
    best_solution=population[0]
    return best_solution
#-----------------------------------------------------------------------------------------------------------------------
# PSO
class Particle:
    def __init__(self,problem,position,number_of_swap,best_number_knapsack=-1):
        self.problem=problem
        self.position=position
        self.velocity=number_of_swap
        self.best_position=solution(problem)
        self.best_number_knapsack=best_number_knapsack
        self.fitness=0
    def update_velocity(self,global_best,w,c1,c2):
        number_of_swap=math.ceil(self.velocity*w+c1*random.random()*(self.best_position.number_knapsack-self.position.number_knapsack)+c2*random.random()*(global_best.best_number_knapsack-self.position.number_knapsack))
        return number_of_swap
    def update_position(self):
        new_position=solution(self.problem)
        new_position.knapsacks=copy.deepcopy(self.position.knapsacks)
        for i in range(abs(self.velocity)):
            Clear_null_knapsack(new_position)
            shift_items(new_position)
            PSO_mutation(new_position)
            #shift_item_large_knapsack(new_position)
        new_position.number_knapsack=len(new_position.knapsacks)
        fitness(new_position)
        if new_position.number_knapsack<self.best_number_knapsack:
            self.best_number_knapsack=new_position.number_knapsack
            self.best_position=new_position
        self.position=new_position
def Clear_null_knapsack(solution):
    for knapsack in solution.knapsacks:
        if len(knapsack.getItems())==0:
            solution.knapsacks.remove(knapsack)
def swap_items_solution(solution):
    kn_not_full=[kn for kn in solution.knapsacks if kn.getWeight()<kn.capacity]
    if len(kn_not_full)<2:
        return
    kn1=random.choice(kn_not_full)
    item1=random.choice(kn1.getItems())
    for kn in kn_not_full:
        if kn!=kn1:
            for item2 in kn.getItems():
                if item1.weight<item2.weight<=item1.weight*1.2 and kn1.getWeight()-item1.weight+item2.weight<=kn1.capacity:
                    kn.add(item1)
                    kn1.add(item2)
                    kn.remove(item2)
                    kn1.remove(item1)
                    return
def PSO_mutation(solution):
    number_of_mutation=math.ceil(solution.number_knapsack*PSO_mutation_rate_N)
    Kn_in_order_weight=sorted(solution.knapsacks,key=lambda x:x.getWeight())
    items=[]
    for i in range(number_of_mutation):
        swap_items_solution(solution)
        shift_item_large_knapsack(solution)
        items+=Kn_in_order_weight[i].getItems()
        solution.knapsacks.remove(Kn_in_order_weight[i])

    Best_Fit(solution,items)
    solution.number_knapsack=len(solution.knapsacks)
    fitness(solution)
    return solution
def swap_item_max_min_knapsack(solution):
    kn_max=max(solution.knapsacks,key=lambda x:len(x.getItems()))
    item_in_max=sorted(kn_max.getItems(),key=lambda x:x.weight)
    move_item=[]
    for item in item_in_max:
        place=False
        for kn in solution.knapsacks:
            if kn!=kn_max:
                if kn.getWeight()+item.weight<=kn.capacity:
                    kn.add(item)
                    kn_max.remove(item)
                    place=True
                    break
        if place:
            move_item.append(item)
        else:
            new_knapsack=Knapsack(solution.problem.knapsack_list[0].capacity)
            new_knapsack.add(item)
            solution.knapsacks.append(new_knapsack)
            solution.number_knapsack=len(solution.knapsacks)
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
def shift_items(solution):
    kn_sorted=sorted(solution.knapsacks,key=lambda x:x.getWeight())
    minimum=kn_sorted[0]
    kn_sorted_rev=sorted(solution.knapsacks,key=lambda x:x.getWeight(),reverse=True)
    item_in_minimum=minimum.getItems()
    #swap items
    for item in item_in_minimum:
        minimum.remove(item)
        for knapsack in kn_sorted_rev:
            if knapsack!=minimum:
                item2=min(knapsack.getItems(),key=lambda x:x.weight)
                if item.weight+knapsack.getWeight()<=knapsack.capacity and item2.weight<item.weight:
                    knapsack.add(item)
                    knapsack.remove(item2)
                    minimum.add(item2)
                    break
                elif item.weight+knapsack.getWeight()-item2.weight<=knapsack.capacity and item2.weight<item.weight:
                    knapsack.add(item)
                    knapsack.remove(item2)
                    minimum.add(item2)
                    break
        else:
            minimum.add(item)

    if len(minimum.getItems())==0:
        solution.knapsacks.remove(minimum)


def PSO_best_fit(solution,items):
    for item in items:
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
def PSO_first_fit(solution,items):
    for item in items:
        for knapsack in solution.knapsacks:
            if knapsack.getWeight()+item.weight<=knapsack.capacity:
                knapsack.add(item)
                break
        else:
            new_knapsack=Knapsack(solution.problem.knapsack_list[0].capacity)
            new_knapsack.add(item)
            solution.knapsacks.append(new_knapsack)
            solution.number_knapsack=len(solution.knapsacks)
def PSO_best_fit(solution,items):
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
def init_population(problem,population_size):
    population=[]
    for i in range(population_size):
        sol=solution(problem)
        items=copy.deepcopy(problem.items)
        items=random.shuffle(items)
        PSO_first_fit(sol,problem.items)
        sol.number_knapsack=len(sol.knapsacks)
        fitness(sol)
        population.append(Particle(problem,sol,math.ceil(random.random()*len(sol.knapsacks)),sol.number_knapsack))
    return population
def update_global_best(population):
    population.sort(key=lambda x:x.best_number_knapsack)
    return population[0]
def update_population(population,global_best,w,c1,c2):
    for particle in population:
        particle.velocity=particle.update_velocity(global_best,w,c1,c2)
        particle.update_position()
def PSO(problem,population_size,w,c1,c2):
    population=init_population(problem,population_size)
    global_best=update_global_best(population)
    time_start=time.time()
    for i in range(PSO_iteration):
        update_population(population,global_best,w,c1,c2)
        global_best=update_global_best(population)
        time_end=time.time()
        if time_end-time_start>15:
            break
    return global_best.position

#-----------------------------------------------------------------------------------------------------------------------
# Simulated Annealing
def random_swap(solution):
    knapsacks=solution.knapsacks
    kn1=random.choice(knapsacks)
    kn2=random.choice(knapsacks)
    item1=random.choice(kn1.getItems())
    item2=random.choice(kn2.getItems())
    if kn1!=kn2 and kn1.getWeight()-item1.weight+item2.weight<=kn1.capacity and kn2.getWeight()-item2.weight+item1.weight<=kn2.capacity:
        kn1.add(item2)
        kn1.remove(item1)
        kn2.add(item1)
        kn2.remove(item2)
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
        while i<25:
            new_solution=copy.deepcopy(current_solution)
            random_number=random.random()
            if random_number>0.35:
                swap_item_max_min_knapsack(new_solution)
                new_solution.number_knapsack=len(new_solution.knapsacks)
                Clear_null_knapsack(new_solution)
                PSO_mutation(new_solution)
                new_solution.number_knapsack=len(new_solution.knapsacks)
            elif random_number<=0.35:
                swap_items_solution(new_solution)
                new_solution.number_knapsack=len(new_solution.knapsacks)
                shift_item_large_knapsack(new_solution)
                new_solution.number_knapsack=len(new_solution.knapsacks)
            else:
                swap_items_solution(new_solution)
                new_solution.number_knapsack=len(new_solution.knapsacks)
                random_swap(new_solution)
                new_solution.number_knapsack=len(new_solution.knapsacks)
                PSO_mutation(new_solution)
            new_solution.number_knapsack=len(new_solution.knapsacks)
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
    filename = sys.argv[2]
    dataProcess(filename)
    timeStart = time.time()
    for problem in Problems:
        Pro_start=time.time()
        #best_solution=PSO(problem,PSO_population_size,PSO_w,PSO_c1,PSO_c2)
        best_solution=geneticAlgorithm(problem)
        problem.my_solution=best_solution
        Pro_end=time.time()
        print(Pro_end-Pro_start)
    PrintToFile(sys.argv[4])
    timeEnd = time.time()
    print('Time:',timeEnd-timeStart)

if __name__ == '__main__':
    main()