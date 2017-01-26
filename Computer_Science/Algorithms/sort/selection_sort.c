/* selection sort */
void selection_sort(int * arr, int n) {
    int min, pos, temp;
    for ( int i=0; i<n-1; i++ ) {
        min=arr[i];
        for ( int j=i+1; j<n; j++ ) {
            if ( arr[j]<min ) {
                min=arr[j];
                pos=j;
            }
        }
        temp=arr[i];
        arr[i]=arr[pos];
        arr[pos]=temp;
    }
}
