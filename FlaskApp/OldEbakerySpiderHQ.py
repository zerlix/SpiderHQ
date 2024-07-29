import os
import sys
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_dir)
from config import config as cfg
from src.init import init
from flask import Flask, render_template, request, redirect, url_for, flash, session
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader
from src.ScrapyUtils import dump_scrapy_settings 
from scrapy.crawler import CrawlerProcess


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Geheimen Schlüssel für Sessions festlegen


@app.route('/')
def home():
    if 'username' in session:
        # Wenn der Benutzer angemeldet ist, wird die Seite mit dem Namen 'home.html' gerendert
        
        return render_template('home.html', username=session['username'], scrapyProjects=cfg.scrapyProjects)

    return redirect(url_for('login'))


@app.route('/get_project', methods=['GET'])
def get_project():
    project = request.args.get('project')
    content = load_project(project)
    return content


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == cfg.USERNAME and password == cfg.PASSWORD:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Ungültiger Benutzername oder Passwort!')
    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


def load_project(project):
    # Setze das Projektverzeichnis als Umgebungsvariable
    sys.path.append(os.path.abspath(project))
    os.environ['SCRAPY_SETTINGS_MODULE'] = f"{project}.settings"
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    dump_scrapy_settings(settings)
    
    
    # Lade das Projekt
    spider_loader = process.spider_loader
    for spider_name in spider_loader.list():
        print(f"Verfügbare Spider: {spider_name}")
        
    # Gib das geladene Projekt zurück
    return spider_name
    #return dump_scrapy_settings(settings)

if __name__ == '__main__':
    init()
    app.run(debug=True)
