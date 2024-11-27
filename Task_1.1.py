import pandas as pd

# Установка максимального количества строк
pd.set_option('display.max_rows', 100)

# Установка максимального количества столбцов
pd.set_option('display.max_columns', 16)

# Загрузка .csv файла
data = pd.read_csv('data.csv')

# Вывод содержимого в консоль
#print(data)

data_proc = data

# Проходим по всем столбцам загруженных данных
# И удаляем столбцы, в которых нет уникальных элементов, кроме нуля

for column_name in data.columns:
    uniq = data[column_name].unique() # Количество уникальных элементов в столбце
    if(len(uniq) == 1):
        #print('Column:', column_name, end="  ")
        #print(uniq)
        data_proc = data_proc.drop(columns=[column_name])

print(data_proc)

data_proc_2 = data_proc

# Заполняю пропущенные значения в нужных столбцах

data_proc_2[['Цена', 'Остаток', 'Количество', 'Транзит', 'НаСкладе']] = data_proc_2[['Цена', 'Остаток', 'Количество', 'Транзит', 'НаСкладе']].fillna(0.0)
data_proc_2[['ДлинаЕд', 'ШиринаЕд', 'ВысотаЕд']] = data_proc_2[['ДлинаЕд', 'ШиринаЕд', 'ВысотаЕд']].fillna(0.000)

# print(data_proc_2)

# Удалаю строки, в столбцах которых я не смогу заполнить пропущенные данные
data_proc_2 = data_proc_2.dropna()

print(data_proc_2)