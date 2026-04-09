#include <stdio.h>
#include "types.h"
#include "recentList.h"

RecentList* new_RecentList(){
    RecentList* S = malloc(sizeof(RecentList));
    S->list = NULL;
    S->len = 0;
    return S;
}

void list_add(RecentList* S, Pessoa p){
    node* new = new_node(p), *temp = NULL, *aux = S->list;
    
    addNode(&S->list, new);

    aux = S->list;
    if(S->len < CUT_QUEUE){
        S->len++;
    }else{
        temp = S->list;
        S->list = S->list->next;
        free(temp);
    }
}

int in_list(RecentList *S ,Priority pr){
    node* aux = S->list;
    while(aux){
        if(pr == aux->data.prioridade) return 1;
        aux = aux->next;
    }
    return 0;
}

void delete_Recentlist(RecentList* S){
    node* aux;
    while(S->list){
        aux = S->list;
        S->list = S->list->next;
        free(aux);
    }
    free(S);
}

void print_list(RecentList* S){
    node* aux = S->list;
    while(aux){
        printf("%s\n", aux->data.nome.data);
        aux = aux->next;
    }
}