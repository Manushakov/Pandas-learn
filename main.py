import pandas as pd
import numpy as np
from functools import reduce

filename = "nbaStats.csv"
frame = pd.read_csv(filename)
del frame['#']  # удаление столбца #
frame['PlayerSalary '] = frame['PlayerSalary '].replace({'\$': '', ' ': '', ',': '', 'z': ''},
                                                        regex=True)  # удаление знака $
mean_value = []  # список столбцов с элементами для среднего значения
sum_value = []   # список столбцов с элементами для суммирования

# Функция анализирует типы данных во всех столбцах и список со значениями
columns_dict = list(frame)  # список с колонками из таблицами
for column in columns_dict:  # распределение атрибутов по спискам для дальнейшего преобразования
    if type(frame[column][3571]) == str and frame[column][3571][-1] == '%':  # Преобразует процентные величины к дробным
        frame[column] = frame[column].str.rstrip('%').astype('float') / 100.0
        mean_value.append(column)
    elif type(frame[column][3571]) == np.float64 and -1 <= frame[column][3571] <= 1:  # находит дробные столбцы
        mean_value.append(column)
    elif type(frame[column][3571]) == np.int64 or type(frame[column][3571]) == np.float64:  # находит столбцы для суммы
        sum_value.append(column)

#  удаляем значения 'SeasonStart' и 'Age' т.к они являются частными случаями
sum_value.remove('SeasonStart')
sum_value.remove('Age')


# Функция создания нового фрейма
def new_frame(player):
    def period(gr):  # функция для временных промежутков
        max_value = gr.max()
        min_value = gr.min()
        return f"{min_value} - {max_value}"

    def stra(x):  # Функция для удобной конкатенации команд и позиций
        return ';'.join(str(y) for y in set(x))

    def salary(x):  # Функция для удобной преобразования PlayerSalary
        return x.astype('float').sum().astype('int64')

    # создание отдельных таблиц для разных списков атрибутов
    df1 = player.groupby("PlayerName", as_index=False)[mean_value].mean()
    df2 = player.groupby("PlayerName", as_index=False).agg({'Tm': stra, 'Pos': stra})
    df3 = player.groupby("PlayerName", as_index=False)[sum_value].sum()
    df4 = player.groupby("PlayerName", as_index=False).agg(
        {'PlayerSalary ': salary, 'Age': period, 'SeasonStart': period})
    dfs = [df4, df2, df3, df1]
    result = reduce(lambda left, right: pd.merge(left, right, on='PlayerName'),
                    dfs)  # Объединение всех созданных ранее таблиц
    # с помощью общего столбца 'PlayerName'
    result = result.round(decimals=2)  # кол-во цифр после запятой
    result = result[columns_dict]  # Сортировка колонок таблицы как в первоначальной
    pd.DataFrame(result).to_csv('nbaNewStats.csv', index=False)
    return result


if __name__ == "__main__":
    new_frame(frame)
