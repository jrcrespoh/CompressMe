from flask import jsonify, request, render_template, url_for
import json
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
        #if request.form.get('message') == 'getSaved':
        url = request.form.get("url")
        html = urllib.request.urlopen(url).read()
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

