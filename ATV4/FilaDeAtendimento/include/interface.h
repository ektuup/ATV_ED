#ifndef _INTERFACE_H_
#define _INTERFACE_H_

#include "priorityQueue.h"

void Header();
void ClearScreen();
int Menu();
void printPessoasAtendidas();
void printEstatisticas();
int ReadFile(String filename, PriorityQueue* pq);
Pessoa getPessoa();
void ChegadaDePessoa(PriorityQueue* pq, Pessoa p);
void LerDoArquivo(String filename, PriorityQueue* pq);
void AtendimentoDePessoa(PriorityQueue* pq);
String getFilename();

#endif