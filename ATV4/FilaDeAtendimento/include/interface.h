#ifndef _INTERFACE_H_
#define _INTERFACE_H_

#include "priorityQueue.h"

void Header();
void ClearScreen();
int Menu();
void printPessoasAtendidas();
void printEstatisticas();
int ReadFile(const char* filename, PriorityQueue* pq);
Pessoa getPessoa();
void ChegadaDePessoa(PriorityQueue* pq, Pessoa p);
void AtendimentoDePessoa(PriorityQueue* pq);

#endif