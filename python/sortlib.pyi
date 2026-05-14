# sortlib.pyi

class SortVector:
    def __init__(self) -> None: ...
    
    def insert(self, value: str) -> None:
        """Insere uma string no vetor"""
        ...

    def clear(self) -> None:
        """esvazia o array"""
        ...

    def at(self, index: int) -> str:
        """Retorna a string no índice i"""
        ...

    def len(self) -> int:
        """Retorna o tamanho do vetor"""
        ...

    def quick_sort(self) -> None:
        """Ordena usando QuickSort"""
        ...

    def hibrid_merge_sort(self) -> None:
        """Ordena usando MergeSort Hibrido com Insertion"""
        ...
        
    def shell_sort(self) -> None:
        """Ordena usando ShellSort"""
        ...

    def heap_sort(self) -> None:
        """Ordena usando HeapSort"""
        ...

    def bubble_sort(self) -> None:
        """Ordena usando BubbleSort"""
        ...

    def selection_sort(self) -> None:
        """Ordena usando SelectionSort"""
        ...

    def insertion_sort(self) -> None:
        """Ordena usando InsertionSort"""
        ...

    def merge_sort(self) -> None:
        """Ordena usando MergeSort"""
        ...