#ifndef _TYPES_H_
#define _TYPES_H_

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

typedef struct Pessoa{
    String nome;
    int idade;
    Priority prioridade;
}Pessoa;

typedef struct node{
    Pessoa data;
    struct node* next;
}node;

typedef struct{
    int atendidos_Spr, atendidos_Cpr, total_atendidos;
    float percent_Spr, percent_Cpr;
    Pessoa atendidas[MAX_PESSOAS];
}Estatisticas;

static inline String new_String(const char* str){
    String S;
    if(str == NULL){
        S.data[0] = '\0'; //caso str seja um ponteiro nulo, a string é vazia;
        return S;
    }
    strcpy(S.data, str);
    return S;
}

//construtor de Pessoa
static inline Pessoa new_Pessoa(String nome, int idade){ 
    Pessoa p = {nome, idade};
    return p;
}

static inline node* new_node(Pessoa p){
    node* new = malloc(sizeof(node));
    new->data = p;
    new->next = NULL;
    return new;
}

static inline void addNode(node** no, node* new){
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

static inline Estatisticas new_Estatisticas(){
    Estatisticas aux = {0, 0, 0, 0, 0};
    return aux;
}

extern Estatisticas results;

#endif