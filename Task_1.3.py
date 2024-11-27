import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Установка максимального количества строк
pd.set_option('display.max_rows', 100)

# Установка максимального количества столбцов
pd.set_option('display.max_columns', 16)

# # Загрузка .csv файла
# data = pd.read_csv('data.csv')

# # Вывод содержимого в консоль
# print(data)

# data_proc = data

# # Проходим по всем столбцам загруженных данных
# # И удаляем столбцы, в которых нет уникальных элементов, кроме нуля

# for column_name in data.columns:
#     uniq = data[column_name].unique() # Количество уникальных элементов в столбце
#     if(len(uniq) == 1):
#         #print('Column:', column_name, end="  ")
#         #print(uniq)
#         data_proc = data_proc.drop(columns=[column_name])

# # print(data_proc)

# data_proc_2 = data_proc

# # Заполняю пропущенные значения в нужных столбцах

# data_proc_2[['Цена', 'Остаток', 'Количество', 'Транзит', 'НаСкладе']] = data_proc_2[['Цена', 'Остаток', 'Количество', 'Транзит', 'НаСкладе']].fillna(0.0)
# data_proc_2[['ДлинаЕд', 'ШиринаЕд', 'ВысотаЕд']] = data_proc_2[['ДлинаЕд', 'ШиринаЕд', 'ВысотаЕд']].fillna(0.000)

# # print(data_proc_2)

# # Удаляю строки, в столбцах которых я не смогу заполнить пропущенные данные
# data_proc_2 = data_proc_2.dropna()

# # print(data_proc_2)

# #
# # ---- 2я часть 1го задания:
# #

# # Переименовываем столбцы
# data_proc_2 = data_proc_2.rename(columns={'Остаток': 'ВсегоТовара'})
# data_proc_2 = data_proc_2.rename(columns={'Количество': 'НаВитрине'})

# # Группируем по коду категории
# data_gtoup = data_proc_2.groupby('КодКатегории').size()

# print()
# print(data_gtoup)

# # Группируем по коду категории, и добавляем столбец средней цены, для каждой группы
# average_price = data_proc_2.groupby('КодКатегории')['Цена'].mean().round(2)

# print()
# print(average_price)

# # Перемещаю полученный столбец средней цены по категориям, в исходную таблицу

# data_proc_3 = data_proc_2.merge(average_price, on='КодКатегории')

# # Переименовываю, для удобства
# data_proc_3 = data_proc_3.rename(columns={'Цена_x': 'Цена'})
# data_proc_3 = data_proc_3.rename(columns={'Цена_y': 'СредняяЦена'})

# # Я знаю, что наверняка существует встроенный метод разницы для 2х столбцов, но мне надоело просить gpt дать мне ответ, 
# # по этому я напишу это сам

# # data_proc_3 = data_proc_3.assign(new_column=[0]*len(data_proc_3)) 
# # Как оказалось, не обязательно явно указывать новый столбец, для его заполнения

# # Для каждой строки нахожу разницу между Ценой и Средней ценой, и вставляю значение в новый столбец

# for index, row in data_proc_3.iterrows():
#     data_proc_3.at[index, 'РазницаЦен'] = row['Цена'] - row['СредняяЦена']

# print()
# print(data_proc_3)

# # Сохраняю датафрейм в файл, для себя
# data_proc_3.to_csv('output_1.csv', index=False)
 
#
# ---- 3я часть 1го задания:
#

# print(data.iloc[1:3,1])

data = pd.read_csv('output_1.csv')

# Пронумеровать строки в рамках одной категории
data['НомерТовара'] = data.groupby('КодКатегории').cumcount() + 1

print(data)

# Посчитать площадь и объём товаров
data['Площадь'] = data['ДлинаЕд'] * data['ШиринаЕд']
data['Объем'] = data['Площадь'] * data['ВысотаЕд']

# Заполнить пропущенные значения средними в рамках категории
for column in ['ДлинаЕд', 'ШиринаЕд', 'ВысотаЕд']:
    data[column] = data.groupby('КодКатегории')[column].transform(lambda x: x.fillna(x.mean()))

# Отсортировать список по частоте продаж товаров
data = data.sort_values('ЧастотаПродаж', ascending=False)

# Исключить товары с частотой продаж меньше 0.012 и без остатков или транзита
data = data[(data['ЧастотаПродаж'] >= 0.012) & ((data['НаВитрине'] > 0) | (data['Транзит'] > 0))]

# Рассчитать сколько товаров по каждой категорий влезет по объему
# Загрузите данные о свободном объеме для каждой категории
volume_data = pd.read_excel('Volume.xlsx')
data = data.merge(volume_data, on='КодКатегории', how='left')
data['КоличествоТоваров'] = data['Свободный объем'] / data['Объем']

# Сохранить результат в файл Excel
with pd.ExcelWriter('output.xlsx') as writer:
    for category, group in data.groupby('КодКатегории'):
        group.to_excel(writer, sheet_name=category)

# Построить график
plt.figure(figsize=(10, 6))
plt.plot(data['НомерТовара'], data['Объем'].cumsum(), label='ЗанятыйОбъем')
plt.plot(data['НомерТовара'], data['Свободный объем'] - data['Объем'].cumsum(), label='Свободный объем')
plt.xlabel('НомерТовара')
plt.ylabel('Объем')
plt.legend()
plt.show()
