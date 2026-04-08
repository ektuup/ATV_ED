#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct no{
	char nome_cliente[50];
	int valor_prioridade;
	struct no* proximo_cliente;
}no;

typedef struct{
	no* head;
	no* tail;
}Queue;


void finalizar_fila(Queue* q){
	no* controle = q->head;
	no* aux = NULL;
	while(controle != NULL){
		aux = controle;
		controle = controle->proximo_cliente;
		free(aux);
	}
	q->head = NULL;
	q->tail = NULL;
}

//procura o no antecessor que contem o valor menor do que o "valor_prioridade"
no* procurar_prioridade(Queue* q, int valor_prioridade){
	no* controle = q->head;
	while(controle->proximo_cliente != NULL && valor_prioridade <= controle->proximo_cliente->valor_prioridade){
		controle = controle->proximo_cliente;
	}
	return controle;
}

void inserir_novo_cliente_p(Queue* q, int valor_prioridade, char nome_cliente[]){
	no* novo_cliente = malloc(sizeof(no));
	novo_cliente->proximo_cliente = NULL;
	strcpy(novo_cliente->nome_cliente, nome_cliente);
	novo_cliente->valor_prioridade = valor_prioridade;

	//se não houver nenhum elemento na fila ainda
	if(q->head == NULL){
		q->head = novo_cliente;
		q->tail = novo_cliente;
		return;
	}

	//caso ainda a inserção é no head, portanto não há cliente anterior
	if(valor_prioridade > q->head->valor_prioridade){
		novo_cliente->proximo_cliente = q->head;
		q->head = novo_cliente;
		return;
	}

	//inserção entre dois clientes
	no* cliente_antecessor = procurar_prioridade(q,valor_prioridade);
	novo_cliente->proximo_cliente = cliente_antecessor->proximo_cliente;
	cliente_antecessor->proximo_cliente = novo_cliente;

	//caso de inserção no tail, ou seja o próximo cliente do cliente antecessor é null
	if(novo_cliente->proximo_cliente == NULL){
		q->tail = novo_cliente;
	}
}

void inserir_novo_cliente_sp(Queue* q, char nome_cliente[]){
	no* novo_cliente = malloc(sizeof(no));
	novo_cliente->valor_prioridade = 0;
	novo_cliente->proximo_cliente = NULL;
	strcpy(novo_cliente->nome_cliente, nome_cliente);

	//se não houver nenhum elemento na fila ainda
	if(q->head == NULL){
		q->head = novo_cliente;
		q->tail = novo_cliente;
		return;
	}

	q->tail->proximo_cliente = novo_cliente;
	q->tail = novo_cliente;

}

void remover_cliente(Queue* f, int quantidade_remover){
	int cont = 0;
	no* controle = f->head;
	while(controle != NULL && cont != quantidade_remover){
		no* aux = controle;
		f->head = controle->proximo_cliente;
		controle = controle->proximo_cliente;
		free(aux);
		cont++;
	}	
}

void atender_cliente(Queue* sp, Queue* p){
	// sp = sem prioridade, p = com prioridade
	if(sp->head ==  NULL && p->head == NULL){
		printf("a fila está vazia.\n");
		return;
	}

	// se nao tiver pessoas na fila com prioridade, atenda 3 ou mais clientes da fila sem prioridade
	if(p->head == NULL){
		remover_cliente(sp,3);
	}
	else{
		//há pessoas com prioridade, mas tem as pessoas sem prioridades necessarias para a politica?
		no* controle = sp->head;
		int cont = 0;
		while(controle != NULL && cont != 3){
			cont++;
			controle = controle->proximo_cliente;
		} // ao final desse bloco teremos quantas pessoas tem na fial sem prioridade
		if(cont == 3){
			remover_cliente(sp,3);
			//logo apos removemos uma pessoa da fila com prioridade
			no* aux = p->head;
			p->head = p->head->proximo_cliente;
			free(aux);
			// cumprindo a politica
		}else{
			//e se nao tiver pessoas sem prioridade o suficiente para a politica?
			remover_cliente(p,3);
			//retiramos 3 ou mais da fila com prioridade
		}
	}
}

void mostrar_todos_clientes(Queue* q){
	no* controle = q->head;

	if(q->head ==  NULL){
		printf("a fila está vazia.\n");
		return;
	}

	int indice_fila = 1;
	while(controle != NULL){
		if(controle->valor_prioridade != 0)
			printf("cliente %d: %s* -> prioridade: %d\n", indice_fila, controle->nome_cliente, controle->valor_prioridade);
		else
			printf("cliente %d: %s\n", indice_fila, controle->nome_cliente);
		controle = controle->proximo_cliente;
		indice_fila++;
	}
}

Queue* iniciar_fila(){
	Queue* q = malloc(sizeof(Queue));
	q->head = NULL;
	q->tail = NULL;
	return q;
}

void menu(Queue* nova_fila_p, Queue* nova_fila_sp){
	while(1){
		int op = 0;
		printf("-----------------------------------------\n");
		printf("1. Chegada de pessoa para atendimento\n");
		printf("2. Atendimento de uma pessoa\n");
		printf("3. Listar todas as pessoas da fila\n");
		printf("4. Sair\n");
		printf("-----------------------------------------\n");


		scanf(" %d", &op);

		if(op == 1){
			char nome_cliente[50]; 
			printf("digite o nome do cliente:\n");
			scanf("%s", nome_cliente);

			int valor_prioridade = 0;
			int op_prioridade = 0;

			printf("deseja inserir prioridade? 1 - sim, 2 - não\n");
			scanf("%d", &op_prioridade);

			if(op_prioridade == 1){
				printf("inseira o valor da prioridade: \n");
				scanf("%d", &valor_prioridade);
				inserir_novo_cliente_p(nova_fila_p, valor_prioridade, nome_cliente);
			}else{
				inserir_novo_cliente_sp(nova_fila_sp, nome_cliente);
			}

			printf("cliente inserido com sucesso.\n");
		}

		else if(op == 2){
			atender_cliente(nova_fila_sp, nova_fila_p);
		}

		else if(op == 3){
			printf("--- fila com prioridade ---\n");
			mostrar_todos_clientes(nova_fila_p);
			printf("--- fila sem prioridade ---\n");
			mostrar_todos_clientes(nova_fila_sp);
		}

		else if(op == 4){
		    if(nova_fila_p->head == NULL && nova_fila_sp->head == NULL){
		    	printf("encerrando programa...\n");
		        break;
		    } else {
		        printf("ainda há pessoas na fila. \n");
		    }
		}
		else
		    printf("opção inválida\n");
	}
}

int main()
{
	system("clear");
	Queue* nova_fila_p = iniciar_fila();
	Queue* nova_fila_sp = iniciar_fila();

	inserir_novo_cliente_p(nova_fila_p, 13, "p13");
	inserir_novo_cliente_p(nova_fila_p, 12, "p12");
	inserir_novo_cliente_p(nova_fila_p, 11, "p11");
	inserir_novo_cliente_p(nova_fila_p, 8, "p8");
	inserir_novo_cliente_p(nova_fila_p, 7, "p7");
	inserir_novo_cliente_p(nova_fila_p, 5, "p5");

	inserir_novo_cliente_sp(nova_fila_sp, "p1");
	inserir_novo_cliente_sp(nova_fila_sp, "p2");
	inserir_novo_cliente_sp(nova_fila_sp, "p3");
	inserir_novo_cliente_sp(nova_fila_sp, "p4");
	inserir_novo_cliente_sp(nova_fila_sp, "p6");
	inserir_novo_cliente_sp(nova_fila_sp, "p9");
	inserir_novo_cliente_sp(nova_fila_sp, "p10");
	inserir_novo_cliente_sp(nova_fila_sp, "p14");
	inserir_novo_cliente_sp(nova_fila_sp, "p15");
	inserir_novo_cliente_sp(nova_fila_sp, "p16");
	inserir_novo_cliente_sp(nova_fila_sp, "p17");
	inserir_novo_cliente_sp(nova_fila_sp, "p18");
	inserir_novo_cliente_sp(nova_fila_sp, "p19");

	menu(nova_fila_p, nova_fila_sp);

	finalizar_fila(nova_fila_p);
	finalizar_fila(nova_fila_sp);
	return 0;
}

// ta faltando atualizar o tail na hora de atender, por enquanto isso ainda nao deu problema :D

/* caso teste 1: 
	inserir_novo_cliente_p(nova_fila_p, 13, "p13");
	inserir_novo_cliente_p(nova_fila_p, 12, "p12");
	inserir_novo_cliente_p(nova_fila_p, 11, "p11");
	inserir_novo_cliente_p(nova_fila_p, 8, "p8");
	inserir_novo_cliente_p(nova_fila_p, 7, "p7");
	inserir_novo_cliente_p(nova_fila_p, 5, "p5");

	inserir_novo_cliente_sp(nova_fila_sp, "p1");
	inserir_novo_cliente_sp(nova_fila_sp, "p2");
	inserir_novo_cliente_sp(nova_fila_sp, "p3");
	inserir_novo_cliente_sp(nova_fila_sp, "p4");
	inserir_novo_cliente_sp(nova_fila_sp, "p6");
	inserir_novo_cliente_sp(nova_fila_sp, "p9");
	inserir_novo_cliente_sp(nova_fila_sp, "p10");
	inserir_novo_cliente_sp(nova_fila_sp, "p14");
	inserir_novo_cliente_sp(nova_fila_sp, "p15");
	inserir_novo_cliente_sp(nova_fila_sp, "p16");
	inserir_novo_cliente_sp(nova_fila_sp, "p17");
	inserir_novo_cliente_sp(nova_fila_sp, "p18");
	inserir_novo_cliente_sp(nova_fila_sp, "p19");
	inserir_novo_cliente_sp(nova_fila_sp, "p20");
*/
