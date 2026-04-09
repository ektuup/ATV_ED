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
}

no* procurar_prioridade(Queue* q, int valor_prioridade){
	no* controle = q->head;
	while(controle->proximo_cliente != NULL && valor_prioridade <= controle->proximo_cliente->valor_prioridade){
		controle = controle->proximo_cliente;
	}
	return controle;
}

void inserir_novo_cliente(Queue* q, int valor_prioridade, char nome_cliente[]){
	no* novo_cliente = malloc(sizeof(no));
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

void remover_cliente(Queue *q){

	if(q->head ==  NULL){
		printf("a fila está vazia.\n");
		return;
	}
	
	//se o primeiro elemento tiver valor prioridade igual a 0, podemos considerar que todo o resto da fila é igual a zero já que estamos inserindo ordenado
	if(q->head->valor_prioridade == 0){
		finalizar_fila(q);
		return;
	}
	//se o primeiro elemento tiver valor prioridade diferente 0, podemos considerar que todo o resto da fila é diferente de zero já que estamos inserindo ordenado
	if(q->tail->valor_prioridade != 0){
		finalizar_fila(q);
		return;
	}


	if(q->head->valor_prioridade != 0){
		no* aux = q->head;
		q->head = q->head->proximo_cliente;
		free(aux);

		no* controle = q->head;
		int cont = 0;
		while(controle != NULL && controle->proximo_cliente != NULL){
			if(controle->proximo_cliente->valor_prioridade == 0 && cont != 3){
				aux = controle->proximo_cliente;
				controle->proximo_cliente = aux->proximo_cliente;
				free(aux);
				cont++;
			}
			else{
				controle = controle->proximo_cliente;
			}
		}
	}
}

void mostrar_todos_clintes(Queue* q){
	no* controle = q->head;

	if(q->head ==  NULL){
		printf("a fila está vazia.\n");
		return;
	}

	int indice_fila = 1;
	while(controle != NULL){
		if(controle->valor_prioridade == 0)
			printf("cliente %d: %s*\n", indice_fila, controle->nome_cliente);
		else
			printf("cliente %d: %s -> prioridade: %d\n", indice_fila, controle->nome_cliente, controle->valor_prioridade);
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

void menu(Queue* nova_fila){
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
				scanf("%d", &valor_prioridade);
			}

			inserir_novo_cliente(nova_fila, valor_prioridade, nome_cliente);
			printf("cliente inserido com sucesso.\n");
		}

		if(op == 2)
			remover_cliente(nova_fila);

		if(op == 3)
			mostrar_todos_clintes(nova_fila);	
	}while(op != 4);
}

int main()
{
	Queue* nova_fila = iniciar_fila();
	//menu(nova_fila);
	inserir_novo_cliente(nova_fila, 4, "victor");
	inserir_novo_cliente(nova_fila, 5, "cami");
	inserir_novo_cliente(nova_fila, 9, "paula");
	inserir_novo_cliente(nova_fila, 10, "mathews");
	inserir_novo_cliente(nova_fila, 10, "art");
	inserir_novo_cliente(nova_fila, 0, "may");
	inserir_novo_cliente(nova_fila, 0, "sávia");
	inserir_novo_cliente(nova_fila, 11, "heytor");
	inserir_novo_cliente(nova_fila, 0, "glaucio");
	mostrar_todos_clintes(nova_fila);
	printf("head: %s\n", nova_fila->head->nome_cliente);
	printf("tail: %s\n", nova_fila->tail->nome_cliente);

	printf("------------\n");
	printf("testes: \n");
	printf("------------\n");

	remover_cliente(nova_fila);
	mostrar_todos_clintes(nova_fila);
	printf("head: %s\n", nova_fila->head->nome_cliente);
	printf("tail: %s\n", nova_fila->tail->nome_cliente);

	finalizar_fila(nova_fila);
	return 0;
}
