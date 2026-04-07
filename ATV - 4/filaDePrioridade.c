#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define and &&
#define or ||
#define not !
#define mod %
#define MAX_PESSOAS 128
#define PESSOA_INVALIDA (Pessoa){(String){""}, -1}

typedef enum{NORMAL, HIGH}Priority;

Priority IdadeToPriority(int idade){
    return idade < 60 ? NORMAL : HIGH;
}

typedef struct{
    char data[64];
}String;

String new_String(const char* str){
    String S;
    if(str == NULL){
        S.data[0] = '\0'; //caso str seja um ponteiro nulo, a string é vazia;
        return S;
    }
    strcpy(S.data, str);
    return S;
}

typedef struct Pessoa{
    String nome;
    int idade;
}Pessoa;

//construtor de Pessoa
Pessoa new_Pessoa(String nome, int idade){ 
    return (Pessoa){nome, idade};
}

typedef struct node{
    Pessoa data;
    struct node* next;
}node;

node* new_node(Pessoa p){
    node* new = malloc(sizeof(node));
    new->data = p;
    new->next = NULL;
    return new;
}

typedef struct PriorityQueue{
    node* highPriority, *normalPriority;
    int contDequeue;
    size_t size;
}PriorityQueue;

PriorityQueue* new_priorityQueue(){
    PriorityQueue* pq = malloc(sizeof(PriorityQueue));
    pq->highPriority = NULL;
    pq->normalPriority = NULL;
    pq->contDequeue = 0;
    pq->size = 0;
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
        while((temp)->next != NULL)
            (temp) = (temp)->next;
        (temp)->next = new;
    }
    pq->size++;
    printf("%s inserido na lista de prioridade %s\n", p.nome.data, (pr == HIGH) ? "Alta" : "Normal");
}

int IsEmpty(PriorityQueue* pq, Priority p){
    node* queue = (p == HIGH) ? pq->highPriority : pq->normalPriority;
    return queue == NULL;
}

Pessoa deQueue(PriorityQueue* pq){
    //tira da fila normal enquant cont < 3 e a fila normal nao ser vazia.
    //se cont == 3 ou a fila normal estar vazia, tira da de prioridade alta.
    if(pq->size == 0) return PESSOA_INVALIDA;
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
    pq->size--;
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

int ReadFile(const char* filename, Pessoa* p){
    FILE* arq = fopen(filename, "r");
    String line = new_String(""), nome;
    int idade;
    int i = 0, cont = 0, olha;
    while(fgets(line.data, sizeof(line.data), arq)){
        while(line.data[i] == ' ') i++;
        if(line.data[i] == '\0') continue;
        
        int lido = sscanf(line.data, "%63[^;];%d", nome.data, &idade);

        if(lido < 2){
            line.data[strlen(line.data) - 1] = '\0';
            printf("Erro em '%s' : cada linha do arquivo deve ser do formato 'nome;idade'\n", line.data);
            exit(EXIT_FAILURE);
        }
        if(cont == MAX_PESSOAS){
            printf("Erro: capacidade maxima de pessoas permitido é %d. por favor aumente a capacidade caso queira armazenar mais\n", MAX_PESSOAS);
            return cont;
        }

        p[cont++] = new_Pessoa(nome, idade);
    }
    return cont;
}

int main(){
    PriorityQueue* fila = new_priorityQueue();
    const char* filename = "clientes.txt";
    Pessoa pessoas[MAX_PESSOAS], atendida;
    int n = ReadFile(filename, pessoas);
    int cont_atendidas = 0; 
    for(int i = 0; i < n; i++){
        enQueue(fila, pessoas[i]);
        printf("%s;%d\n", pessoas[i].nome.data, pessoas[i].idade);
    }
    print_priorityQueue(fila);

    for(int i = 0; i < n; i++){
        if(fila->size){
            atendida = deQueue(fila);
            Priority p = IdadeToPriority(atendida.idade);
            cont_atendidas++;
            printf("%s foi atendido(a) na fila com prioridade %s\n", atendida.nome.data, (p == HIGH) ? "Alta" : "Normal");
        }
    }
    delete_priorityQueue(&fila);
    return 0;
}