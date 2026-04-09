#include "priorityQueue.h"

Priority getPriority(Pessoa p){
    return (p.idade < IDADE_PRIORITARIA_MINIMA) ? NORMAL : HIGH;
}

PriorityQueue* new_priorityQueue(){
    PriorityQueue* pq = malloc(sizeof(PriorityQueue));
    pq->highPriority = NULL;
    pq->normalPriority = NULL;
    pq->size = 0;
    pq->history = new_RecentList();
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
    node* aux = NULL;

    //uma pessoa com prioridade só é adicionada na lista se nao houver nenhuma adição no historico dos 3 ultimos
    //no caso do historico ter pelo menos um asterisc (EX: { , , *}), nao podemos adicionar uma pessoa de prioridade 
    //{ , , ,}esse é o unico caso em que podemos adicionar, a menos que a lista de pessoas com prioridade normal esteja vazia

    if(not in_list(pq->history, HIGH) and not IsEmpty(pq, HIGH)){
        aux = pq->highPriority;
        pq->highPriority = pq->highPriority->next;
    }else if(not IsEmpty(pq, NORMAL)){
        aux = pq->normalPriority;
        pq->normalPriority = pq->normalPriority->next;
    }else if(not IsEmpty(pq, HIGH)){
        aux = pq->highPriority;
        pq->highPriority = pq->highPriority->next;
    }
    list_add(pq->history, aux->data);

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
    delete_Recentlist((*pq)->history);
    free(*pq);
    (*pq) = NULL;
}
