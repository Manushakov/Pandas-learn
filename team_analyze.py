import pandas as pd

frame = pd.read_csv("nbaStats.csv")

b = int(input("Введите год: "))


def get_teams(year):
    players_dict = {}
    team_list = pd.unique(frame[frame['SeasonStart'] == year]['Tm']).tolist()  # находим список команд за необх год
    for team in team_list:  # Анализируем каждую команду, находим id игрока с наибольшим количеством очков
        result1 = frame.loc[(frame['SeasonStart'] == year) & (frame['Tm'] == team)]['PTS'].idxmax()
        c = frame.iloc[result1][["PlayerName", 'PTS']].tolist()
        players_dict[team] = c
    return players_dict if players_dict != {} else "Нет информации о данном годе"


print(get_teams(b))
