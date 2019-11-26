import hashlib
import sqlite3
from datetime import datetime

import requests
from flask import Flask, render_template, make_response, request, send_file

app = Flask(__name__)

'''
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
'''


@app.route('/')
def hello_world():
    return 'Server importthis.pythonanywhere.com'


@app.route('/upload', methods=['GET', 'POST'])
def main():
    user_cookies = str(request.cookies)
    filename = "1pic_stat.png"
    res = send_file(filename, mimetype='image/gif')
    # Передалать подсчет уникальных IP
    if not get_bool_unique_ip(get_ip_address()):
        count_unique_user_for_ip()
    if len(user_cookies) == 2 or len(user_cookies) == 77 or len(
            user_cookies) == 90 or len(user_cookies) == 38:  # значит куки пустые и он точно новый
        count_unique_user_for_cookie()
        user_agent = str(request.user_agent)
        cookie_for_user = create_unique_cookie_for_user(user_agent)
        res.set_cookie('chzmrff-id-image-cookie', cookie_for_user,
                       max_age=60 * 60 * 24 * 365 * 4)  # 4 years
        add_user_at_databases(get_ip_address(),cookie_for_user)
        return res
    else:  # у него уже есть куки от нашего сайта
        add_user_at_databases(get_ip_address(), str(request.cookies))
        return res


# Реализовано только для выборки по дня или вывод всех не укальных посещений
# Надо сделать вывод уникальных посещений для API
@app.route('/api', methods=['GET'])
def api():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if request.method == "GET":
        value_non_unique_day = request.args.get("non_unique_day")
        value_non_unique_month = request.args.get("non_unique_month")
        value_non_unique_year = request.args.get("non_unique_year")
        value_non_unique_all = request.args.get("non_unique_all")
        value_unique = request.args.get("unique")
        res = ""
        if value_unique == "ip":
            try:
                with open("count_unique_user_for_ip.txt", "r") as f:
                    return f.read()
            except:
                return "Ошибка при получении уникальых по IP"
        if value_unique == "cookie":
            try:
                with open("count_unique_user_for_cookie.txt", "r") as f:
                    return f.read()
            except:
                return "Ошибка при получении уникальных cookie"
        if value_non_unique_day is not None:
            try:
                for x in cursor.execute("SELECT count() FROM USER_INFO WHERE DATE = {}".format(value_non_unique_day)):
                    res += str(x)
                return res
            except:
                return "You did not enter a search date. Reference - serverimportthis.pythonanywhere.com/api"
        if value_non_unique_all is "":
            for x in cursor.execute("SELECT count() FROM USER_INFO"):
                res += str(x)
            return res
        return make_response(render_template('help_api.html'))
    return "serverimportthis.com"


# Полностью переписать статистику. Добавить отдельную страницу с выдачей всей инфы из БД
@app.route("/stat", methods=['GET', 'POST'])
def stat():
    ip_address = get_ip_address()
    adding_last_conn_to_txt()
    resp = render_template("stat.html", date=str(datetime.now()),
                           count_user=get_count_non_unique_user(),
                           count_unique_ip=do_read("count_unique_user_for_ip.txt"),
                           count_unique_cookie=do_read("count_unique_user_for_cookie.txt"),
                           ip_address=get_ip_address(),
                           cookies=request.cookies,
                           user_agent=request.user_agent,
                           accept_lang=request.accept_languages,
                           full_info_geo=get_info_on_ip(ip_address),
                           lat=get_coordinates_ip(ip_address)[0],
                           lon=get_coordinates_ip(ip_address)[1])
    return resp


def get_count_non_unique_user():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    res = ""
    for x in cursor.execute("SELECT count() FROM USER_INFO"):
        res += str(x)
    return res[1:4]


def adding_last_conn_to_txt():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    res = ""
    for line in cursor.execute("SELECT * FROM user_info"):
        res += str(line) + " \n"

    with open('info_last_conn_07112019.txt', 'w') as f:
        f.write(str(res))


def do_read(path):
    with open(path, "r") as f:
        res = f.read()
    return res


def get_info_on_ip(ip):
    info_or_ip = ""
    response = requests.get(
        "http://ip-api.com/line/{}?fields=country,countryCode,region,regionName,city,query".format(ip))
    for line in response:
        info_or_ip += str(line)
    return info_or_ip


def get_coordinates_ip(ip):
    response = requests.get("http://ip-api.com/line/{}?fields=lat,lon".format(ip))
    a = ""
    for line in response:
        a += str(line)
    lat = float(a[2:9])
    lon = float(a[11:18])
    return lat, lon


def add_user_at_databases(ip_adress, cookie_for_user):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    ref_time = int(datetime.now().strftime('%y%m%d'))
    user_info = [(str(ip_adress), str(cookie_for_user), ref_time)]
    cursor.executemany("INSERT INTO user_info VALUES (?,?,?)", user_info)
    conn.commit()


def get_bool_unique_ip(ip_adress):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    a = ""
    for x in cursor.execute("SELECT IP_ADRESS FROM USER_INFO"):
        a += str(x)
    if ip_adress in a:
        return True
    else:
        return False


def create_unique_cookie_for_user(user_agent): # Протестировать
    date = str(datetime.now())

    uniq_cookies = str.join(date, user_agent)
    f = hashlib.md5(str(uniq_cookies).encode('utf-8'))
    enter_cookie = f.hexdigest()
    return enter_cookie


def count_unique_user_for_ip():
    with open("count_unique_user_for_ip.txt", "r+") as f:
        count = int(f.read()) + 1
        f.seek(0)
        f.truncate()
        f.write(str(count))


def count_unique_user_for_cookie():
    with open("count_unique_user_for_cookie.txt", "r+") as f:
        count = int(f.read()) + 1
        f.seek(0)
        f.truncate()
        f.write(str(count))


def get_ip_address(): #Что то придумать с этим ( я про тестировку)
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = (request.environ['REMOTE_ADDR'])
    else:
        ip = (request.environ['HTTP_X_FORWARDED_FOR'])
    return str(ip)


if __name__ == '__main__':
    app.debug = True
    app.run()
