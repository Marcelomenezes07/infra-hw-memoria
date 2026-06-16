import cProfile
import pstats
import io

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def fatorial(n):
    if n <= 1:
        return 1
    return n * fatorial(n - 1)

def soma_array(arr):
    soma = 0
    for x in arr:
        soma += x
    return soma

def bubble_sort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def executar_fibonacci():
    print("\n[Fibonacci]")
    for i in range(30, 36):
        print(f"  fib({i}) = {fibonacci(i)}")

def executar_fatorial():
    print("\n[Fatorial]")
    for i in range(1, 16):
        print(f"  fat({i}) = {fatorial(i)}")

def executar_soma():
    arr = list(range(1, 10001))
    for _ in range(500):
        soma_array(arr)
    print(f"\n[Soma] soma = {soma_array(arr)}")

def executar_sort():
    arr = list(range(3000, 0, -1))
    resultado = bubble_sort(arr)
    print(f"\n[Sort] {resultado[0]}..{resultado[-1]}")

def main():
    print("=== Task_0x003 - Python ===")
    executar_fibonacci()
    executar_fatorial()
    executar_soma()
    executar_sort()
    print("\nConcluido!")

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    profiler.dump_stats("profile.prof")
    s = io.StringIO()
    pstats.Stats(profiler, stream=s).sort_stats("cumulative").print_stats(10)
    print(s.getvalue())
    print("profile.prof gerado! Execute: snakeviz profile.prof")
