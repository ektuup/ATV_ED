#include "priorityQueue.h"

Priority getPriority(Pessoa p){
    return (p.idade < IDADE_PRIORITARIA_MINIMA) ? NORMAL : HIGH;
}

node* new_node(Pessoa p){
    node* new = malloc(sizeof(node));
    new->data = p;
    new->next = NULL;
    return new;
}

void addNode(node** no, node* new){
    if(*no == NULL){
        *no = new;
        return;
    }
    node* temp = *no;
    while(temp->next != NULL){
        temp = temp->next;
    }
    temp->next = new;
}

PriorityQueue* new_priorityQueue(){
    PriorityQueue* pq = malloc(sizeof(PriorityQueue));
    pq->highPriority = NULL;
    pq->normalPriority = NULL;
    pq->contDequeue = 0;
    pq->size = 0;
    return pq;
}

void enQueue(PriorityQueue* pq, Pessoa p){
    p.prioridade = getPriority(p);
    node** aux = (p.prioridade == HIGH) ? &pq->highPriority : &pq->normalPriority;
    node* new = new_node(p);
    addNode(aux, new);
    pq->size++;
}

int IsEmpty(PriorityQueue* pq, Priority p){
    node* queue = (p == HIGH) ? pq->highPriority : pq->normalPriority;
    return queue == NULL;
}

Pessoa deQueue(PriorityQueue* pq){
    //tira da fila normal enquant cont < 3 e a fila normal nao ser vazia.
    //se cont == 3 ou a fila normal estar vazia, tira da de prioridade alta.
    node* aux = NULL;
    if(pq->contDequeue == 0 and not IsEmpty(pq, HIGH)){
        aux = pq->highPriority;
        pq->highPriority = pq->highPriority->next;
        pq->contDequeue = (pq->contDequeue + 1) mod 4; 
        //uso do mod 4 porque se contdeQueue == 0, entao tira da prioridade, se for 1, 2 ou 3 tira do normal
    }else if(not IsEmpty(pq, NORMAL)){
        aux = pq->normalPriority;
        pq->normalPriority = pq->normalPriority->next;
        pq->contDequeue = (pq->contDequeue + 1) mod 4;
    }else if(not IsEmpty(pq, HIGH)){
        aux = pq->highPriority;
        pq->highPriority = pq->highPriority->next; 
        pq->contDequeue = (pq->contDequeue + 1) mod 4;
        //caso o contDequeue seja diferente de 0, mas nao hajam pessoas sem prioridade na fila, remove os com prioridade
    }
    pq->size--;
    Pessoa p = aux->data;
    free(aux);
    return p;
}

void delete_priorityQueue(PriorityQueue** pq){
    if(pq == NULL || *pq == NULL) return;
    while((*pq)->size){
        deQueue(*pq); //deQueue ja remove todos seguindo a regra de negocios
    }
    free(*pq);
    (*pq) = NULL;
}

void printpriorityQueue(PriorityQueue* pq){
    PriorityQueue *aux = new_priorityQueue();
    Pessoa p;
    printf("Pessoas na fila de atendimento:\n");
    while(pq->size){
        p = deQueue(pq);
        printf("%s%s\n", p.prioridade == HIGH ? "*" : "", p.nome.data);
        enQueue(aux, p);
        //usa duas filas com prioridade para guardar os dados enquanto printa, não havendo perda
    }
    
    while(aux->size){
        enQueue(pq, deQueue(aux));
        //devolve os dados para a fila original
    }
    delete_priorityQueue(&aux);
}