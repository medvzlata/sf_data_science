"""Игра «Угадай число»
Компьютер сам загадывает и сам угадывает число
"""

import numpy as np

def random_predict(number:int=1) -> int:
    """ Рандомно угадываем число

    Args:
        number (int, optional): Загаданное число. Defaults to 1.

    Returns:
        int: Число попыток
    """
    count = 0 # счетчик попыток
    min_n = 0 # нижний предел диапозона предполагаемых чисел
    max_n = 101 # верхний предел диапозона предполагаемых чисел
        
    while True:
        count += 1
        predict_number = np.random.randint(min_n, max_n) # предполагаемое число
        if predict_number < number:
            min_n = predict_number # если предполагаемое число меньше загаданного, меняем нижнюю границу диапозона
        elif predict_number > number:
            max_n = predict_number # если предполагаемое число больше загаданного, меняем верхнюю границу диапозона
        elif number == predict_number:
            break # выход из цикла, если угадали        
    return(count)

def score_game(random_predict) -> int:
    """За какое количество попыток в среднем из 1000 подходов угадывает наш алгоритм

    Args:
        random_predict (_type_): функция угадывания

    Returns:
        int: среднее количество попыток
    """
    count_ls = [] # список для сохранения количества попыток
    np.random.seed(1) # фиксируем сид для воспроизводимости
    random_array = np.random.randint(1, 101, size=(1000)) # загадали список чисел
    
    for number in random_array:
        count_ls.append(random_predict(number))
        
    score = int(np.mean(count_ls)) # находим среднее количество попыток
    
    print(f'Ваш алгоритм угадывает число в среднем за: {score} попыток')
    return(score)

#RUN    

if __name__ == '__main__':
    score_game(random_predict)

#print(f'Количество попыток: {random_predict(10)}')
        