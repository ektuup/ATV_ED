from matplotlib import pyplot as plt
import numpy as np
import csv

all_algorithms = [
    "Bubblesort",
    "Selectionsort",
    "Insertionsort",
    "Shellsort" ,
    "Mergesort-BottomUp",
    "Mergesort-Híbrido",
    "Quicksort" ,
    "QuickSort Aleatorizado",
    "Heapsort"
]

map_files = {'nomes100k.txt':100000, 'nomes250k.txt': 250000, 'nomes500k.txt': 500000, 'nomes1m.txt': 1000000}
num_words = {}

def get_average():
    average_time_sort = {}
    cont_sort = {}

    with open('estatisticas_ordenacao.csv', 'r', encoding="utf-8") as fcsv:
        scanner = csv.DictReader(fcsv, delimiter=',')

        average_time_sort = {}
        cont_sort = {}
        for row in scanner:

            fname = row['Arquivo']
            num_words[fname] = map_files[fname]
            if not fname in average_time_sort:
                average_time_sort[fname] = {}
            if not fname in cont_sort:
                cont_sort[fname] = {}

            for sort_name in all_algorithms:
                if sort_name not in average_time_sort[fname]:
                    average_time_sort[fname][sort_name] = 0
                
                if sort_name not in cont_sort[fname]:
                    cont_sort[fname][sort_name] = 0

                try:
                    average_time_sort[fname][sort_name] += float(row[sort_name])
                    cont_sort[fname][sort_name] += 1

                except ValueError:
                    average_time_sort[fname][sort_name] += 0

        for fname in average_time_sort:
            for sort_name in all_algorithms:
                try:
                    average_time_sort[fname][sort_name] /= cont_sort[fname][sort_name]
                except ZeroDivisionError:
                    average_time_sort[fname][sort_name] = None
    return average_time_sort

def linearitmic_regression(x, y):
    x = np.array(x)
    y = np.array(y)
    
    A = np.array([
        [np.sum((x*np.log2(x))**2), np.sum((x**2)*np.log2(x)), np.sum(x*np.log2(x))],
        [np.sum((x**2)*np.log2(x)), np.sum(x**2),               np.sum(x)],
        [np.sum(x*np.log2(x)),      np.sum(x),                  len(x)]
    ])

    B = np.array([
        [np.sum(x*y*np.log2(x)),
        np.sum(x*y),
        np.sum(y)]
    ]).reshape(3, 1)

    X = np.linalg.solve(A, B)

    a, b, c = X[0][0], X[1][0], X[2][0]
    return a, b, c

def x_log_x(a, b, c, x):
    return a*x*np.log2(x) + b*x + c

def x_square(a, b, c, x):
    return a*(x**2) + b*x + c

def quadratic_regression(x, y):
    x = np.array(x)
    y = np.array(y)

    x = x/10000
    A = np.array([
        [np.sum(x**4), np.sum(x**3), np.sum(x**2)],
        [np.sum(x**3), np.sum(x**2), np.sum(x)],
        [np.sum(x**2), np.sum(x), len(x)]
    ])

    B = np.array([
        [np.sum((x**2)*y), np.sum(x*y), np.sum(y)]
    ]).reshape(3, 1)

    X = np.linalg.solve(A, B)

    a, b, c = X[0][0], X[1][0], X[2][0]
    return a/(10000**2), b/10000, c


def plot_graph(regression):
    average_time_sort = get_average()
    x = [i for i in num_words.values()]
    x_text_all = ['100k', '250k', '500k', '1M']
    x_text = [x_text_all[i] for i in range(len(x))]
    y = {}

    for s in all_algorithms:
        if s not in y:
            y[s] = []
        for f in num_words:
            y[s].append(average_time_sort[f][s])

    i = 0
    plt.figure(figsize=(10, 6))
    for s in all_algorithms:
        selected_group = ((i >= 3 and regression == linearitmic_regression) or (i < 3 and regression == quadratic_regression))
        
        if not None in y[s] and selected_group:
            if len(x) >= 3:
                a, b, c = regression(x, y[s])
                x_curva = np.linspace(min(x), max(x), 1000)
                if(regression == linearitmic_regression):
                    y_curva = x_log_x(a, b, c, x_curva)
                else:
                    y_curva = x_square(a, b, c, x_curva)
            else:
                x_curva = np.array(x)
                y_curva = np.array(y[s])

            plt.title('Desempenho de algoritmos de ordenação')
            plt.plot(x_curva, y_curva, label=s)
            plt.scatter(x, y[s], marker='o', s=15)
            plt.xlabel('Tamanho')
            plt.ylabel('Tempo (ms)')
        i+=1

    plt.xticks(x, x_text)
    plt.legend(fontsize=10)
    plt.show()