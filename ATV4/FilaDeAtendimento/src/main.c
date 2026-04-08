#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define and &&
#define or ||
#define not !
#define mod %

#define MAX_PESSOAS 128
#define IDADE_PRIORITARIA_MINIMA 60

typedef enum{NORMAL, HIGH}Priority;

typedef struct{
    char data[64];
}String;

void Header(){
    printf("----------------FILA-DE-ATENDIMENTO----------------\n");
}

int Menu(){
    String op;
    char dig;
    Header();
    printf("Politica de prioridade: Pessoas com a partir de\n60 anos tem prioridade na fila\n");

    printf("informe uma opção:\n\n"
           "\t1 - chegada de pessoa para atendimento\n"
           "\t2 - Atendimento de uma pesssoa\n"
           "\t3 - Listar todas as pessoas da fila\n"
           "\t4 - Ler arquivo de atendimento\n"
           "\t0 - Sair\n"
    );
    
    while(1){
        scanf(" %63[^\n]", op.data);
        dig = op.data[0];
        if(strlen(op.data) == 1 && ('0' <= dig && dig <= '4')) break;
        printf("Informe uma opcao valida! (0, 1, 2, 3 ou 4)\n");
    }
    return dig;
}

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
    Priority prioridade;
}Pessoa;

//construtor de Pessoa
Pessoa new_Pessoa(String nome, int idade){ 
    Pessoa p = {nome, idade};
    return p;
}

Priority getPriority(Pessoa p){
    return (p.idade < IDADE_PRIORITARIA_MINIMA) ? NORMAL : HIGH;
}

typedef struct{
    int atendidos_Spr, atendidos_Cpr, total_atendidos;
    float percent_Spr, percent_Cpr;
    Pessoa atendidas[MAX_PESSOAS];
}Estatisticas;
Estatisticas results;

Estatisticas new_Estatisticas(){
    Estatisticas aux = {0, 0, 0, 0, 0};
    return aux;
}

void printPessoasAtendidas(){
    printf("\nPessoas atendidas:\n");
    for(int i = 0; i < results.total_atendidos; i++){
        Pessoa p = results.atendidas[i];
        printf("%d - %s%s\n", i + 1, p.prioridade == HIGH ? "*" : "", p.nome.data);
    }
}

void printEstatisticas(){
    printf("-------------------ESTATISTICAS-------------------\n");
    results.percent_Cpr = results.total_atendidos ? (100.0 * results.atendidos_Cpr)/results.total_atendidos : 0;
    results.percent_Spr = results.total_atendidos ? (100.0 * results.atendidos_Spr)/results.total_atendidos : 0;
    printf("Total de pessoas atendidas: %d\n"
            "Total de pessoas atendidas com prioridade: %d (%.2f%%)\n"
            "Total de pessoas atendidas sem prioridade: %d (%.2f%%)\n",
            results.total_atendidos,
            results.atendidos_Cpr,
            results.percent_Cpr,
            results.atendidos_Spr,
            results.percent_Spr
    );
    printPessoasAtendidas();
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
    int size;
}PriorityQueue;

PriorityQueue* new_priorityQueue(){
    PriorityQueue* pq = malloc(sizeof(PriorityQueue));
    pq->highPriority = NULL;
    pq->normalPriority = NULL;
    pq->contDequeue = 0;
    pq->size = 0;
    return pq;
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
    }
    pq->size--;
    Pessoa p = aux->data;
    free(aux);
    return p;
}

void delete_priorityQueue(PriorityQueue** pq){
    if(pq == NULL || *pq == NULL) return;
    while((*pq)->size){
        deQueue(*pq);
    }
    free(*pq);
    (*pq) = NULL;
}

void printpriorityQueue(PriorityQueue* pq){
    PriorityQueue *aux = new_priorityQueue();
    Pessoa p;
    while(pq->size){
        p = deQueue(pq);
        printf("%s%s\n", p.prioridade == HIGH ? "*" : "", p.nome.data);
        enQueue(aux, p);
    }

    while(aux->size){
        enQueue(pq, deQueue(aux));
    }
    delete_priorityQueue(&aux);
}


int ReadFile(const char* filename, PriorityQueue* pq){
    FILE* arq = fopen(filename, "r");
    String line = new_String(""), nome;
    int cont = 0, olha, idade;

    while(fgets(line.data, sizeof(line.data), arq)){
        line.data[strlen(line.data) - 1] = '\0'; //remove o '\n' absorvido pelo fgets

        int i = 0;
        while(line.data[i] == ' ') i++; 
        if(line.data[i] == '\0') continue;  //ignora linhas vazias
        
        int lido = sscanf(&line.data[i], "%63[^;];%d", nome.data, &idade); //le a partir da posição que nao tem mais espaços

        if(lido < 2){
            line.data[strlen(line.data) - 1] = '\0';
            printf("Erro em '%s' : cada linha do arquivo deve ser do formato 'nome;idade'\n", line.data);
            for(int k = 0; k < cont; k++){
                deQueue(pq);
            }
            return 0;
        }
        if(cont == MAX_PESSOAS){
            printf("Erro: capacidade maxima de pessoas permitido é %d. por favor aumente a capacidade caso queira armazenar mais\n", MAX_PESSOAS);
            return cont;
        }

        enQueue(pq, new_Pessoa(nome, idade));
        cont++;
    }
    fclose(arq);
    return cont;
}

Pessoa getPessoa(){
    Pessoa p;
    printf("Informe o nome da pessoa: ");
    scanf(" %63[^\n]", p.nome.data);

    printf("Informe a idade da pessoa: ");
    scanf(" %d", &p.idade);

    p.prioridade = getPriority(p);
    return p;
}

void ChegadaDePessoa(PriorityQueue* pq, Pessoa p){
    enQueue(pq, p);
    printf("%s foi inserido(a) na fila\n", p.nome.data);
}

void AtendimentoDePessoa(PriorityQueue* pq){
    Pessoa atendida;
    if(pq->size){
        atendida = deQueue(pq);
        printf("%s foi atendido(a)\n", atendida.nome.data);

        (atendida.prioridade == HIGH) ? results.atendidos_Cpr++ : results.atendidos_Spr++;
        results.atendidas[results.total_atendidos++] = atendida;
    }else{
        printf("Fila vazia\n");
    }
}

int main(){
    results = new_Estatisticas();
    PriorityQueue* fila = new_priorityQueue();
    const char* filename = "clientes.txt";

    system("clear");
    while(1){
        int op = Menu();
        switch(op){
            case '1':
                system("clear");
                Pessoa aux = getPessoa();
                ChegadaDePessoa(fila, aux);
                break;
            case '2':
                system("clear");   
                AtendimentoDePessoa(fila);
                break;
            case '3':
                system("clear");  
                printpriorityQueue(fila);
                break;
            case '4':
                system("clear");  
                int lido = ReadFile(filename, fila);
                printf("%s", lido ? "Arquivo lido com sucesso!\n" : "Falha ao ler o arquivo\n");
                break;
            case '0':
                if(fila->size){
                    system("clear");  
                    printf("Ainda ha %d pessoas na fila.\n"
                        "O programa so finaliza quando nao ha mais ninguem na fila de atendimento\n",
                        fila->size
                    );
                    continue;
                }
                system("clear");  
                printEstatisticas();
                delete_priorityQueue(&fila);
                return 0;
        }
    }
}
