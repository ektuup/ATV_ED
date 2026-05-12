#include <iostream>
#include <string>
#include <cmath>
#define troca(x, y){do{string aux = x; x = y; y = aux;}while(0);}
using namespace std;

struct S_Array
{
	int Size = 3;
	int Index = 0;
	string *Arr = new string [Size];
};

class Array
{
public:
	S_Array array;

	void insert(string value){
		if(array.Index == array.Size)
			realoc();
		array.Arr[array.Index++] = value;
	}
	
	void realoc()
	{
		array.Size *= 2;
		string *aux_array = new string[array.Size];

		for(int i = 0; i < array.Index; i++)
			aux_array[i] = array.Arr[i];
		
		delete[] array.Arr;
		array.Arr = aux_array;
	}

	void InsertionSort()
	{
		for(int i = 1; i < array.Index; i++)
		{
			int j = i - 1;
			string current = array.Arr[i];

			while(j >= 0 && array.Arr[j] > current){
				array.Arr[j + 1] = array.Arr[j];
				j--;
			}

			array.Arr[j + 1] = current;
		}
	}

	void SelectionSort()
	{
		for(int i = 0; i < array.Index; i++)
		{
			int min = i;

			for(int j = i + 1; j < array.Index; j++)
				if(array.Arr[j] < array.Arr[min])
					min = j;	

			troca(array.Arr[i], array.Arr[min]);
		}

	}

	void BubbleSort()
	{
		for(int i = 0; i < array.Index; i++)
			for(int j = 0; j < array.Index - 1 - i; j++)
				if(array.Arr[j] > array.Arr[j + 1])
					troca(array.Arr[j], array.Arr[j + 1]);
	}

	void ShellSort()
	{
		int j, i;
		string aux;

		float k = log(array.Index + 1)/log(3);
		k = floor(k + 0.5);
		int h = (pow(3, k) - 1) / 2;

		while(h > 0)
		{
			for(int i = 0; i < array.Index - h; i++)
			{
				if(array.Arr[i] > array.Arr[i + h])
				{
					aux = array.Arr[i + h];
					array.Arr[i + h] = array.Arr[i];
					array.Arr[i] = aux;
					j = i - h;
					while(j >= 0)
					{
						if(aux < array.Arr[j])
						{
							array.Arr[j + h] = array.Arr[j];
							array.Arr[j] = aux;
						}
						else break;
						j -= h;
					}
				}
			}
			h = (h - 1) / 3;
		}
	}

	void HeapSort()
	{
	}	

	void MergeSort()
	{
		if (array.Index <= 1) return;

		int n = array.Index;
		string* temp = new string[n];

		for (int bloco = 1; bloco < n; bloco *= 2) 
		{
			for (int i = 0; i < n; i += 2 * bloco) 
			{
				int left = i;
				int mid = min(i + bloco, n);
				int right = min(i + 2 * bloco, n);

				int idx_esq = left;    
				int idx_dir = mid;    
				int idx_temp = left;

				while (idx_esq < mid && idx_dir < right) {
					if (array.Arr[idx_esq] <= array.Arr[idx_dir])
						temp[idx_temp++] = array.Arr[idx_esq++];
					else
						temp[idx_temp++] = array.Arr[idx_dir++];
				}

				while (idx_esq < mid) temp[idx_temp++] = array.Arr[idx_esq++];
				while (idx_dir < right) temp[idx_temp++] = array.Arr[idx_dir++];
			}

			for (int i = 0; i < n; i++) {
				array.Arr[i] = temp[i];
			}
		}

		delete[] temp;
	}

	void QuickSort()
	{
	}
		
	~Array(){
		delete[] array.Arr;
	}
};
