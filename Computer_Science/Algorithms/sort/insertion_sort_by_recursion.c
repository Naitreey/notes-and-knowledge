/* insertion sort */
static void insert(int * arr, int n);
void insertion_sort_by_recursion(int * arr, int n) {
    if ( n>1 ) {
        insertion_sort_by_recursion(arr, n-1);
        insert(arr,n);
    }
}

static void insert(int * arr, int n) {
    int key=arr[n-1];
    int i;
    for ( i=n-2; i>=0 && arr[i]>key; i-- ) {
        arr[i+1]=arr[i];
    }
    arr[i+1]=key;
}
