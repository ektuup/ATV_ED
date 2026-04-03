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
	//obs: as prioridades repetidas ja foram tratadas
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

void atender_cliente(Queue* sp, Queue* p){
	// sp = sem prioridade, p = com prioridade
	if(p->head == NULL){
		int cont = 0;
		no* controle = sp->head;
		while(controle != NULL && cont != 3){
			no* aux = controle;
			sp->head = controle->proximo_cliente;
			controle = controle->proximo_cliente;
			free(aux);
			cont++;
		}
	}
	else{
		no* controle = sp->head;
		int cont = 0;
		while(controle != NULL && cont != 3){
			cont++;
			controle = controle->proximo_cliente;
		}

		if(cont == 3){
			for (int i = 0; i < 3; ++i){
				no* aux = sp->head;
				sp->head = sp->head->proximo_cliente;
				free(aux);
			}
			no* aux = p->head;
			p->head = p->head->proximo_cliente;
			free(aux);
		}else{
			int cont = 0;
			no* controle = p->head;
			while(controle != NULL && cont != 3){
				no* aux = controle;
				p->head = controle->proximo_cliente;
				free(aux);
				cont++;
				controle = controle->proximo_cliente;
			}
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
			printf("cliente %d: %s -> prioridade: %d\n", indice_fila, controle->nome_cliente, controle->valor_prioridade);
		else
			printf("cliente %d: %s*\n", indice_fila, controle->nome_cliente);
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
	int op = 0;
	do{
		printf("1. chegada de pessoa para atendimento\n");
		printf("2. atendimento de uma pessoa\n");
		printf("3. listar todas as pessoas da fila\n");
		printf("4. sair\n");

		scanf("%d", &op);

		if(op == 1){
			char nome_cliente[50]; 
			printf("digite o nome do cliente:\n");
			scanf("%s", nome_cliente);

			int valor_prioridade = 0;
			int op_prioridade = 0;

			printf("deseja inserir prioridade? 1 - sim, 2 - não\n");
			scanf("%d", &op_prioridade);

			if(op_prioridade == 1){
				printf("Inseira o valor da prioridade: \n");
				scanf("%d", &valor_prioridade);
				inserir_novo_cliente_p(nova_fila_p, valor_prioridade, nome_cliente);
			}else{
				inserir_novo_cliente_sp(nova_fila_sp, nome_cliente);
			}

			printf("cliente inserido com sucesso.\n");
		}

		if(op == 2)
			atender_cliente(nova_fila_sp, nova_fila_p);

		if(op == 3){
			printf("--- fila com prioridade ---\n");
			mostrar_todos_clientes(nova_fila_p);
			printf("--- fila sem prioridade ---\n");
			mostrar_todos_clientes(nova_fila_sp);	
		}
	}while(op != 4);
}

int main()
{
	Queue* nova_fila_p = iniciar_fila();
	Queue* nova_fila_sp = iniciar_fila();

	menu(nova_fila_p, nova_fila_sp);

	finalizar_fila(nova_fila_p);
	finalizar_fila(nova_fila_sp);
	return 0;
}
