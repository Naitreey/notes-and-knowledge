/* binary search */
#include <math.h>
static int real_binary_search(int * arr, int start, int end, int target);

int binary_search(int * arr, int n, int target) {
    return real_binary_search(arr, 0, n-1, target);
}

static int real_binary_search(int * arr, int low, int high, int target) {
    if ( low>high ) {
        return -1;
    }
    int midpoint=(int)floor((low+high)/2);
    if ( target==arr[midpoint] ) {
        return midpoint;
    }
    else if ( target<arr[midpoint] ) {
        return real_binary_search(arr, low, midpoint-1, target);
    }
    else {
        return real_binary_search(arr, midpoint+1, high, target);
    }
}
