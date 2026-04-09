#include "interface.h"

void ClearScreen(){
    system("clear");
}

void Header(){
    printf("----------------FILA-DE-ATENDIMENTO----------------\n");
}

int Menu(){
    String op;
    char dig;
    Header();
    printf("Politica de prioridade: Pessoas com a partir de\n60 anos tem prioridade na fila\n");

    printf("informe uma opção:\n\n"
           "\t1 - Chegada de pessoa para atendimento\n"
           "\t2 - Atendimento de uma pesssoa\n"
           "\t3 - Listar todas as pessoas da fila\n"
           "\t4 - Ler arquivo de atendimento\n"
           "\t5 - Atender Geral\n"
           "\t0 - Sair\n"
    );
    
    while(1){
        scanf(" %63[^\n]", op.data);
        dig = op.data[0];
        if(strlen(op.data) == 1 && ('0' <= dig && dig <= '5')) break;
        printf("Informe uma opcao valida! (0, 1, 2, 3 ou 4)\n");
    }
    return dig;
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
}

int ReadFile(String filename, PriorityQueue* pq){
    FILE* arq = fopen(filename.data, "r");
    if(arq == NULL) return -1;

    String line = new_String(""), nome;
    int cont = 0, olha, idade;
    
    while(fgets(line.data, sizeof(line.data), arq)){
        line.data[strcspn(line.data, "\n")] = '\0'; //remove o '\n' absorvido pelo fgets
        int i = 0;
        while(line.data[i] == ' ') i++; 
        if(line.data[i] == '\0') continue;  //ignora linhas vazias
        
        int lido = sscanf(&line.data[i], "%63[^;];%d", nome.data, &idade); //le a partir da posição que nao tem mais espaços
        
        if(lido < 2){
            line.data[strcspn(line.data, "\n")] = '\0';

            printf("Erro em '%s' : cada linha do arquivo deve ser do formato 'nome;idade'\n", line.data);
            for(int k = 0; k < cont; k++){
                deQueue(pq);
            }
            return 0;
        }
        
        enQueue(pq, new_Pessoa(nome, idade));
        cont++;
    }
    fclose(arq);
    return cont;
}

Pessoa getPessoa(){
    Header();
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
    printf("%s foi inserido(a) %sna fila\n",  p.nome.data, p.prioridade == HIGH ? "com prioridade " : "");
}

void AtendimentoDePessoa(PriorityQueue* pq){
    Pessoa atendida;
    if(pq->size){
        atendida = deQueue(pq);
        printf("Pessoa chamada: %s%s\n", atendida.prioridade == HIGH ? "*" : "", atendida.nome.data);
        (atendida.prioridade == HIGH) ? results.atendidos_Cpr++ : results.atendidos_Spr++;
        results.atendidas[results.total_atendidos++] = atendida;
    }else{
        printf("Fila vazia\n");
    }
}

void AtenderGeral(PriorityQueue* pq){
    int i = 0;
    printf("----------------PESSOAS-ATENDIDAS----------------\n");
    while(pq->size){
        Pessoa atendida = deQueue(pq);
        printf("%d - %s%s\n", ++i, atendida.prioridade == HIGH ? "*" : "", atendida.nome.data);
        (atendida.prioridade == HIGH) ? results.atendidos_Cpr++ : results.atendidos_Spr++;
        results.atendidas[results.total_atendidos++] = atendida;
    }
}

String getFilePath(){
    String filename, filepath = new_String("inputs/");
    Header();
    printf("informe o nome do arquivo que voce quer ler (nome.txt):\n");
    scanf(" %63[^\n]", filename.data);
    strcat(filepath.data, filename.data);
    return filepath;
}

void LerDoArquivo(String filepath, PriorityQueue* pq){    
    int lido = ReadFile(filepath, pq);

    if(lido > 0){
        printf("Arquivo lido com sucesso!\n");
    }else if(lido == 0){
        printf("Falha ao ler o arquivo\n");
    }else if(lido == -1){
        printf("Arquivo nao encontrado\n");
    }else if(lido == MAX_PESSOAS){
        printf("Erro: capacidade maxima de pessoas permitido é %d. por favor aumente a capacidade caso queira armazenar mais\n", MAX_PESSOAS);
    }
}

void EnterClear(){
    printf("Pressione Enter para voltar ao menu...\n");
    getchar(); getchar();
    ClearScreen();
}