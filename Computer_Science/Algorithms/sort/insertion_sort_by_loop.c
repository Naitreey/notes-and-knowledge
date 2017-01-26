/* insertion sort */
void insertion_sort_by_loop(int * arr, int n) {
    for ( int i=1; i<n; i++ ) {
        int key=arr[i];
        int j;
        for ( j=i-1; j>=0 && arr[j]>key; j-- ) {
            arr[j+1]=arr[j];
        }
        arr[j+1]=key;
    }
}
