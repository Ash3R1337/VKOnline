# VKOnline
VKOnline 1.0
Данный скрипт позволяет легко узнать статус онлайна пользователя сети ВКонтакте только по его ID, просматревать статус сразу десятка пользователей и удалять уже неотслеживаемых, просмотреть полную ПУБЛИЧНУЮ информацию о пользователе, которую он указал у себя в профиле. Вся информация предоставлена в интернете и является ПУБЛИЧНОЙ.

Установка и использование.
Termux:
git clone https://github.com/Ash3R1337/VKOnline.git
pip install --upgrade pip
pkg install wheel
pkg install libxml2 libxslt
pip install lxml ИЛИ 
CFLAGS="-O0" pip install lxml (Если загрузка идет долго)
cd VKOnline
python3 VKOnline.py
