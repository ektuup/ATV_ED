#ifndef PET_HPP
#define PET_HPP

#include <string>

#include <iostream>
using namespace std;

#define GROWUP 2
#define MIN_CAPACITY 100000

struct Array{
	int capacity = MIN_CAPACITY;
	int index = 0;
	string **data = new string*[capacity];
};

class SortVector {
public:
	string at(int i);
	int len();
	void exch(int i, int j);
	void copy(SortVector* other);
	void insert(const char* value);
	void InsertionSort();
	void SelectionSort();
	void BubbleSort();
	void ShellSort();
	void HeapSort();
	void MergeSort_BottomUp();
	void Hibrid_MergeSort();
	void QuickSort();
	void QuickSort_Random();
	void clear();
	~SortVector();
	
private:
	struct Array array;
	void realoc();
	int partition(int begin, int end);
	int partition_random(int begin, int end);
	void sink(int k, int n);
	void __insertion(int begin, int end);
    void __merge(string** aux, int begin, int mid, int end);
	void __hibrid_mergesort(string** aux, int begin, int end);
	void __quicksort(int begin, int end);
	void __quicksort_random(int begin, int end);
};

#endif