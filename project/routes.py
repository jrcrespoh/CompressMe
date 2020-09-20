from flask import json, request, render_template, make_response, send_from_directory
from project import application
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request


@application.route("/")
def index():
    return render_template("index.html")


@application.route("/files", methods=['GET', 'POST'])
def activities():
    if request.method == 'POST':
        url = request.form.get("url")
        if indexed(url):
            return json.jsonify(success=True)
        else:
            return compress(url)
    else:
        return render_template("files.html")


@application.route("/fetch", methods=['POST'])
def download():
    url = request.form.get("url")
    try:
        filename = fetch_file(url)
    except Exception:
        return
    return send_from_directory("sites",
                               filename,
                               as_attachment=True,
                               attachment_filename="site.txt")


@application.route("/latest", methods=['POST'])
def get_latest():
    try:
        with open("project/sites/indexed.json", mode='r') as f:
            index = json.load(f)
        return json.jsonify(success=True, sites=index['latest'])
    except Exception:
        return json.jsonify(success=False)


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def extract_content(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def indexed(url):
    try:
        with open("project/sites/indexed.json", mode='r') as f:
            index = json.load(f)
        return url in index['sites']
    except Exception:
        return False


def compress(url):
    try:
        html = urllib.request.urlopen(url).read()
        content = extract_content(html)
        with open("project/sites/indexed.json", mode='r') as f:
            index = json.load(f)
        count = index['count']
        with open(f"project/sites/{count}.txt", mode='x') as f:
            f.write(content)
        index['sites'][url] = count
        index['latest'].append(url)
        index['latest'].pop(0)
        index['count'] += 1
        with open("project/sites/indexed.json", mode='w') as f:
            json.htmlsafe_dump(index, f)
        return json.jsonify(success=True)
    except Exception:
        return json.jsonify(success=False)


def fetch_file(url):
    try:
        with open("project/sites/indexed.json", mode='r') as f:
            index = json.load(f)
        site = index['sites'][url]
        return f'{site}.txt'
    except Exception as e:
        raise e
