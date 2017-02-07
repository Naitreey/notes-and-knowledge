#include <string.h>
int binary_search(int * arr, int n, int target);

//search API
int search(int * arr, int n, int target, char * method) {
    if ( strcmp(method, "binary_search")==0 ) {
        return binary_search(arr, n, target);
    }
    else {
        return 0;
    }
}
