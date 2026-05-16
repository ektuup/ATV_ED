#include <iostream>
#include <string>
#include <cmath>
#include "SortVector.hpp"
#include <random>

using namespace std;

int SortVector::partition(int begin, int end){
	int i = begin, j = end;
	string* pivo = array.data[i];
	
	while(1){
		while(i <= end && *array.data[i] <= *pivo) i++;
		while(j >= begin + 1 && *array.data[j] > *pivo) j--;
		if(i >= j) break;
		std::swap(array.data[i], array.data[j]);
		i++, j--;
	}
	std::swap(array.data[j], array.data[begin]);
	return j;
}

int SortVector::partition_random(int begin, int end){
	int index_pivo = begin + (rand() % (end - begin + 1));
	std::swap(array.data[index_pivo], array.data[begin]);
	
	string* pivo = array.data[begin];
	int i = begin, j = end;
	
	while(1){
		while(i <= end && *array.data[i] <= *pivo) i++;
		while(j >= begin + 1 && *array.data[j] > *pivo) j--;
		if(i >= j) break;
		std::swap(array.data[i], array.data[j]);
		i++, j--;
	}
	std::swap(array.data[j], array.data[begin]);
	return j;
}

void SortVector::sink(int k, int n){
	while(2*k + 1 < n){
		int j = 2*k + 1;
		if (j < n - 1 && *array.data[j] < *array.data[j + 1]) j++;
		if(*array.data[k] >= *array.data[j]) break;
		std::swap(array.data[k], array.data[j]);
		k = j;
	}
}

void SortVector::__quicksort(int begin, int end){
	if (begin >= end) return;

	int p = partition(begin, end);
	__quicksort(begin, p - 1);
	__quicksort(p + 1, end);
}

void SortVector::__quicksort_random(int begin, int end){
	if (begin >= end) return;

	int p = partition_random(begin, end);
	__quicksort_random(begin, p - 1);
	__quicksort_random(p + 1, end);
}

void SortVector::__insertion(int begin, int end){
	for(int i = begin + 1; i <= end; i++)
	{
		int j = i - 1;
		string* current = array.data[i];

		while(j >= begin && *array.data[j] > *current){
			array.data[j + 1] = array.data[j];
			j--;
		}

		array.data[j + 1] = current;
	}
}

void SortVector::__merge(string** aux, int begin, int mid, int end){

	int i = begin, j = mid + 1, k = begin;

	while(i <= mid && j <= end){
		if(*aux[i] <= *aux[j]){
			array.data[k++] = aux[i++];
		}else{
			array.data[k++] = aux[j++];
		}
	}

	while(i <= mid) array.data[k++] = aux[i++];
	while(j <= end) array.data[k++] = aux[j++];
}

void SortVector::__hibrid_mergesort(string** aux, int begin, int end){
	if (end - begin + 1 <= 24) {
		__insertion(begin, end);
	}else{
		int mid = (begin + end) >> 1;
		__hibrid_mergesort(aux, begin, mid);
		__hibrid_mergesort(aux, mid + 1, end);
		__merge(aux, begin, mid, end);
	}
}

string SortVector::at(int i){
	if(i >= 0 and i < array.index)
		return *array.data[i];
	return NULL;
}

int SortVector::len(){
	return array.index;
}

void SortVector::clear(){
	for(int i = 0; i < array.index; i++)
		delete array.data[i];
	array.index = 0;
	array.capacity = MIN_CAPACITY;
	delete [] array.data;
	array.data = new string*[array.capacity];
}

void SortVector::copy(SortVector* other){
	clear();
	for(int i = 0; i < other->len(); i++)
		insert(other->at(i).c_str());
}

void SortVector::exch(int i, int j){
	string* aux = array.data[i];
	array.data[i] = array.data[j];
	array.data[j] = aux;
}

void SortVector::insert(const char* value){
	realoc();
	array.data[array.index++] = new string(value);
}

void SortVector::realoc()
{
	if(array.index + 1 >= array.capacity){
		array.capacity *= GROWUP;
		string **aux_array = new string*[array.capacity];

		for(int i = 0; i < array.index; i++)
			aux_array[i] = array.data[i];
		
		delete[] array.data;
		array.data = aux_array;
	}
}

void SortVector::InsertionSort(){
	__insertion(0, array.index - 1);
}

void SortVector::SelectionSort()
{
	for(int i = 0; i < array.index; i++)
	{
		int min = i;

		for(int j = i + 1; j < array.index; j++)
			if(*array.data[j] < *array.data[min])
				min = j;	

		exch(i, min);
	}

}

void SortVector::BubbleSort()
{
	for(int i = 0; i < array.index; i++){
		int swaped = 0;
		for(int j = 0; j < array.index - 1 - i; j++){
			if(*array.data[j] > *array.data[j + 1]){
				exch(j, j + 1);
				swaped = 1;
			}
		}
		if(!swaped) return;
	}
}

void SortVector::ShellSort()
{
	int j, i;
	string* aux = NULL;

	float k = log(array.index + 1)/log(3);
	k = floor(k + 0.5);
	int h = (pow(3, k) - 1) / 2;

	while(h > 0)
	{
		for(int i = 0; i < array.index - h; i++)
		{
			if(*array.data[i] > *array.data[i + h])
			{
				aux = array.data[i + h];
				array.data[i + h] = array.data[i];
				array.data[i] = aux;
				j = i - h;
				while(j >= 0)
				{
					if(*aux < *array.data[j])
					{
						array.data[j + h] = array.data[j];
						array.data[j] = aux;
					}
					else break;
					j -= h;
				}
			}
		}
		h = (h - 1) / 3;
	}
}

void SortVector::HeapSort()
{
	int k;
	for(k = (array.index - 1)/2; k >= 0; k--)
		sink(k, array.index);
	
	k = array.index;
	while(k > 0){
		exch(0, --k);
		sink(0, k);
	}
}	

void SortVector::MergeSort_BottomUp()
{
	if (array.index <= 1) return;

	int n = array.index;
	string** temp = new string*[n];

	for (int bloco = 1; bloco < n; bloco *= 2) 
	{
		for (int i = 0; i < n; i += 2 * bloco) 
		{
			int left = i;
			int mid = std::min(i + bloco, n);
			int right = std::min(i + 2 * bloco, n);

			int idx_esq = left;    
			int idx_dir = mid;    
			int idx_temp = left;

			while (idx_esq < mid && idx_dir < right) {
				if (*array.data[idx_esq] <= *array.data[idx_dir])
					temp[idx_temp++] = array.data[idx_esq++];
				else
					temp[idx_temp++] = array.data[idx_dir++];
			}

			while (idx_esq < mid) temp[idx_temp++] = array.data[idx_esq++];
			while (idx_dir < right) temp[idx_temp++] = array.data[idx_dir++];
		}

		for (int i = 0; i < n; i++) {
			array.data[i] = temp[i];
		}
	}

	delete[] temp;
}

void SortVector::Hibrid_MergeSort(){
	string** aux = new string*[array.index];
	for(int i = 0; i < array.index; i++){
		aux[i] = array.data[i];
	}
	__hibrid_mergesort(aux, 0, array.index - 1);
	delete[] aux;
}

void SortVector::QuickSort(){
	__quicksort(0, array.index - 1);
}

void SortVector::QuickSort_Random(){
	__quicksort_random(0, array.index - 1);
}

SortVector::~SortVector(){
	for(int i = 0; i < array.index; i++)
		delete array.data[i];
	delete[] array.data;
	array.data = NULL;
}