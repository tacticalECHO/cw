import io
import re
Num_Problem = 0
Problems = []
class Item:
    def __init__(self,weight):
        self.weight=weight
class problem:
    def __init__(self,name,capacity,numberofitems,items,bestsolution):
        self.name=name
        self.capacity=capacity
        self.numberofitems=numberofitems
        self.items=items
        self.bestsolution=bestsolution
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

def main():
    filename = 'test.txt'
    dataProcess(filename)
    

if __name__ == '__main__':
    main()