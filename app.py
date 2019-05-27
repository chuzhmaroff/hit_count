from flask import Flask, render_template, make_response, request
from datetime import datetime
import random

app = Flask(__name__)


@app.route("/stat", methods=['GET', 'POST'])
def stat():
    f = open('usercount.txt')
    count_user = f.read()
    f.close()

    f = open('users.txt')
    text = f.read()
    # text = a.split('new')

    return render_template("stat.html",
                           headers=request.headers,
                           date=str(datetime.now()),
                           count_user=count_user,
                           fullheaders=text,
                           cookies=request.cookies,
                           user_agent=request.user_agent,
                           referens=request.referrer,
                           accept_lang=request.accept_languages,
                           ip_adress=getip()
                           )


def getip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = (request.environ['REMOTE_ADDR'])
    else:
        ip = (request.environ['HTTP_X_FORWARDED_FOR'])
    return ip


def newconnection():
    headers = request.headers
    cookies = request.cookies
    useragent = request.user_agent
    referens = request.referrer
    accept_languages = request.accept_languages

    f = open('users.txt', 'a')
    ip = getip()
    f.write('Connect ' + str(datetime.now()) +
            ' IP address: ' + ip +
            ' Cookies ' + str(cookies) +
            ' Browser ' + str(useragent) +
            ' Refer link ' + str(referens) +
            ' Accept languages' + str(accept_languages) + '\n')

    f.close()


def count_user():
    f = open('usercount.txt')
    usernumber = f.read()
    f.close()
    num = int(usernumber)
    num += 1
    p = open('usercount.txt', 'w')
    p.write(str(num))
    p.close()


@app.route("/", methods=['GET', 'POST'])
def main():
    count_user()
    newconnection()
    # Выдача псевдо куки
    # usercookie = random.randint(1, 1000000)
    # resp = make_response(render_template('index.html'))
    # resp.set_cookie('random_cookies', '%d' % usercookie)
    return render_template('index.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")


@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    return render_template("gallery.html")


if __name__ == "__main__":
    # app.run(host='192.168.15.82')
    app.run(debug=True)
    # app.run(host='192.168.0.1')
