#include <stdio.h>
#include <stdlib.h>
#include "search.h"
#define SIZE 10

int main(int argc, char *argv[]) {
    if ( argc!=3 ) {
        exit(EXIT_FAILURE);
    }

    int arr[SIZE]={2,4,5,6,7,9,13,45,67,100};
    int target=atoi(argv[1]);
    char *method=argv[2];

    printf("%d\n", search(arr, SIZE, target, method));

    return 0;
}
