#include "priorityQueue.h"
#include "interface.h"

Estatisticas results;

int main(){
    results = new_Estatisticas();
    PriorityQueue* fila = new_priorityQueue();
    String filename;
    Pessoa aux;
    int flag = 1, enter;

    ClearScreen();
    while(flag){
        int op = Menu();
        switch(op){
            case '1':
                ClearScreen();
                aux = getPessoa();
                ChegadaDePessoa(fila, aux);
                break;
            case '2':
                ClearScreen();   
                AtendimentoDePessoa(fila);
                break;
            case '3':
                ClearScreen();  
                Header();
                printpriorityQueue(fila);
                printf("Pressione Enter para voltar ao menu...\n");
                getchar(); getchar();
                ClearScreen();
                break;
            case '4':
                ClearScreen();  
                filename = getFilename();
                LerDoArquivo(filename, fila);
                break;
            case '0':
                if(fila->size){
                    ClearScreen();  
                    printf("Ainda ha %d pessoas na fila de atendimento.\n"
                        "O programa so finaliza quando nao ha mais ninguem em espera\n",
                        fila->size
                    );
                }else{
                    flag = 0;
                }
                break;
        }
    }
    ClearScreen();  
    printEstatisticas();
    delete_priorityQueue(&fila);
    return 0;
}