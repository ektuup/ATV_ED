#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <random>
#include <time.h>
#include "SortVector.hpp"

//compilação: g++ -shared -o python/sortlib.so -fpic cpp/src/*.cpp -I /usr/include/python* -Icpp/include 

typedef struct{
    PyObject_HEAD
    SortVector* sort_vector;
}SortVectorObject;

static int SortVector_init(SortVectorObject* self, PyObject* args, PyObject* keys){
    srand(time(NULL));
    self->sort_vector = new SortVector();
    return 0;
}

static void SortVector_delete(SortVectorObject* self){
    delete self->sort_vector;
    Py_TYPE(self)->tp_free((PyObject*)self);
    self = NULL;
}

static PyObject* SortVector_insert(SortVectorObject *self, PyObject *args){
    const char* value;
    if(!PyArg_ParseTuple(args, "s", &value)) return NULL;

    self->sort_vector->insert(value);
    Py_RETURN_NONE;
}

static PyObject* SortVector_at(SortVectorObject* self, PyObject* args){
    int i;
    if(!PyArg_ParseTuple(args, "i", &i)) return NULL;

    std::string* value = self->sort_vector->at(i);
    return Py_BuildValue("s", value->c_str());
}

static PyObject* SortVector_len(SortVectorObject* self, PyObject* args){
    return Py_BuildValue("i", self->sort_vector->len());
}

static PyObject* SortVector_clear(SortVectorObject* self, PyObject* args){
    self->sort_vector->clear();
    Py_RETURN_NONE;
}

static PyObject* SortVector_copy(SortVectorObject* self, PyObject* args){
    PyObject* other_obj;
    if(!PyArg_ParseTuple(args, "O", &other_obj)) return NULL;

    SortVectorObject* other = (SortVectorObject*)other_obj;
    self->sort_vector->copy(other->sort_vector);
    Py_RETURN_NONE;
}

static PyObject* SortVector_QuickSort(SortVectorObject* self, PyObject* args){
    Py_BEGIN_ALLOW_THREADS
    self->sort_vector->QuickSort();
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}

static PyObject* SortVector_QuickSort_Random(SortVectorObject* self, PyObject* args){
    Py_BEGIN_ALLOW_THREADS
    self->sort_vector->QuickSort_Random();
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}
 
 
static PyObject* SortVector_HeapSort(SortVectorObject* self, PyObject* args){
    Py_BEGIN_ALLOW_THREADS
    self->sort_vector->HeapSort();
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}
 
static PyObject* SortVector_MergeSort(SortVectorObject* self, PyObject* args){
    Py_BEGIN_ALLOW_THREADS
    self->sort_vector->MergeSort_BottomUp();
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}
 
static PyObject* SortVector_Hibrid_MergeSort(SortVectorObject* self, PyObject* args){
    Py_BEGIN_ALLOW_THREADS
    self->sort_vector->Hibrid_MergeSort();
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}
 
static PyObject* SortVector_BubbleSort(SortVectorObject* self, PyObject* args){
    Py_BEGIN_ALLOW_THREADS
    self->sort_vector->BubbleSort();
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}
 
static PyObject* SortVector_SelectionSort(SortVectorObject* self, PyObject* args){
    Py_BEGIN_ALLOW_THREADS
    self->sort_vector->SelectionSort();
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}
 
static PyObject* SortVector_InsertionSort(SortVectorObject* self, PyObject* args){
    Py_BEGIN_ALLOW_THREADS
    self->sort_vector->InsertionSort();
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}
 
static PyObject* SortVector_ShellSort(SortVectorObject* self, PyObject* args){
    Py_BEGIN_ALLOW_THREADS
    self->sort_vector->ShellSort();
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}
 
static PyObject* SortVector_exchange(SortVectorObject* self, PyObject* args){
    int i, j;
    if(!PyArg_ParseTuple(args, "ii", &i, &j)) return NULL;
    self->sort_vector->exch(i, j);
    Py_RETURN_NONE;
}

 static PyMethodDef SortVector_methods[] = {
    {"insert", (PyCFunction)SortVector_insert, METH_VARARGS, "Insere uma string"},
    {"at", (PyCFunction)SortVector_at, METH_VARARGS, "Retorna a string no índice i"},
    {"len", (PyCFunction)SortVector_len, METH_NOARGS, "Retorna o tamanho do vetor"},
    {"clear", (PyCFunction)SortVector_clear, METH_NOARGS, "Esvazia o vetor"},
    {"copy", (PyCFunction)SortVector_copy, METH_VARARGS, "Copia outro SortVector"},
    {"quick_sort", (PyCFunction)SortVector_QuickSort, METH_NOARGS, "Ordena usando QuickSort"},
    {"quick_sort_rand", (PyCFunction)SortVector_QuickSort_Random, METH_NOARGS, "Ordena usando QuickSort"},
    {"shell_sort", (PyCFunction)SortVector_ShellSort, METH_NOARGS, "Ordena usando ShellSort"},
    {"heap_sort", (PyCFunction)SortVector_HeapSort, METH_NOARGS, "Ordena usando HeapSort"},
    {"bubble_sort", (PyCFunction)SortVector_BubbleSort, METH_NOARGS, "Ordena usando BubbleSort"},
    {"selection_sort", (PyCFunction)SortVector_SelectionSort, METH_NOARGS, "Ordena usando SelectionSort"},
    {"insertion_sort", (PyCFunction)SortVector_InsertionSort, METH_NOARGS, "Ordena usando InsertionSort"},
    {"merge_sort", (PyCFunction)SortVector_MergeSort, METH_NOARGS, "Ordena usando MergeSort"},
    {"hibrid_merge_sort", (PyCFunction)SortVector_Hibrid_MergeSort, METH_NOARGS, "Ordena usando MergeSort hibrido com insertion"},
    {NULL, NULL, 0, NULL}

}; 

static PyTypeObject SortVectorType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "sortlib.SortVector",
    .tp_basicsize = sizeof(SortVectorObject),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor)SortVector_delete,
    .tp_doc = "",
    .tp_methods = SortVector_methods,
    .tp_init = (initproc)SortVector_init,
    .tp_new = PyType_GenericNew,
};

static PyModuleDef sort_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "sort_lib",
    .m_doc = "Módulo de ordenação em C++",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_sortlib(void) {
    PyObject* m = NULL;
    if (PyType_Ready(&SortVectorType) < 0) return NULL;
    m = PyModule_Create(&sort_module);
    if (!m) return NULL;

    Py_INCREF(&SortVectorType);
    if (PyModule_AddObject(m, "SortVector", (PyObject*)&SortVectorType) < 0) {
        Py_DECREF(&SortVectorType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
} 