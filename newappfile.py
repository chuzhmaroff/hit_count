from flask import Flask, render_template, make_response, request
import random, os, time, hashlib
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    count_non_unique_user()
    user_cookies = str(request.cookies)
    if get_bool_unique_ip(get_ip_address()):
        add_unique_ip(get_ip_address())
        count_unique_user_for_ip()
    if len(user_cookies) == 2:  # значит куки пустые и он точно новый
        count_unique_user_for_cookie()
        resp = make_response(render_template('index.html'))
        resp.set_cookie('UID', create_unique_cookie_for_user(), max_age=60 * 60 * 24 * 365 * 4)  # 4 years
        return resp
    else:  # у него уже есть куки от нашего сайта
        # count_unique_user_for_ip()
        # count_unique_user_for_cookie()
        resp = make_response(render_template('index.html'))
        return resp


@app.route("/stat", methods=['GET', 'POST'])
def stat():
    with open("count_non_unique_user.txt") as f:
        count_non_unique_user = f.read()
    with open("count_unique_user_for_cookie.txt") as f:
        count_unique_user_for_cookies = f.read()
    with open("count_unique_user_for_ip.txt") as f:
        count_unique_user_for_ip = f.read()
    resp = render_template("stat.html", date=str(datetime.now()),
                           count_user=count_non_unique_user,
                           count_unique_ip=count_unique_user_for_ip,
                           count_unique_cookie=count_unique_user_for_cookies,
                           ip_address=get_ip_address(),
                           cookies=request.cookies,
                           user_agent=request.user_agent,
                           accept_lang=request.accept_languages)
    return resp


def get_bool_unique_ip(ip):
    with open('unique_ip.txt') as f:
        data = f.read()
        data = data.split("\n")
        if ip in data:
            return False
        else:
            return True


def add_unique_ip(ip):
    with open('unique_ip.txt', 'r+') as f:
        f.write(ip + '\n')


def count_non_unique_user():
    with open("count_non_unique_user.txt", "r+") as f:
        count = int(f.read()) + 1
        f.seek(0)
        f.truncate()
        f.write(str(count))


def create_unique_cookie_for_user():
    date = str(datetime.now())
    useragent = str(request.user_agent)
    uniq_cookies = str.join(date, useragent)
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


def get_ip_address():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = (request.environ['REMOTE_ADDR'])
    else:
        ip = (request.environ['HTTP_X_FORWARDED_FOR'])
    return str(ip)


if __name__ == '__main__':
    app.run(debug=True)
