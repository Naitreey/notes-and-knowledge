/* merge sort */
#include <math.h>
#include <limits.h>

//local auxiliary function (file scope internal linkage)
static void merge_with_sentinel(int * subarr, int start, int middle, int end);
static void real_merge_sort(int * arr, int start, int end);

void merge_sort_with_sentinel(int * arr, int n) {
    real_merge_sort(arr, 0, n-1);
}

static void real_merge_sort(int * arr, int start, int end) {
    if ( start<end ) {
        int middle=(int)floor((start+end)/2);
        real_merge_sort(arr, start, middle);
        real_merge_sort(arr, middle+1, end);
        merge_with_sentinel(arr, start, middle, end);
    }
}

//merge operation using sentinel value --- elegant
static void merge_with_sentinel(int * arr, int start, int middle, int end) {
    int lenL=middle-start+2;
    int lenR=end-middle+1;

    //temp arrays
    int arrL[lenL];
    int arrR[lenR];

    //initialization
    for ( int i=start, j=0; i<=middle; i++, j++ ) {
        arrL[j]=arr[i];
    }
    for ( int i=middle+1, j=0; i<=end; i++, j++ ) {
        arrR[j]=arr[i];
    }
    arrL[lenL-1]=INT_MAX;
    arrR[lenR-1]=INT_MAX;

    //merge two arrays
    for ( int i=0, j=0, k=start; k<=end; k++ ) {
        if ( arrL[i]<=arrR[j] ) {
            arr[k]=arrL[i];
            i++;
        }
        else {
            arr[k]=arrR[j];
            j++;
        }
    }
}
