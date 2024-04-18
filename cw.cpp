#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <iostream>
using namespace std;

struct problem
{
    string name;//name of the problem
    int n;//number of items
    int pack_capacity;//capacity of the knapsack
    int *items;//array of items
    int best_value;//best value found so far
};

struct backpack
{
    int *items;//array of items in the backpack
    int capacity;//capacity of the backpack
};



void read_problem(struct problem *p, string file_name)
{
    FILE *f;
    f = fopen(file_name.c_str(), "r");
    if (f == NULL)
    {
        cout << "Error opening file" << endl;
        exit(1);
    }
    char line[100];
    fscanf(f, "%s", line);
    p->name = line;
    fscanf(f, "%s", line);
    p->n = atoi(line);
    fscanf(f, "%s", line);
    p->pack_capacity = atoi(line);
}