import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import constants
import json


with open("velocity.json", "r", encoding="UTF-8") as file:
    records = json.load(file)

sec = []
speed = []
i = 0
for count in range(0, len(records), len(records) // 475):
    if count >= 350:
        i += 1.105
        speed.append(records[count])
        sec.append(i)
        if i >= 475:
            break
    else:
        i += 1
        speed.append(records[count])
        sec.append(i)


# Функция для проверки на то, осталось ли топливо в первой ступени. Если есть, то возвращает 1, иначе - 0
def f1(t):
    global t1
    return t1 - t > 0

# Функция для проверки на то, осталось ли топливо во второй ступени. Если есть, то возвращает 1, иначе - 0
def f2(t):
    global t1
    global t2

    return (t1 + t2 - t > 0) and (t1 - t <= 0)

# Функция для проверки на то, осталось ли топливо в третьей ступени. Если есть, то возвращает 1, иначе - 0
def f3(t):
    global t1
    global t2
    global t3

    return (t1 + t2 - t <= 0) and (t3 + t2 + t1 - t > 0)


temp = 90

# Функция для вычисления угла, связанным с косинусом, в математической модели
def alpha(t):
    global temp
    temp += 0.1

    return (temp * (math.pi / 180)) # Перевод значений угла в градусы


temp_1 = 360

# Функция для вычисления угла, связанным с синусом, в математической модели
def beta(t):
    global temp_1
    temp_1 += 0.05 # Изменение

    return (temp_1 * (math.pi / 180)) # Перевод значений угла в градусы


u = 0 # Скорость ракеты
t1 = 131  # Время, за которое уйдет все топливо из первой ступени
t2 = 220  # Время, за которое уйдет все топливо из второй ступени
t3 = 99  # Время, за которое уйдет все топливо из третьей ступени
g = constants.g  # Ускорение свободного падения
m1 = 216000  # Масса топлива первой ступени
m2 = 160000  # Масса топлива второй ступени
m3 = 40000  # Масса топлива третьей ступени
M0 = 31200  # Масса полезной нагрузки

I1 = 26  # Удельный импульс 1
I2 = 9  # Удельный импульс 2
I3 = 17  # Удельный импульс 3

M21 = 948000  # Масса первой ступени без топлива
M22 = 220000  # Масса второй ступени без топлива
M23 = 137000  # Масса третьей ступени без топлива

Ni1 = m1 / t1  # Ню1
Ni2 = m2 / t2  # Ню2
Ni3 = m3 / t3  # Ню3
t0 = 0 # Время
speed_values = [] # Массив скоростей
time = [] # Массив по пройденному времени
last_speed = 0
for _ in range(sum([t1,t2,t3 + 25])): # Идем от 0 секунды до суммы времени, за которое уйдет все топливо из ступеней
    t = 1 # Константа
    t0 += 1 # Увеличивается время на 1 с каждым проходом
    # Расчет скорости
    u += (f1(t0) * I1 *
          math.log((M0 + M21 + m1 - (Ni1 * t * f1(t0)) + M22 + m2 - Ni2 * t * f3(t0) + M23 + m3 - Ni3 * t * f3(t0)) /
                   (M0 + M21 + M22 + m2 - Ni2 * t * f2(t0) + M23 + m3 - Ni3 * t * f3(t0))) + f2(t0) * I2 *
          math.log((M0 + M22 + m2 - (Ni2 * (t - t2) * f2(t0)) + M23 + m3 - Ni3 * (t - t2) * f3(t0))
                   / (M0 + M22 + M23 + m3 - Ni3 * t * f3(t0))) + f3(t0) * I3 *
          math.log((M0 + M23 + m3 - Ni3 * (t - t3 - t2) * f3(t0))
                   / (M0 + M23))) - ((f1(t0) * I1 * Ni2 * g * (1 - math.cos(alpha(t)))) /
      (M0 + M21 + m1 - Ni1 * t * f1(t0) + M22 + m2 - Ni2 * t * f3(
          t0) + M23 + m3 - Ni3 * t * f3(t0))) - (
     (f2(t0) * I2 * Ni2 * g * (1 - math.cos(alpha(t)))) /
     (M0 + M22 + m2 - Ni2 * t * f2(t0) + M23 + m3 - Ni3 * t * f3(t0))) - (
     (f3(t0) * I3 * Ni3 * g * (1 - math.cos(alpha(t)))) /
     (M0 + M23 + m3 - Ni3 * t * f3(t0))) - g * math.sin(beta(t))

    # Запись последней скорости, если мы вышли за время, когда закончилось все топливо
    if t0 >= sum([t1,t2,t3]) and last_speed == 0:
        last_speed = u
    if last_speed != 0:
        u = last_speed

    speed_values.append(u) # Добавление текущей скорости
    time.append(t0) # Добавление текущего времени

x = np.array(time) # Многомерный массив по значениям х для построения графика
y = np.array(speed_values) # Многомерный массив по значениям y для построения графика
x1 = np.array(sec)
y1 = np.array(speed)


plt.title('График скорости ракеты от времени\n', fontsize=12, fontweight="bold") # Титульник на графике
plt.ylabel("Скорость V(t)", fontsize=14) # Описание функции y на графике
plt.xlabel("Время t", fontsize=14) # Описание функции x на графике
plt.plot(x, y, 'r', label = "график мат.модели") # r, g - red, green colour
plt.plot(x1, y1, 'g', linestyle='--', label = "график KSP") # r, g - red, green colour
plt.legend()
plt.show() # Вывод графика
