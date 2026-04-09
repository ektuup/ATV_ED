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
    //tira da fila normal enquant cont < 3 e a fila normal nao ser vazia.
    //se contDequeue == 3 ou a fila normal estar vazia, tira da de prioridade alta.
    node* aux = NULL;

    if(not in_list(pq->history, HIGH) and not IsEmpty(pq, HIGH)){    
        aux = pq->highPriority;
        pq->highPriority = pq->highPriority->next;
        //uso do mod 4 porque se contdeQueue == 0, entao tira da prioridade, se for 1, 2 ou 3 tira do normal
    }else if(not IsEmpty(pq, NORMAL)){
        aux = pq->normalPriority;
        pq->normalPriority = pq->normalPriority->next;
    }else if(not IsEmpty(pq, HIGH)){
        aux = pq->highPriority;
        pq->highPriority = pq->highPriority->next; 
        //caso o contDequeue seja diferente de 0, mas nao hajam pessoas sem prioridade na fila, remove os com prioridade
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

void printpriorityQueue(PriorityQueue* pq){
    // node* aux = pq->highPriority;
    // int i = 0;
    // printf("Pessoas com Prioridade:\n\n");

    // while(aux){
    //     printf("%d - *%s\n", ++i, aux->data.nome.data);
    //     aux = aux->next;
    // }
    // putchar('\n');

    // i = 0;
    // aux = pq->normalPriority;
    // printf("Pessoas sem Prioridade:\n\n");

    // while(aux){
    //     printf("%d - %s\n", ++i, aux->data.nome.data);
    //     aux = aux->next;
    // }
    // putchar('\n');

    Pessoa p;
    int i = 0;
    node* auxHigh = pq->highPriority, *auxNormal = pq->normalPriority;
    RecentList* S = new_RecentList();
    while(auxHigh or auxNormal){
        if(not in_list(S, HIGH) and auxHigh != NULL){    
            p = auxHigh->data;
            auxHigh = auxHigh->next;
            //uso do mod 4 porque se contdeQueue == 0, entao tira da prioridade, se for 1, 2 ou 3 tira do normal
        }else if(auxNormal != NULL){
            p = auxNormal->data;
            auxNormal = auxNormal->next;
        }else if(auxHigh != NULL){
            p = auxHigh->data;
            auxHigh = auxHigh->next; 
            //caso o contDequeue seja diferente de 0, mas nao hajam pessoas sem prioridade na fila, remove os com prioridade
        }
        printf("%d - %s%s\n", ++i, p.prioridade == HIGH ? "*" : "", p.nome.data);
        list_add(S, p);
    }
    delete_Recentlist(S);
}
