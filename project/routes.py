from flask import jsonify, request, render_template, url_for
import json
from project import application
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

index = ""

@application.route("/")
def index():
    return render_template("index.html")


@application.route("/files", methods=['GET', 'POST'])
def activities():
    if request.method == 'POST':
        url = request.form.get("url")
        if indexed(url):
            file_url = fetch_file(url)
            return jsonify(success=True, file_url=file_url)
        else:
            process(url)
        try:
            html = urllib.request.urlopen(url).read()
        except urllib.URLError:
            return jsonify(sucess=False, file_url=None)
        return text_from_html(html)

    else:
        return render_template("files.html")


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def indexed(url):
    pass


def process(url):
    pass


def fetch_file(url):
    pass
