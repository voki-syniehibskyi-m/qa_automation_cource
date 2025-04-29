import random
from collections import Counter

# Сколько случайных чисел сгенерировать
amount_of_nums = 1000

# выставляем от какого и до какого числа будем создавать случайные числа.
min_value = 1
max_value = 10

# Создаём список и заполняем его "случайным" числами.
random_numbers = [random.randint(min_value, max_value) for _ in range(amount_of_nums)]

# Считаем распределение.
counter = Counter(random_numbers)

# Выводим распределение
print("Распределение случайных чисел:")
for number, count in sorted(counter.items()):
    print(f"Число {number}: {count} раз")