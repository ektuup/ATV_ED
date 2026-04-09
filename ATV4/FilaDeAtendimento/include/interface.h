#ifndef _INTERFACE_H_
#define _INTERFACE_H_

#include "priorityQueue.h"

void Header();
void AtenderGeral(PriorityQueue *pq);
void ClearScreen();
int Menu();
void printEstatisticas();
int ReadFile(String filename, PriorityQueue* pq);
Pessoa getPessoa();
void EnterClear();
void ChegadaDePessoa(PriorityQueue* pq, Pessoa p);
void LerDoArquivo(String filename, PriorityQueue* pq);
void AtendimentoDePessoa(PriorityQueue* pq);
String getFilePath();

#endif