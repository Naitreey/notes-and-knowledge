#include <string.h>
//implementation of sorting algorithms
void insertion_sort_by_loop(int * arr, int n);
void insertion_sort_by_recursion(int * arr, int n);
void selection_sort(int * arr, int n);
void merge_sort_with_sentinel(int * arr, int n);
void merge_sort_without_sentinel(int * arr, int n);

//API
void sort(int * arr, int n, char * method) {
    if ( strcmp(method, "insertion_sort_by_loop")==0 ) {
        insertion_sort_by_loop(arr,n);
    }
    else if ( strcmp(method, "insertion_sort_by_recursion")==0 ) {
        insertion_sort_by_recursion(arr,n);
    }
    else if ( strcmp(method, "selection_sort")==0 ) {
        selection_sort(arr,n);
    }
    else if ( strcmp(method, "merge_sort_with_sentinel")==0 ) {
        merge_sort_with_sentinel(arr,n);
    }
    else if ( strcmp(method, "merge_sort_without_sentinel")==0 ) {
        merge_sort_without_sentinel(arr,n);
    }
}
