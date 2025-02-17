import aiogram
from aiogram import types, Bot
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
import botbot,json,string
from math import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup,State

storage= MemoryStorage()

bot = Bot(botbot.TOKEN)
st = Dispatcher(bot, storage = storage)

class Test(StatesGroup):
    X= State()
    Y = State()
""""приветствие"""

while True:
    try:

        @st.message_handler(commands=['start'])
        async def welcome(message):
            if message.from_user.last_name is not None:
                mess = f" {message.from_user.first_name} {message.from_user.last_name},этот бот будет много что уметь но пока можно решить статистику "
            else:
                mess = f" {message.from_user.first_name}, этот бот будет много что уметь но пока можно решить статистику "
            await message.reply(mess, reply_markup=types.ReplyKeyboardRemove())


        @st.message_handler(commands=['statistika'])
        async def statistika(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("1 если x")
            item2 = types.KeyboardButton("2 если x и y")

            markup.add(item1, item2)

            await bot.send_message(message.from_user.id, "на тебе", reply_markup=markup)

        #
        """Отправляет музыку"""


        @st.message_handler(commands=['audio'])
        async def get_user_text(message):
            audio = open("MGMT - Little Dark Age.mp3", "rb")
            await bot.send_audio(message.chat.id, audio)


        @st.message_handler(content_types=['text'])
        async def answer(message):
            if message.text == '1 если x':
                await Test.X.set()
                await bot.send_message(message.chat.id, 'Введите X через пробел')
            elif message.text == '2 если x и y':
                await bot.send_message(message.chat.id, 'Введите X через пробел')
                await Test.X.set()
                await bot.send_message(message.chat.id, 'Введите Y через пробел')
                await Test.Y.set()

            async def x_def(state=Test.X):
                X = [float(s) for s in message.text.split()]
                n = len(X)
                mess1 = f'{X}'
                AverageX, AverageListX, mess2 = get_average(X)
                VarX, mess3 = get_var(AverageListX, AverageX, n)
                mess4 = get_rasmax(n, VarX, X)
                mess5 = get_cao(AverageListX, VarX, n)
                mess = f'{mess1} \n {mess2} \n {mess3} \n {mess4} \n {mess5}'
                await bot.send_message(message.chat.id, mess, parse_mode="html")
                mess6 = get_g(AverageListX, n)
                await bot.send_message(message.from_user.id, mess6, parse_mode="html")
        #
        #
        # async def get_dop(message):
        #     global X
        #     X = [float(s) for s in message.text.split()]
        #     msg = bot.send_message(message.chat.id, 'Введите Y через пробел')
        #     bot.register_next_step_handler(msg, y_def)
        #
        #
        # async def y_def(message):
        #     global X, Y
        #     Y = [float(s) for s in message.text.split()]
        #     id = message.chat.id
        #     n = len(X)
        #     mess1 = f'{X} X'
        #     mess2 = f'{Y} Y'
        #     AverageX, AverageListX, mess3 = get_average(X)
        #     AverageY, AverageListY, mess4 = get_average(Y)
        #     pirson = get_pirson(AverageListX, AverageListY)
        #     fexner = get_fexner(AverageListX, AverageListY, n)
        #     spirman = get_spirman(X, Y, n)
        #     kembel = get_kembel(X, Y, n)
        #     mess = f'{mess1} \n {mess2} \n {mess3} \n {mess4} \n {pirson} пирсон \n {fexner} фехнер С Н\n{spirman}  спирман\n{kembel}кэмбэл'
        #     bot.send_message(id, mess)
        #
        #
            async def get_average(n):
                Average = sum(n) / len(n)
                AverageList = list(map(lambda i: (i - Average), n))
                mess = f"{Average} среднее \n {AverageList} X-Xсред"
                return Average, AverageList, mess


            """"Коэфф Вариации"""


            async def get_var(AverageListX, AverageX, n):
                X = AverageListX
                VarX = sqrt((sum(list(map(lambda x: (x ** 2), X)))) / n)
                mess = f'{VarX} корень среднее в евадрате делитть на n σ еще надо поделить на среднее \n {VarX / AverageX} коэффициент вариации до 33'
                return VarX, mess


            """"размах и диограмма"""


            async def get_rasmax(n, VarX, X):
                k = 1 + 3.32 * log(n, 10)
                maxX = max(X)
                minX = min(X)
                i = (maxX - minX) / ceil(k)
                Promeczutki = [minX + i * n for n in range(ceil(k))]
                mess = f'{maxX} max \n {minX} min \n {k} k \n {i} i \n {Promeczutki} промежутки \n {(maxX - minX) / VarX} размах'
                return mess


            """CAO"""


            async def get_cao(AverageListX, VarX, n):
                X = AverageListX
                CAO = sum(list(map(lambda x: abs(x), X))) / n
                mess = f'{CAO} CAO среднее в модуле делить на n \n {(CAO / VarX) - sqrt(2 / pi)} сравнение c 0.4 делить на пи ≤ {0.4 / sqrt(n)}'
                return mess

            async def get_g(AverageListX , n):
                g1 = (sqrt(n) * sum(list(map(lambda x: (x ** 3), AverageListX)))) / (
                            sqrt(sum(list(map(lambda x: (x ** 2), AverageListX)))) ** 3)
                g2 = n * sum(list(map(lambda x: (x ** 4), AverageListX))) / (
                            (sum(list(map(lambda x: (x ** 2), AverageListX)))) ** 2) - 3
                G1 = (sqrt(n * (n - 1))) / (n - 2) * g1
                G2 = (n - 1) / ((n - 2) * (n - 3)) * ((n + 1) * g2 + 6)
                S1 = sqrt((6 * n * (n - 1)) / ((n - 2) * (n + 1) * (n + 3)))
                S2 = sqrt((24 * n * ((n - 1) ** 2)) / ((n - 3)*(n - 2)*(n + 3)*(n + 5)))
                W = f'{abs(G1)} ≤ {3 * S1} \n {abs(G2)} ≤ {5 * S2}'
                mess = f"{g1} g1 \n{g2} g2 \n{G1} G1 \n{G2} G2 \n{S1} S1\n{S2} S2\n{W}"
                return mess



            """"Пирсон"""


            async def get_pirson(AverageListX, AverageListY):
                X = AverageListX
                Y = AverageListY
                pirson = (sum(list(map(lambda x, y: (x * y), X, Y)))) / sqrt(
                    (sum(list(map(lambda x: (x ** 2), X)))) * (sum(list(map(lambda x: (x ** 2), Y)))))
                print(pirson, "Пирсон")
                return pirson


            async def get_fexner(AverageListX, AverageListY, n):
                X = AverageListX
                Y = AverageListY
                C = 0
                H = 0
                for i in range(n):
                    if X[i] < 0 and Y[i] < 0:
                        C += 1
                    if X[i] > 0 and Y[i] > 0:
                        C += 1
                    else:
                        H += 1
                print(C, H, "C and H")
                print((C - H) / (C + H), "Фехнер")
                F = (C - H) / (C + H)
                return F


            async def get_spirman(X, Y, n):
                X3 = []
                Y3 = []
                X1 = X
                Y1 = Y
                X2 = sorted(X)
                Y2 = sorted(Y)
                for i in range(n):
                    for p in range(n):
                        if X1[i] == X2[p]:
                            X3.append(X2.index(X2[p]) + 1)
                        if Y1[i] == Y2[p]:
                            Y3.append(Y2.index(Y2[p]) + 1)
                print(X3, "Px", Y3, "Py")
                W = list(map(lambda x, y: (x - y), X3, Y3))
                print(W, "△")
                W2 = list(map(lambda x, y: (x - y) ** 2, X3, Y3))
                print(W2, "△^2")
                Spi = 1 - (6 * sum(W2) / (n ** 3 - n))
                print(Spi, "spirman")
                return Spi


            async def get_kembel(X, Y, n):
                X3 = []
                Y3 = []
                X1 = X
                Y1 = Y
                X2 = sorted(X)
                Y2 = sorted(Y)
                for i in range(n):
                    for p in range(n):
                        if X1[i] == X2[p]:
                            X3.append(float(X2.index(X2[p])) + 1)
                        if Y1[i] == Y2[p]:
                            Y3.append(float(Y2.index(Y2[p])) + 1)
                XY = X3 + Y3
                Ysup = [None] * n
                X3s = sorted(X3)
                for i in range(n):
                    for p in range(n):
                        if XY[i] == X3s[p]:
                            Ysup[p] = XY[i + n]

                """"P"""
                P = 0
                n1 = 0
                for i in range(n):
                    for p in range(n, n1 + 0, -1):
                        if Ysup[i] > Ysup[p - 1]:
                            P += 1
                    n1 += 1

                """"Q"""
                n1 = 0
                Q = 0
                for i in range(n):
                    for p in range(n, n1 + 0, -1):
                        if Ysup[i] < Ysup[p - 1]:
                            Q += 1
                    n1 += 1
                Kembel = ((2 * (P - Q)) / (n ** 2 - n))
                print(Kembel, "Kembel", Q, "Q", P, "P")
                return Kembel

        # bot.polling(none_stop=True)
        executor.start_polling(st,skip_updates= True)
    except:
        pass
