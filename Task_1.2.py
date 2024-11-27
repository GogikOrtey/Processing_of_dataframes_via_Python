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

# print(data_proc)

data_proc_2 = data_proc

# Заполняю пропущенные значения в нужных столбцах

data_proc_2[['Цена', 'Остаток', 'Количество', 'Транзит', 'НаСкладе']] = data_proc_2[['Цена', 'Остаток', 'Количество', 'Транзит', 'НаСкладе']].fillna(0.0)
data_proc_2[['ДлинаЕд', 'ШиринаЕд', 'ВысотаЕд']] = data_proc_2[['ДлинаЕд', 'ШиринаЕд', 'ВысотаЕд']].fillna(0.000)

# print(data_proc_2)

# Удаляю строки, в столбцах которых я не смогу заполнить пропущенные данные
data_proc_2 = data_proc_2.dropna()

# print(data_proc_2)

#
# ---- 2я часть 1го задания:
#

# Переименовываем столбцы
data_proc_2 = data_proc_2.rename(columns={'Остаток': 'ВсегоТовара'})
data_proc_2 = data_proc_2.rename(columns={'Количество': 'НаВитрине'})

# Группируем по коду категории
data_gtoup = data_proc_2.groupby('КодКатегории').size()

print()
print(data_gtoup)

# Группируем по коду категории, и добавляем столбец средней цены, для каждой группы
average_price = data_proc_2.groupby('КодКатегории')['Цена'].mean().round(2)

print()
print(average_price)

# Перемещаю полученный столбец средней цены по категориям, в исходную таблицу

data_proc_3 = data_proc_2.merge(average_price, on='КодКатегории')

# Переименовываю, для удобства
data_proc_3 = data_proc_3.rename(columns={'Цена_x': 'Цена'})
data_proc_3 = data_proc_3.rename(columns={'Цена_y': 'СредняяЦена'})

# Я знаю, что наверняка существует встроенный метод разницы для 2х столбцов, но мне надоело просить gpt дать мне ответ, 
# по этому я напишу это сам

# data_proc_3 = data_proc_3.assign(new_column=[0]*len(data_proc_3)) 
# Как оказалось, не обязательно явно указывать новый столбец, для его заполнения

# Для каждой строки нахожу разницу между Ценой и Средней ценой, и вставляю значение в новый столбец

for index, row in data_proc_3.iterrows():
    data_proc_3.at[index, 'РазницаЦен'] = row['Цена'] - row['СредняяЦена']

print()
print(data_proc_3)
