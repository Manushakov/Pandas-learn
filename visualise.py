import pandas as pd
import matplotlib.pyplot as plt

frame = pd.read_csv("nbaStats.csv")

b = input("Введите название команды ")
c = int(input("Введите год "))
players = frame["Tm"].unique()
years = frame["SeasonStart"].unique()


def get_players(team_name, year):
    team_name = team_name.upper()  # исключает синтаксическую ошибку
    result = frame.loc[(frame['Tm'] == team_name) & (frame['SeasonStart'] == year)]
    players_list = list(result["PlayerName"])
    result1 = result[["PlayerName", "PTS"]]
    result1.plot(  # задается построение гистограммы
        x='PlayerName',
        y='PTS',
        kind='barh',
        figsize=(18, 8),
        title='Статистика игроков')  # Задаем что будет на осях гистрограммы , а также размер и тип графика.
    plt.xlabel('Кол-во набранных очков', fontsize=12, color='red')  # надпись под осью Х
    plt.ylabel('Игроки', fontsize=12, color='red')  # надпись слева от оси Y
    plt.show()  #
    return players_list


if b.upper() not in players:
    print("Данная команда не найдена")
if c not in years:
    print("Нет информации по данному сезону")
else:
    print(get_players(b, c))
