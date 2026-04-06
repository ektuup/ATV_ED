#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define and &&
#define or ||
#define not !
#define mod %

typedef unsigned char uint8;
typedef enum{NORMAL, HIGH}Priority;

typedef struct{
    char data[64];
    int len;
}String;

typedef struct Pessoa{
    String nome;
    uint8 idade;
}Pessoa;

Priority IdadeToPriority(uint8 idade){
    return idade < 60 ? NORMAL : HIGH;
}

Pessoa new_Pessoa(String nome, uint8 idade){
    return (Pessoa){nome, idade};
}

String new_String(const char* str){
    String S;
    if(str == NULL){
        S.data[0] = '\0';
        S.len = 0;
        return S;
    }
    strcpy(S.data, str);
    S.len = strlen(str);
    return S;
}

typedef struct node{
    Pessoa data;
    struct node* next;
}node;

typedef struct PriorityQueue{
    node* highPriority, *normalPriority;
    int contDequeue;
}PriorityQueue;

node* new_node(Pessoa p){
    node* new = malloc(sizeof(node));
    new->data = p;
    new->next = NULL;
    return new;
}

PriorityQueue* new_priorityQueue(){
    PriorityQueue* pq = malloc(sizeof(PriorityQueue));
    pq->highPriority = NULL;
    pq->normalPriority = NULL;
    pq->contDequeue = 0;
    return pq;
}

void enQueue(PriorityQueue* pq, Pessoa p){
    Priority pr = IdadeToPriority(p.idade);
    node** aux = (pr == HIGH) ? &(pq->highPriority) : &(pq->normalPriority);
    node* new = new_node(p);
    if(*aux == NULL){
        *aux = new;
    }else{
        node* temp = *aux;
        while(temp->next != NULL){
            temp = temp->next;
        }
        temp->next = new;
    }
    printf("%s inserido na lista de prioridade %s\n", p.nome.data, (pr == HIGH) ? "Alta" : "Normal");
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
    }else if(not IsEmpty(pq, NORMAL)){
        aux = pq->normalPriority;
        pq->normalPriority = pq->normalPriority->next;
        pq->contDequeue = (pq->contDequeue + 1) mod 4;
    }else if(not IsEmpty(pq, HIGH)){
        aux = pq->highPriority;
        pq->highPriority = pq->highPriority->next;
        pq->contDequeue = (pq->contDequeue + 1) mod 4;
    }
    Pessoa p = aux->data;
    free(aux);
    return p;
}

void delete_priorityQueue(PriorityQueue** pq){
    if(pq == NULL || *pq == NULL) return;
    node* aux = (*pq)->highPriority;
    while(aux != NULL){
        node* temp = aux;
        aux = aux->next;
        free(temp);
    }
    aux = (*pq)->normalPriority;
    while(aux != NULL){
        node* temp = aux;
        aux = aux->next;
        free(temp);
    }
    free(*pq);
    (*pq) = NULL;
}

void print_priorityQueue(PriorityQueue* pq){
    printf("Fila de prioridade alta:\n");
    node* aux = pq->highPriority;
    int i = 1;
    while(aux != NULL){
        printf("%d - %s\n", i++, aux->data.nome);
        aux = aux->next;
    }
    putchar('\n');
    aux = pq->normalPriority;
    printf("Fila de prioridade normal:\n");
    i = 1;
    while(aux != NULL){
        printf("%d - %s\n", i++, aux->data.nome);
        aux = aux->next;
    }
    putchar('\n');
}

int main(){
    PriorityQueue* fila = new_priorityQueue();
    const char* nomes[] = {"Ana", "Glaucio", "Artur", "Heytor", "Karina", "Eliza", "Antonia", "Luiza", "Marina", "Jose"};
    uint8 idades[] = {18, 20, 19, 21, 45, 6, 60, 65, 62, 84};
    int n = sizeof(nomes)/sizeof(nomes[0]);
    Pessoa pessoas[n];
    Pessoa atendida;
    int cont_atendidas = 0;
    for(int i = 0; i < n; i++){
        pessoas[i] = new_Pessoa(new_String(nomes[i]), idades[i]);
        enQueue(fila, pessoas[i]);
    }
    print_priorityQueue(fila);

    for(int i = 0; i < n; i++){
        atendida = deQueue(fila);
        Priority p = IdadeToPriority(atendida.idade);
        printf("%s foi atendido(a) na fila com prioridade %s\n", atendida.nome.data, (p == HIGH) ? "Alta" : "Normal");
    }

    delete_priorityQueue(&fila);
    return 0;
}