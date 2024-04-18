import io
import re
Problems = []
class Item:
    def __init__(self,weight):
        self.weight=weight
class problem:
    def __init__(self,name,capacity,numberofitems,items,Best_solution):
        self.name=name
        self.numberofitems=numberofitems
        self.items=items
        self.Best_solution=Best_solution
        self.knapsack_list=[knapsack(capacity)]
        self.number_knapsack=0
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
            items.append(Item(weight))
        Problems.append(problem(name,capacity,Numberofitems,items,bestsloution))
        index+=Numberofitems+1
def FirstSolution(problem):
    problem.items.sort(key=lambda x: x.weight, reverse=True)
    for i in range(problem.numberofitems):
        if problem.knapsack_list[problem.number_knapsack].getWeight()+problem.items[i].weight<=problem.knapsack_list[problem.number_knapsack].capacity:
            problem.knapsack_list[problem.number_knapsack].add(problem.items[i])
        else:
            problem.knapsack_list.append(knapsack(problem.knapsack_list[problem.number_knapsack].capacity))
            problem.number_knapsack+=1
            problem.knapsack_list[problem.number_knapsack].add(problem.items[i])

def main():
    filename = 'test.txt'
    dataProcess(filename)
    for problem in Problems:
        FirstSolution(problem)
        print(problem.name)
        print(problem.number_knapsack)
        print(problem.Best_solution)
        print('\n')
    

if __name__ == '__main__':
    main()