from bs4 import BeautifulSoup
import requests
import os
import codecs

def menu():
    print('\n\033[91m1: Отследить пользователя\n2: Список отслеживаемых пользователей\n3: Удалить из списка\033[0m')
    MenuAns = input()
    menus = {
        '1': 'Отследить пользователя',
        '2': 'Список отслеживаемых пользователей',
        '3': 'Удалить из списка',
    }
    if MenuAns in menus:
        print('\033[92mВыбрано: {}\033[0m'.format(menus[MenuAns]))
        if MenuAns == '1':
            NewUser()
        elif MenuAns == '2':
            Track()
        elif MenuAns == '3':
            Delete()
    else:
        print('\033[91mТакого значения нет\033[0m')
        menu()

def menu_user():
    print('\n\033[91m1: Отследить пользователя\n2: Список отслеживаемых пользователей\n3: Вся информация о пользователе\n4: Главное меню\033[0m')
    MenuUserAns = input()
    MenusUser = {
        '1': 'Отследить пользователя',
        '2': 'Список отслеживаемых пользователей',
        '3': 'Вся информация о пользователе',
        '4': 'Главное меню'
    }
    if MenuUserAns in MenusUser:
        print('\033[92mВыбрано: {}\033[0m'.format(MenusUser[MenuUserAns]))
        if MenuUserAns == '1':
            NewUser()
        elif MenuUserAns == '2':
            Track()
        elif MenuUserAns == '3':
            Info()
        elif MenuUserAns == '4':
            menu()
    else:
        print('\033[91mТакого значения нет\033[0m')
        menu_user()

#Парсер
def get_html(url):
    r = requests.get(url)
    r.encoding = 'utf8'
    return r.text

def get_head(html):
    soup = BeautifulSoup(html, 'lxml')
    head = soup.findAll('div', class_='user-field__value')
    heads = []
    for i in head:
       heads.append(i.string)
    return heads

def NewUser(): #Получаем через парсер всю информацию, выводим онлайн или оффлайн
    UserId = input('Введите id пользователя: ')
    print('\033[92mПроверка пользователя...\033[0m')
    try:
        VkStat = get_head(get_html('https://vkfaces.com/vk/user/{}'.format(UserId)))
        F_Name = VkStat[6].replace('\n', '').lstrip().rstrip()
        S_Name = VkStat[7].replace('\n', '').lstrip().rstrip()
        Online_Stat = VkStat[1].replace('\n', '').lstrip().rstrip()
        if len(Online_Stat) > 13: 
            print('Статус пользователя {} {}: '.format(F_Name, S_Name), '\033[93mбыл(а) в сети {}\033[0m'.format(Online_Stat))
            f2 = codecs.open('tempUser.txt', 'w', 'utf-8') #Сохраням всю информацию о действующем пользователе, чтобы можно было её предоставить
            for i in VkStat:
                if i != None:
                    f2.write("%s\n" % i.lstrip().rstrip())
            f2.close()
            f = codecs.open('users.txt', 'r+', 'utf-8') #Сохраняем id пользователя в файл, если он уже есть там, то не сохраняем и закрываем файл
            l = [line.strip() for line in f]
            if UserId not in l:
                f.close()
                f = codecs.open('users.txt', 'a+', 'utf-8')
                f.write("%s\n" % UserId)
                f.close()
            else:
                f.close()
            menu_user()
        else: 
            print('Статус пользователя {} {}:\033[92m {}\033[0m'.format(F_Name, S_Name, Online_Stat)) #Дальше всё как для if выше
            f2 = codecs.open('tempUser.txt', 'w', 'utf-8')
            for i in VkStat:
                if i != None:
                    f2.write("%s\n" % i.lstrip().rstrip())
            f2.close()
            f = codecs.open('users.txt', 'r+', 'utf-8')
            l = [line.strip() for line in f]
            if UserId not in l:
                f.close()
                f = codecs.open('users.txt', 'a+', 'utf-8')
                f.write("%s\n" % UserId)
                f.close()
            else:
                f.close()
            menu_user()
    except IndexError:
        print('\033[91mПользователь не найден, введите ID заново\033[0m')
        NewUser()
    except requests.exceptions.ConnectionError: 
        print('\033[91mОшибка! Нет соединения с интернетом\033[0m')
        menu()

def Track(): #id хранятся в отдельном файле, можно их считывать и выводить
    f = codecs.open('users.txt', 'r+', 'utf-8')
    l = [line.strip() for line in f]
    try:
        for i in range(len(l)):
            VkStat = get_head(get_html('https://vkfaces.com/vk/user/{}'.format(l[i])))
            F_Name = VkStat[6].replace('\n', '').lstrip().rstrip()
            S_Name = VkStat[7].replace('\n', '').lstrip().rstrip()
            Online_Stat = VkStat[1].replace('\n', '').lstrip().rstrip()
            if len(Online_Stat) > 13:
                print('Статус пользователя {} {}: '.format(F_Name, S_Name), '\033[93mбыл(а) в сети {}\033[0m'.format(Online_Stat))
            else:
                print('Статус пользователя {} {}:\033[92m {}\033[0m'.format(F_Name, S_Name, Online_Stat))
    except requests.exceptions.ConnectionError:
        print('\033[91mОшибка! Нет соединения с интернетом\033[0m')
        menu()
    f.close()
    menu()

def Delete(): #Файл с id пользователей перезаписывается без удаляемого id, так удаляем пользователя из файла
    f = codecs.open('users.txt', 'r+', 'utf-8')
    l = [line.strip() for line in f]
    print('IDs: ' + ', '.join(l))
    f.seek(0)
    user_del = input('Введите id пользователя, которого надо удалить из списка: ')
    if user_del in l:
        for line in l:
            if line != user_del:
                f.write("%s\n" % line)
        print('\033[92mУспешно удалено\033[0m')
        f.truncate()
    else:
        print('\033[91mОшибка! Пользователя нет в списке\033[0m')
    f.close()
    menu()

def Info():
    f2 = codecs.open('tempUser.txt', 'r+', 'utf-8')
    l2 = [line.strip() for line in f2]
    print(
    '''
    \033[93mИнформация о пользователе {} {}\033[0m
    Статус: {}
    Последнее посещение: {}
    Количество фотографий: {}
    '''.format(l2[5], l2[6], l2[0], l2[1], l2[2])
    )
    print(
    '''
            \033[92mОсновная информация\033[0m
    Реальный ID: {}
    Домен профиля: {}
    Отчество: {}
    Пол: {}
    Дата рождения: {}
    Родной город: {}
    '''.format(l2[3], l2[4], l2[7], l2[8], l2[9], l2[10])
    )
    print(
    '''
            \033[92mКонтактная информация\033[0m
    Страна: {}
    Город: {}
    Сайт: {}
    Skype: {}
    Facebook: {}
    Twitter: {}
    Livejournal: {}
    Instagram: {}
    '''.format(l2[11], l2[12], l2[13], l2[14], l2[15], l2[16], l2[17], l2[18])
    )
    print(
    '''
            \033[92mЛичная информация\033[0m
    Деятельность: {}
    Интересы: {}
    Любимая музыка: {}
    Любимые фильмы: {}
    Любимые телешоу: {}
    Любимые книги: {}
    Любимые игры: {}
    Любимые цитаты: {}
    О себе: {}
    '''.format(l2[19], l2[20], l2[21], l2[22], l2[23], l2[24], l2[25], l2[26], l2[27])
    )
    print(
    '''
            \033[92mЖизненная позиция\033[0m
    Политические предпочтения: {}
    Мировоззрение: {}
    Главное в жизни: {}
    Главное в людях: {}
    Отношение к курению: {}
    Отношение к алкоголю: {}
    Вдохновляют: {}
    '''.format(l2[28], l2[29], l2[30], l2[31], l2[32], l2[33], l2[34])
    )
    f2.close()
    menu()


print('\033[92m------------------------------------VKOnline v1.0------------------------------------\033[0m')
if os.path.exists('users.txt'): #Проверка на существование файлов, с которыми будем работать
    f = codecs.open('users.txt', 'r+', 'utf-8')
else:
    f = codecs.open('users.txt', 'w', 'utf-8')

if os.path.exists('tempUser.txt'):
    f2 = codecs.open('tempUser.txt', 'r+', 'utf-8')
else:
    f2 = codecs.open('tempUser.txt', 'w', 'utf-8')
menu()