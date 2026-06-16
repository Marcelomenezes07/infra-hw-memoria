#include <stdio.h>
#include <stdlib.h>

long fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

long fatorial(int n) {
    if (n <= 1) return 1;
    return n * fatorial(n - 1);
}

long soma_array(int *arr, int tamanho) {
    long soma = 0;
    for (int i = 0; i < tamanho; i++) soma += arr[i];
    return soma;
}

void bubble_sort(int *arr, int tamanho) {
    for (int i = 0; i < tamanho - 1; i++)
        for (int j = 0; j < tamanho - i - 1; j++)
            if (arr[j] > arr[j+1]) { int t=arr[j]; arr[j]=arr[j+1]; arr[j+1]=t; }
}

int main() {
    printf("=== Task_0x003 - C ===\n");
    for (int i = 30; i <= 35; i++)
        printf("fib(%d) = %ld\n", i, fibonacci(i));
    for (int i = 1; i <= 15; i++)
        printf("fat(%d) = %ld\n", i, fatorial(i));
    int tam = 10000;
    int *arr = malloc(tam * sizeof(int));
    for (int i = 0; i < tam; i++) arr[i] = i+1;
    for (int r = 0; r < 500; r++) soma_array(arr, tam);
    printf("soma = %ld\n", soma_array(arr, tam));
    int s = 3000;
    int *arr2 = malloc(s * sizeof(int));
    for (int i = 0; i < s; i++) arr2[i] = s - i;
    bubble_sort(arr2, s);
    printf("sort: %d..%d\n", arr2[0], arr2[s-1]);
    free(arr); free(arr2);
    return 0;
}
