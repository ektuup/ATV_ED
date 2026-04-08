#ifndef _PRIORITQUEUE_H_
#define _PRIORITQUEUE_H_

#include "types.h"

typedef struct node{
    Pessoa data;
    struct node* next;
}node;

typedef struct PriorityQueue{
    node* highPriority, *normalPriority;
    int contDequeue;
    int size;
}PriorityQueue;

node* new_node(Pessoa p);
void addNode(node** no, node* new);
PriorityQueue* new_priorityQueue();
void enQueue(PriorityQueue* pq, Pessoa p);
int IsEmpty(PriorityQueue* pq, Priority p);
Pessoa deQueue(PriorityQueue* pq);
void delete_priorityQueue(PriorityQueue** pq);
void printpriorityQueue(PriorityQueue* pq);
Priority getPriority(Pessoa p);

#endif