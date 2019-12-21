#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType

from datetime import datetime, timedelta
import json

import requests
import re
from bs4 import BeautifulSoup

def k2(now_tp, now_plus_1_tp, now_plus_2_tp, now_plus_3_tp, now_plus_4_tp, back = 'Назад'):
    '''Честно, я не нашла, как передать переменные в мой почти готовый json, который только получал бы даты для кнопочек,
       поэтому я сделала так'''
    k_2 = {"one_time": False,
        "buttons": [
            [{
                "action": {
                  "type": "text",
                  "label": now_tp
                },
                "color": "primary"
            },
            {
                  "action": {
                    "type": "text",
                    "label": now_plus_1_tp
                 },
                 "color": "primary"
             }],
             [{
                  "action": {
                    "type": "text",
                    "label": now_plus_2_tp
                 },
                 "color": "primary"
             },
             {
                  "action": {
                    "type": "text",
                    "label": now_plus_3_tp
                 },
                 "color": "primary"
             }],
             [{
               "action": {
                 "type": "text",
                 "label": now_plus_4_tp
                 },
                 "color": "primary"
             },
             {
               "action": {
                 "type": "text",
                 "label": back
                 },
                 "color": "secondary"
             }]
      ]
    }
    return k_2

def parsing(now_tp, now_plus_1_tp, now_plus_2_tp, now_plus_3_tp, now_plus_4_tp, movie_name, day):
    link = 'https://kinoteatr.ru/raspisanie-kinoteatrov/'
    r = requests.get(link)
    if r.status_code == 200: 
        soup = BeautifulSoup(r.text, "html.parser") 
    else:
        print("Страница не найдена")
    cinema = {}       #словарь, где будет: ключ - название кинотеатра в сети, значение - информация о нём
    name = soup.findAll('div', 'cinema_card_wrap_description')
    for i, e in enumerate(name):
        x = re.sub('\n', '', name[i].findAll('h3', 'title movie_card_title')[0].text)
        x = re.sub('  ', '', x)
        x = x.replace('\t', '')
        cinema[x] = []
    addr = []
    for i, e in enumerate(name):
        a = ''
        add = re.sub('\n', '', name[i].findAll('span', 'sub_title')[1].text)
        add = 'м. ' + re.sub('  ', '', add)
        for b in range(len(add) - 1):  #у нас когда несколько станций метро, они слеплены, тут я делаю, чтобы они как бы отдельно
            if (add[b].islower()) and (add[b+1].isupper()):
                add = add.replace(add[b] + add[b+1], add[b] + ', м. ' + add[b+1])
        add1 = re.sub('\n', '', name[i].findAll('span', 'sub_title')[0].text)
        add1 = re.sub('  ', '', add1)
        a = add + ', ' + add1
        addr.append(a)
    for i,e in enumerate(cinema.keys()):
        a = cinema[e]
        a.append(addr[i])
    links = []
    for i, e in enumerate(name):
        a = name[i].select('div.cinema_card_wrap_description a')
        for t in a:
            links.append(t.attrs['href'])  
    linksss = []
    #сюда я записываю только искомую дату, потому что иначе это всё выполняется ещё дольше
    for l in links:
        #в общем, мне нужен цикл, чтобы он проходил по 5 датам в каждом кинотеатре, брал там расписание и всё такое
        if day == now_tp:
            linksss.append(l)     #когда расписание на сегодня, ссылка совпадает с этой ссылкой
        elif day == now_plus_1_tp:
            linksss.append(l + '?day=tomorrow')  #на завтра
        elif day == now_plus_2_tp: 
            now_plus_2_t_app = now_plus_2.strftime("%Y-%m-%d")
            linksss.append(l + '?date=' + now_plus_2_t_app)   #на 2 дня вперёд
        elif day == now_plus_3_tp:
            now_plus_3_t_app = now_plus_3.strftime("%Y-%m-%d")
            linksss.append(l + '?date=' + now_plus_3_t_app)   #на 3 дня вперёд
        elif day == now_plus_4_tp:
            now_plus_4_t_app = now_plus_4.strftime("%Y-%m-%d")
            linksss.append(l + '?date=' + now_plus_4_t_app)   #на 4 дня вперёд
    #а теперь, надеюсь, достаточно сделать один код "вытягивания" всего необходимого для кааааждой ссылки 
    filmsss = []
    for lin in linksss:
        r = requests.get(lin)
        if r.status_code == 200: 
            soup = BeautifulSoup(r.text, "html.parser")   
        else:
            print("Страница не найдена")
        films = {}       #словарь, где будет: ключ - название фильма в кинотеартре, значение - информация об этом фильме
        film = soup.findAll('div', 'shedule_movie bordered gtm_movie')  
        for i, e in enumerate(film):
            x = re.sub('\n', '', film[i].findAll('span', 'movie_card_header title')[0].text)
            x = re.sub('  ', '', x)
            x = x.replace('\t', '')
            films[x] = []
        g = []   #жанр
        for i, e in enumerate(film):
            x = re.sub('\n', '', film[i].findAll('span', 'movie_card_raiting sub_title')[0].text)
            x = re.sub('  ', '', x)
            x = x.replace('\t\t', '')
            x1 = ''
            if x != '':  #ну тут я что могу сделать, если кто-то решил показать в кинотеатре трансляцию какой-то игрульки без жанра 
                if x[2].isalpha():          #а это из-за возрастного ограничения, которое разной длины бывает
                    for buk in range(2, len(x)):
                        x1 += x[buk]
                else:
                    for buk in range(3, len(x)):
                        x1 += x[buk]
            g.append(x1)
        lasts = []   #длительность
        for i, e in enumerate(film):
            x = re.sub('\n', '', film[i].findAll('span', 'title')[1].text)
            x = re.sub('  ', '', x)
            x = x.replace('\t\t', '')
            lasts.append(x)
        for i, e in enumerate(films.keys()):
            a = films[e]
            a.append(g[i])
        for i, e in enumerate(films.keys()):
            a = films[e]
            a.append(lasts[i])
        time_and_price = []
        for i, e in enumerate(film):
            full_inf = re.sub('\n', '', film[i].findAll('div', 'shedule_movie_sessions col col-md-8')[0].text)
            full_inf = re.sub('   ', '', full_inf)
            full_inf = full_inf.replace('\t', '')
            #а тут просто привожу в красивый и удобный для пользователя вид
            full_inf = full_inf.replace('  ', ' ')
            full_inf = full_inf.replace('Стандарт ', 'Стандарт; ')
            full_inf = full_inf.replace('4DX 4DX', '4DX')
            full_inf = full_inf.replace('DIMAX IMAX', 'D IMAX')
            full_inf = full_inf.replace('Премиум ', 'Премиум; ')
            full_inf = full_inf.replace('4DX ', '4DX; ')
            full_inf = full_inf.replace('Dolby Atmos ', 'Dolby Atmos; ')
            full_inf = full_inf.replace('Мувик ', 'Мувик; ')
            full_inf = full_inf.replace('IMAX ', 'IMAX; ')
            full_inf = full_inf.replace('Prime ', 'Prime; ')
            full_inf = full_inf.replace(' р.', '₽')
            time_and_price.append(full_inf)
        for i, e in enumerate(films.keys()):
            a = films[e]
            a.append(time_and_price[i])
        filmsss.append(films)
    for i, e in enumerate(cinema.keys()):
        a = cinema[e]
        a.append(filmsss[i])
    link2 = 'https://kinomax.ru/finder'
    r = requests.get(link2)
    if r.status_code == 200: 
        soup = BeautifulSoup(r.text, "html.parser") 
    else:
        print("Страница не найдена")
    cinema_k = {}       #аналогично тут, в принципе
    name = soup.findAll('div', 'pt-3 pb-3')
    for i, e in enumerate(name):
        x = re.sub('\n', '', name[i].findAll('div', 'd-flex flex-column fs-11 text-primary')[0].text)
        x = re.sub('  ', '', x)
        x = re.sub('\xa0', '', x)
        x = x.replace('\t', '')
        cinema_k[x] = []
    addr = []
    for i, e in enumerate(name):
        add = re.sub('\n', '', name[i].findAll('div', 'fs-08')[0].text)
        add = re.sub('\xa0', '', add)
        add = re.sub('\t', '', add)
        if '·' in add:
            add = 'м. ' + add
            add = add.replace('·', ', ')
        addr.append(add)
    for i,e in enumerate(cinema_k.keys()):
        a = cinema_k[e]
        a.append(addr[i])
    links = []
    for i, e in enumerate(name):
        a = name[i].select('div a')
        for t in a:
            links.append('https://kinomax.ru' + t.attrs['href']) 
    linksss = []
    for l in links:
        if day == now_tp:
            linksss.append(l)     
        elif day == now_plus_1_tp:
            now_plus_1_t_app = now_plus_1.strftime("%Y-%m-%d")
            linksss.append(l + '#' + now_plus_1_t_app)  
        elif day == now_plus_2_tp: 
            now_plus_2_t_app = now_plus_2.strftime("%Y-%m-%d")
            linksss.append(l + '#' + now_plus_2_t_app)   
        elif day == now_plus_3_tp:
            now_plus_3_t_app = now_plus_3.strftime("%Y-%m-%d")
            linksss.append(l + '#' + now_plus_3_t_app)   
        elif day == now_plus_4_tp:
            now_plus_4_t_app = now_plus_4.strftime("%Y-%m-%d")
            linksss.append(l + '#' + now_plus_4_t_app)  
    filmsss = []
    for lin in linksss:
        r = requests.get(lin)
        if r.status_code == 200: 
            soup = BeautifulSoup(r.text, "html.parser")   
        else:
            print("Страница не найдена")
        films = {}      #словарь, где будет так же: ключ - название фильма в кинотеартре, значение - информация об этом фильме
        film = soup.findAll('div', 'd-flex border-bottom-1 border-stack film')  
        for i, e in enumerate(film):
            x = re.sub('\n', '', film[i].findAll('div', 'w-70')[0].text)
            x = re.sub('  ', '', x)
            x = x.replace('\t', '')
            films[x] = []
        g = []      #жанр
        for i, e in enumerate(film):
            x = re.sub('\n', '', film[i].findAll('div', 'w-70')[1].text)
            x = re.sub('  ', '', x)
            x = x.replace('\t', '')
            x1 = ''
            for sym in x:
                if sym.isdigit():
                    end = x.find(sym)
                    break
            for j in range(end):
                x1 += x[j]
            g.append(x1)
        lasts = []   #длительность
        for i, e in enumerate(film):
            x = re.sub('\n', '', film[i].findAll('div', 'w-70')[1].text)
            x = re.sub('  ', '', x)
            x = x.replace('\t', '')
            x1 = ''
            for sym in x:
                if sym.isdigit():
                    start = x.find(sym)
                    break
            for j in range(start, len(x)):
                x1 += x[j]
            lasts.append(x1)
        for i, e in enumerate(films.keys()):
            a = films[e]
            a.append(g[i])
        for i, e in enumerate(films.keys()):
            a = films[e]
            a.append(lasts[i])
        time_and_price = []
        for i, e in enumerate(film):
            full_inf = re.sub('\n', '', film[i].findAll('div', 'd-flex w-80')[0].text)
            full_inf = re.sub('   ', '', full_inf)
            full_inf = full_inf.replace('\t', '')
            full_inf = full_inf.replace('  ', ' ')
            full_inf = full_inf.replace('2D', '2D: ')
            full_inf = full_inf.replace('3D', '3D: ')
            full_inf = full_inf.replace('4D', '4D: ')
            full_inf = full_inf.replace('₽', '₽, ')
            full_inf = full_inf.replace('Детский зал', 'Детский зал: ')
            full_inf = full_inf.replace(', Комфорт', ', Комфорт: ')
            for b in range(len(full_inf) - 1):
                if (full_inf[b].isdigit()) and (full_inf[b+1].islower()):
                    full_inf = full_inf.replace(full_inf[b] + full_inf[b+1], full_inf[b] + ' ' + full_inf[b+1])
            for b in range(len(full_inf) - 4):    
                if (full_inf[b].isdigit()) and (full_inf[b+1].isdigit()) and (full_inf[b+2].isdigit()):
                    if (full_inf[b+3].isdigit()) and (full_inf[b+4].isdigit()):
                        a1 = full_inf[b]
                        a2 = full_inf[b+1]
                        a3 = full_inf[b+2]
                        a4 = full_inf[b+3]
                        a5 = full_inf[b+4]
                        full_inf = full_inf.replace(a1 + a2 + a3 + a4 + a5, a1 + a2 + ' ' + a3 + a4 + a5)
            for b in range(len(full_inf) - 2):    
                if (full_inf[b].isdigit()) and (full_inf[b+1] == ' ') and (full_inf[b+2].isdigit()):
                    a1 = full_inf[b]
                    a3 = full_inf[b+2]
                    full_inf = full_inf.replace(a1 + ' ' + a3, a1 + ' - ' + a3)    
            x1 = ''
            for h in range(len(full_inf)-2):
                x1 += full_inf[h]
            time_and_price.append(x1)
        for i, e in enumerate(films.keys()):
            a = films[e]
            a.append(time_and_price[i])
        filmsss.append(films)
    for i, e in enumerate(cinema_k.keys()):
        a = cinema_k[e]
        a.append(filmsss[i])
    cinema.update(cinema_k)
    how_many_matches = 0
    result = ''
    for k in cinema.keys():
        j = cinema[k]
        el = j[1]
        for e in el.keys():
            e_n = e.replace('ё', 'е')  #специально для "звёздные"/"звездные"
            if (movie_name in e.lower()) or (movie_name in e_n.lower()):
                s = el[e]
                n = '    &#128293;&#128293;&#128293;' + e + '&#128293;&#128293;&#128293;'
                g = '&#127902;ЖАНР: ' + s[0] + ', ' 
                l = '&#128253;ДЛИТЕЛЬНОСТЬ: ' + s[1]
                a = '&#127963;НАЗВАНИЕ КИНОТЕАТРА: ' + k
                b = '&#127988;АДРЕС: ' + j[0] + ' '
                c = '&#127903;СЕАНСЫ: ' + s[2] + ' '
                result += n + '\n' + g + '\n' + l + '\n' + a + '\n' + b +'\n' + c + '\n\n'
                how_many_matches += 1
    if how_many_matches == 0:
        to_ret = '''По Вашему запросу ничего не найдено3(, но Вы можете вспользоваться ссылками:
            https://kinoteatr.ru/raspisanie-kinoteatrov/
            https://kinomax.ru/finder
        Вдруг там есть что-то интересное)
            '''
    else:
        to_ret = result
    return to_ret

token = 'f325c7287974f63be58c9cacffd5e99fde9cce5f73dcfc440625b67c802ccfa33c909528498b458c7b4ff'
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
k = 0      #это значит, что пользователь не выбрал дату, а значит, ещё не готов выбрать фильм
now = datetime.now()              #я хочу, чтоб у меня были кнопочки на 5 дней вперёд, включая сегодня
plus_days = timedelta(days = 1)   #то есть получатся дни от сегодня до сегодня + 4
now_plus_1 = now + plus_days
now_plus_2 = now_plus_1 + plus_days
now_plus_3 = now_plus_2 + plus_days
now_plus_4 = now_plus_3 + plus_days
now_tp = now.strftime("%d.%m")              #мне удобнее хранить их именно так, ведь мне с ними ещё работать
now_plus_1_tp = now_plus_1.strftime("%d.%m")
now_plus_2_tp = now_plus_2.strftime("%d.%m")
now_plus_3_tp = now_plus_3.strftime("%d.%m")
now_plus_4_tp = now_plus_4.strftime("%d.%m")
interesting_facts = ['Первым продуктом со штрих-кодом была жевательная резинка Wrigley’s',
                     'Авиакомпания American Airlines сэкономила 40.000$ в 1987 году, уменьшив количество оливок на одну в салатах для первого класса',
                     'Человек по имени Чарльз Осборн икал в течение 68 лет',
                     'Если 111.111.111 умножить на 111.111.111, то получится 12345678987654321',
                     'Первый в истории одеколон появился как средство профилактики чумы',
                     'Зажигалка для сигарет была придумана раньше, чем обычные спички',
                     'Бедренная кость человека крепче бетона (особенно в продольном направлении)',
                     'Верблюды имеют тройное веко и два слоя ресниц для защиты глаз от песка',
                     'Некоторые гусеницы могут есть себя в отсутствие другой пищи',
                     'Когда в 1850 г. из Европы в Америку привезли первую партию воробьев, американцы так обрадовались, что закормили их всех до смерти',
                     'Принцы Вильям и Чарльз никогда не летают в одном самолете, чтобы Королевство не лишилось сразу двух наследников',
                     'Яблоки более эффективны для пробуждения организма утром, чем кофе',
                     'Большинство частиц пыли в доме происходит от омертвелой кожи',
                     'Усы необходимы кошке для перемещения в пространстве',
                     'Австралия является страной, в которой около 90% жителей поселили в своих домах кошек',
                     'Котёнок способен видеть сон уже через одну неделю после рождения',
                     'Животное способно узнавать голос своего хозяина, но в большинстве случаев игнорирует его',
                     'Во время защиты кошка прижимает уши к голове, в момент атаки уши раздвигаются в стороны',
                     'Кошки не способны пережевывать большие куски мяса. Это связано с тем, что их челюсть не может двигаться в стороны',
                     'Чтобы справиться с египтянами, ассирийские воины привязывали кошек к своим щитам, ведь ащитники Египта не могли ударить священное животное']
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            mess = event.text.lower()
            if (k == 1) and ('привет' not in mess) and ('пока' not in mess) and ('найти фильм' not in mess):
                #вот тут пользователь выбрал искать фильм, тут всё самое главное
                movie_name = mess
                vk.messages.send(
                    user_id = event.user_id,
                    message = 'Понял, принял, обрабатываю:-)',
                    keyboard = open('keyboard1.json', 'r', encoding="UTF-8").read(),
                    random_id = random.randint(0, 2048)
                )
                ind_f = random.randint(1, 20)
                fact = interesting_facts[ind_f]
                pr = '   '
                a = '''Выполняю сложные логические вычисления в поисках Вашего фильма... на самом деле, мне просто нужно немного времени&#128519;'''
                b = 'Чтобы скрасить Ваше ожидание, покажу интересный фактик: ' + fact + '&#128559;'
                mes = pr + a + '\n\n' + pr + '\n' + b
                vk.messages.send(
                    user_id = event.user_id,
                    message = mes,
                    keyboard = open('keyboard1.json', 'r', encoding="UTF-8").read(),
                    random_id = random.randint(0, 2048)
                )
                resolution = parsing(now_tp, now_plus_1_tp, now_plus_2_tp, now_plus_3_tp, now_plus_4_tp, movie_name, day)
                res =  resolution.split('\n\n')
                if '' in res:
                    res.remove('')
                for theatres in res:
                    vk.messages.send(
                        user_id = event.user_id,
                        message = theatres,
                        keyboard = open('keyboard1.json', 'r', encoding="UTF-8").read(),
                        random_id = random.randint(0, 2048)
                    )
                if len(res) != 1:
                    ss = '''Также за дополнительной информцией Вы можете обратиться к сайтам:
                        https://kinoteatr.ru/raspisanie-kinoteatrov/
                        https://kinomax.ru/finder'''
                    vk.messages.send(
                            user_id = event.user_id,
                            message = ss,
                            keyboard = open('keyboard1.json', 'r', encoding="UTF-8").read(),
                            random_id = random.randint(0, 2048)
                        )
                k = 0
            elif ('привет' in mess) or ('драст' in mess) or ('хай' in mess) or ('хаю' in mess) or ('йо' in mess):
                k = 0
                vk.messages.send(
                    user_id = event.user_id,
                    message = 'Приветик!:-)',
                    keyboard = open('keyboard1.json', 'r', encoding="UTF-8").read(),
                    random_id = random.randint(0, 2048)
                )
            elif ('пока' in mess) or ('бай' in mess):
                k = 0
                vk.messages.send(
                    user_id = event.user_id,
                    message = 'Покашечки:-(',
                    keyboard = open('keyboard1.json', 'r', encoding="UTF-8").read(),
                    random_id = random.randint(0, 2048)
                )
            elif ('назад' in mess):
                k = 0
                vk.messages.send(
                    user_id = event.user_id,
                    message = 'Будет интереснее, если Вы выберете действие с:',
                    keyboard = open('keyboard1.json', 'r', encoding="UTF-8").read(),
                    random_id = random.randint(0, 2048)
                )
            elif ('найти фильм' in mess):
                k = 0
                k_2 = k2(now_tp, now_plus_1_tp, now_plus_2_tp, now_plus_3_tp, now_plus_4_tp, back = 'Назад')
                keyboard2 = json.dumps(k_2) 
                with open('keyboard2.json', 'w', encoding='UTF-8') as f:
                    f.write(keyboard2)
                vk.messages.send(
                    user_id = event.user_id,
                    message = 'Выберите дату...',
                    keyboard = open('keyboard2.json', 'r', encoding="UTF-8").read(),
                    random_id = random.randint(0, 2048)
                )
            elif (now_tp in mess) or (now_plus_1_tp in mess) or (now_plus_2_tp in mess) or (now_plus_3_tp in mess) or (now_plus_4_tp in mess):
                day = mess
                k = 1
                vk.messages.send(
                    user_id = event.user_id,
                    message = 'А теперь введите название фильма, и я посмотрю, чем могу Вам помочь, какие сеансы подобрать)',
                    keyboard = open('keyboard1.json', 'r', encoding="UTF-8").read(),
                    random_id = random.randint(0, 2048)
                ) 
            else:
                k = 0
                vk.messages.send(
                    user_id = event.user_id,
                    message = 'Простите, но я ещё так молод, ещё не выучил такой команды&#128547;',
                    random_id = random.randint(0, 2048)
                )

