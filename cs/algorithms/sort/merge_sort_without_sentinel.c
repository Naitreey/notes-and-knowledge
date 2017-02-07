/* merge sort */
#include <math.h>
#include <limits.h>

//local auxiliary function (file scope internal linkage)
static void merge_without_sentinel(int * arr, int start, int middle, int end);
static void real_merge_sort(int * arr, int start, int end);

void merge_sort_without_sentinel(int * arr, int n) {
    real_merge_sort(arr, 0, n-1);
}

static void real_merge_sort(int * arr, int start, int end) {
    if ( start<end ) {
        int middle=(int)floor((start+end)/2);
        real_merge_sort(arr, start, middle);
        real_merge_sort(arr, middle+1, end);
        merge_without_sentinel(arr, start, middle, end);
    }
}

//merge operation not using sentinel value --- less elegant, same running time
static void merge_without_sentinel(int * arr, int start, int middle, int end) {
    int lenL=middle-start+1;
    int lenR=end-middle;

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

    //merge two arrays
    for ( int i=0, j=0, k=start; k<=end; k++ ) {
        if ( i==lenL ) {
            arr[k]=arrR[j];
            j++;
        }
        else if ( j==lenR ) {
            arr[k]=arrL[i];
            i++;
        }
        else if ( arrL[i]<=arrR[j] ) {
            arr[k]=arrL[i];
            i++;
        }
        else {
            arr[k]=arrR[j];
            j++;
        }
    }
}
