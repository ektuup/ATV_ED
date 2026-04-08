#include "priorityQueue.h"
#include "interface.h"

Estatisticas results;

int main(){
    results = new_Estatisticas();
    PriorityQueue* fila = new_priorityQueue();
    String filename;
    Pessoa aux;
    int flag = 1, lido;

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
                printpriorityQueue(fila);
                break;
            case '4':
                ClearScreen();  
                // printf("Informe o nome do arquivo que voce deseja")
                lido = ReadFile(filename, fila);
                printf("%s", lido ? "Arquivo lido com sucesso!\n" : "Falha ao ler o arquivo\n");
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
            }
        }
        ClearScreen();  
        printEstatisticas();
        delete_priorityQueue(&fila);
        return 0;
    }
