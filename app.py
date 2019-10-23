from flask import Flask, render_template, make_response, request
import random
from datetime import datetime
import hashlib

app = Flask(__name__)

'''
main - инициализация и рендеринг основной страницы
nomain - инициализация и рендеринг тестовый вариант __main__
stat - страница статистики

'''


@app.route('/', methods=['GET', 'POST'])
def main():
    count_user()
    user_cookie = str(request.cookies)
    if len(user_cookie) == 2:  # + ip
        cookie = get_hash_cookie()
        count_uniq_cookie()
        write_uniq_cookie(cookie)
        resp = make_response(render_template('index.html'))
        resp.set_cookie("UID", cookie)
        uniq_ip()
        return resp
    else:
        uniq_ip()
        resp = make_response(render_template('index.html'))
        return resp


def nomain():
    count_user()  # подсчет не уникальных посетителей
    resp = make_response(render_template('index.html'))
    usercookie = random.randint(1, 1000000)
    resp.set_cookie('random_cookies', '%d' % usercookie)
    fix_newconnection()
    return resp


@app.route("/stat", methods=['GET', 'POST'])
def stat():
    text_usercount = read_usercount_txt()
    text_full_info = read_full_info_txt()
    text_count_uniq_cookie = read_count_uniq_cookie_txt()
    text_count_uniq_ip = read_count_uniq_ip_txt()

    return render_template("stat.html",
                           headers=request.headers,
                           date=str(datetime.now()),
                           count_user=text_usercount,
                           # fullheaders=text,
                           cookies=request.cookies,
                           user_agent=request.user_agent,
                           referens=request.referrer,
                           accept_lang=request.accept_languages,
                           ip_adress=getip(),
                           full_info=text_full_info,
                           count_uniq_ip=text_count_uniq_ip,
                           count_uniq_cookie=text_count_uniq_cookie

                           )


def fix_newconnection():
    # headers = request.headers
    cookies = request.cookies
    useragent = request.user_agent
    referens = request.referrer
    accept_languages = request.accept_languages

    f = open('full_info.txt', 'a')
    ip = getip()
    f.write('Connect ' + str(datetime.now()) +
            ' IP address: ' + ip +
            ' Cookies ' + str(cookies) +
            ' Browser ' + str(useragent) +
            ' Refer link ' + str(referens) +
            ' Accept languages' + str(accept_languages) + '\n')

    f.close()


def getip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = (request.environ['REMOTE_ADDR'])
    else:
        ip = (request.environ['HTTP_X_FORWARDED_FOR'])
    return ip


"""
!!!ВСЮ ЭТУ ЗАЛУПУ НАХУЙ ПЕРЕПИСАТЬ ЧЕРЕЗ WITH ДОЛБАЕБ!!!
"""


def count_user():
    with open('usercount.txt') as f:
        c = int(f.read())
    c += 1
    with open('usercount.txt', 'w') as f:
        f.write(str(c))


# куки - скрещенные данные текщей даты и useragent
def get_hash_cookie():
    date = str(datetime.now())
    useragent = str(request.user_agent)
    uniq_cookies = str.join(date, useragent)
    f = hashlib.md5(str(uniq_cookies).encode('utf-8'))
    enter_cookie = f.hexdigest()
    return enter_cookie


# мне надо сделать метод для отдельного подсчета уникальных посетителей по IP и по cookies
def count_uniq_cookie():
    with open('count_uniq_cookie.txt') as f:
        c = int(f.read())
    c += 1
    with open('count_uniq_cookie.txt', 'w') as f:
        f.write(str(c))


def count_uniq_ip():
    with open("count_uniq_ip.txt") as f:
        c = int(f.read())
    c += 1
    with open('count_uniq_ip.txt', 'w') as f:
        f.write(str(c))


def uniq_ip():
    with open('unique_ip.txt') as f:
        a = f.read()
    ip = getip()
    b = a.split('\n')
    if ip in b:
        return True
    else:
        write_uniq_ip(ip)
        count_uniq_ip()
        return False


def write_uniq_cookie(cookie):
    with open("unique_cookies.txt", "a") as f:
        f.write(str(cookie) + "\n")


def write_uniq_ip(ip):
    with open("unique_ip.txt", "a") as f:
        f.write(str(ip) + "\n")


def read_usercount_txt():
    with open("usercount.txt") as f:
        var = int(f.read())
    return var


def read_full_info_txt():
    with open("full_info.txt") as f:
        text = f.read()
    return text


def read_count_uniq_cookie_txt():
    with open("count_uniq_cookie.txt") as f:
        count_uniq_cookie = int(f.read())
    return count_uniq_cookie


def read_count_uniq_ip_txt():
    with open("count_uniq_ip.txt") as f:
        count_uniq_ip = int(f.read())
    return count_uniq_ip


if __name__ == '__main__':
    app.run(debug=True)
