import time
import sys
import math


sys.setrecursionlimit(3000)

class Timer:
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.elapsed_time = self.end_time - self.start_time
        print(f'Time elapsed {self.elapsed_time:.9f} sec')
        return False

def cache(func):
    cache_dict = {}
    def wrapper(n):
        if n in cache_dict:
            return cache_dict[n]
        result = func(n)
        cache_dict[n] = result
        return result
    wrapper.cache_dict = cache_dict  # Доступ к кэшу снаружи
    return wrapper

def factorial(n):
    if n < 0:
        raise ValueError("Факториал не определён для отрицательных чисел")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

@cache
def cached_factorial(n):
    if n < 0:
        raise ValueError("Факториал не определён для отрицательных чисел")
    if n == 0 or n == 1:
        return 1
    return n * cached_factorial(n - 1)

def factorial_generator(max_n):
    """Генератор для вычисления факториалов от 0 до max_n."""
    if max_n < 0:
        raise ValueError("Максимальное число не может быть отрицательным")
    result = 1
    yield 0, 1  # Факториал 0 = 1
    for n in range(1, max_n + 1):
        result *= n
        yield n, result

def init_factorial_cache(max_n):
    """Инициализация кэша факториалов с помощью генератора."""
    for n, fact in factorial_generator(max_n):
        cached_factorial.cache_dict[n] = fact


if __name__ == "__main__":
    init_factorial_cache(100)
    # factorial_generator(100)

    with Timer():
        print('Cached factorial')
        cached_factorial(100)

    with Timer():
        print('Math factorial')
        math.factorial(100)

    with Timer():
        print('recursion factorial')
        factorial(100)


