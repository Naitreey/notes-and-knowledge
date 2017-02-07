#include <stdio.h>
#include "sort.h"
#define SIZE 10
int main(int argc, char *argv[]) {
    int arr[SIZE]={5,3,7,5,3,6,8,2,1,9};
    if ( argc!=2 ) {
        return 1;
    }

    sort(arr, SIZE, argv[1]);
    for ( int i=0; i<SIZE; i++ ) {
        printf("%d ", arr[i]);
    }
    putchar('\n');

    return 0;
}
