from urllib import request, error
import re
from data import sources

def getByUrl(url):
    r = request.build_opener().open(url)
    html = r.read()
    r.close()
    return html

def getFromOrakul(horoscope, sign):
    url = sources["orakul.com"]["url"].format(horoscope=horoscope, sign=sign)
    print("Retrieving " + url + " ...")
    try:
        html = getByUrl(url).decode("utf-8")
    except error.URLError as e:
        print(e.reason)
        return "Ошибка получения данных"
    prediction = re.search("\<p class\=\"\"\>\s*([^<]+)\s*\<\/p\>", html, re.UNICODE)
    if prediction != None:
        return str(prediction.group(1))
    else:
        return "Данных нет."


def getFromMail(horoscope, sign):
    url = sources["horo.mail.ru"][horoscope + "_url"].format(horoscope=horoscope, sign=sign)
    print("Retrieving " + url + " ...")
    try:
        html = getByUrl(url).decode("utf-8")
    except error.URLError as e:
        print(e.reason)
        return "Ошибка получения данных"
    prediction = re.search("\<div class\=\"article__item article__item_alignment_left article__item_html\"\><p>\s*([^\n]+)\s*\<\/p\>", html, re.UNICODE)
    if prediction != None:
        return str(prediction.group(1)).replace("<br />", "").replace("&mdash;", "-")
    else:
        return "Данных нет."