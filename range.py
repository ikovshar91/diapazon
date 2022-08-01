import pandas as pd
import os
import time
from tqdm import tqdm

start_time = time.time()

homedir = os.path.expanduser('~')

print('Выполнение программы началось...')

data = []
masks = []
masks2 = []

def ranges(first: str, last: str):
    assert (len(first) == len(last))
    assert (int(first) <= int(last))

    if first == last:
        return [first]
    if first == "0" * len(first) and last == "9" * len(last):
        return ["*"]
    if first[0] == last[0]:
        return [first[0] + v for v in ranges(first[1:], last[1:])]

    assert (int(first[0]) < int(last[0]))
    return ranges(first, first[0] + "9" * (len(first) - 1)) \
           + ranges(str(int(first[0]) + 1) + "0" * (len(first) - 1), last)


for i in tqdm(range(1), desc='Загрузка файла'):
    kody = pd.read_excel(homedir + '\\Desktop\\range\\kody.xlsx', index_col=False)
    kody.insert(0, 'range2', '7' + kody["АВС/ DEF"].astype(str) + kody['До'].astype(str))
    kody.insert(0, 'range1', '7' + kody['АВС/ DEF'].astype(str) + kody['От'].astype(str))


##################### 1 вариант решения ########################################################

# def poisk(kody):
#     for i, row in kody.iterrows():
#         abc = row['АВС/ DEF']
#         ot = row['От']
#         do = row['До']
#         emk = row['Емкость']
#         operator = row['Оператор']
#         region = row['Регион']
#         inn = row['ИНН']
#         start = int(row['range1'])
#         end = int(row['range2'])
#         masks = []
#
#         def end_zeros(num: int) -> int:
#             return len(str(num)) - len(str(num).rstrip('0'))
#
#         all_range = set(range(start, end + 1))
#
#         num_zeros = []
#         for n in all_range:  # pairs (num, tail_zeros)
#             z = end_zeros(n)
#             if z:
#                 num_zeros.append((n, z))
#
#         num_zeros.sort(key=lambda x: (-x[1], x[0]))  # tail_zeros ASC, num DESC
#
#         for num, _zeros in num_zeros:
#             for zeros in reversed(range(1, _zeros + 1)):  # decr tail zeros
#                 tmp_range = set(range(num, num + 10 ** zeros))
#                 if tmp_range.issubset(all_range):  # if range(num, num+10**zeros) in all_range
#                     all_range -= tmp_range  # substract from all_range
#                     masks.append(str(num)[:-zeros] + '*')  # adding mask to list of masks
#
#         for n in all_range:  # no mathcing masks
#             masks.append(str(n))
#
#         data.append([start, end, abc, ot, do, emk, operator, region,inn, str(sorted(masks))])


###################################################################################################
################## 2 вариант решения ##############################################################

def poisk2(kody):
    for i, row in kody.iterrows():
        abc = row['АВС/ DEF']
        ot = row['От']
        do = row['До']
        emk = row['Емкость']
        operator = row['Оператор']
        region = row['Регион']
        inn = row['ИНН']

        start = str(row['range1'])
        end = str(row['range2'])

        if len(start) != 11:
            if len(start) == 5: start = '7' + str(abc) + "000000" + str(row['От'])
            if len(start) == 6: start = '7' + str(abc) + "00000" + str(row['От'])
            if len(start) == 7: start = '7' + str(abc) + "0000" + str(row['От'])
            if len(start) == 8: start = '7' + str(abc) + "000" + str(row['От'])
            if len(start) == 9: start = '7' + str(abc) + "00" + str(row['От'])
            if len(start) == 10: start = '7' + str(abc) + "0" + str(row['От'])

        if len(end) != 11:
            if len(end) == 5: end = '7' + str(abc) + "000000" + str(row['До'])
            if len(end) == 6: end = '7' + str(abc) + "00000" + str(row['До'])
            if len(end) == 7: end = '7' + str(abc) + "0000" + str(row['До'])
            if len(end) == 8: end = '7' + str(abc) + "000" + str(row['До'])
            if len(end) == 9: end = '7' + str(abc) + "00" + str(row['До'])
            if len(end) == 10: end = '7' + str(abc) + "0" + str(row['До'])

        range_ = ranges(str(start), str(end))
        for i in range(len(range_)):
            if not range_[i].__contains__("*"):
                masks2.append(range_[i])
            else:
                masks.append(range_[i])

        data.append([start, end, abc, ot, do, emk, operator, region, inn, range_])


###################################################################################################

for i in tqdm(range(1), desc='Поиск диапазонов'):
    poisk2(kody)

kody2 = pd.DataFrame(data)
range2 = ranges(masks2[0],masks2[len(masks2) - 1])

for i in range(len(range2)):
    masks.append(range2[i])

kody3 = pd.DataFrame(sorted(list(set(masks))), columns=['ranges'])

kody2.rename(
    columns={0: 'rangeA', 1: 'rangeB', 2: 'АВС/ DEF', 3: 'От', 4: 'До', 5: 'Емкость', 6: 'Оператор', 7: 'Регион',
             8: 'ИНН', 9: 'Диапазон'}, inplace=True)

for i in tqdm(range(2), desc='Загрузка в файл:'):
    kody2.to_excel(homedir + '\\Desktop\\range\\kodyItog.xlsx', sheet_name='itog', index=False)
    kody3.to_excel(homedir + '\\Desktop\\range\\kodyItog2.xlsx', sheet_name='itog', index=False)

print('Успешно выполнено')

stop_time = str(time.time() - start_time)

print(f'Программа выполнилась за {stop_time[0:6]} секунд')

input('Нажмите Enter для завершения программы...\n')
