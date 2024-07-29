import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

## Eigene libs
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_dir)
from config.config import scrapyProjects, DIRS
from config.logging_config import LOGGING_CONFIG
from src.ScrapyProject import ScrapyProject
from src.database.MariaDB import MariaDatabase

# Flask
from flask import Flask, render_template, request, redirect, url_for, flash, session
app = Flask(__name__)
#app.secret_key = 'your_secret_key'  # Geheimen Schlüssel für Sessions festlegen

### Logging
import logging
import logging.config
logging.config.dictConfig(LOGGING_CONFIG)
#flask_app_logger = logging.getLogger('flask_app')
#werkzeug_logger = logging.getLogger('werkzeug')
#werkzeug_logger.addHandler(flask_app_logger.handlers[0])
#flask_app_logger.info("Starting FlaskApp")


def init_app():
    global scrapy_projects
    scrapy_projects = []
    for project_name in scrapyProjects:
        project_dir = os.path.join(DIRS['DIR_APP'], DIRS['DIR_SCRAPY'], project_name)
        scrapy_projects.append(ScrapyProject(project_dir))
       


def load_scrapy_project(project_dir):
    sys.path.append(os.path.abspath(project_dir))
    os.environ['SCRAPY_SETTINGS_MODULE'] = f"{os.path.basename(project_dir)}.settings"
    #flask_app_logger.info(f"load_scrapy_project: Loading settings from {os.path.abspath(project_dir)}.settings")
    settings = get_project_settings()
    return CrawlerProcess(settings)



@app.route('/start_spider', methods=['POST'])
def start_spider():
    spider_name = request.form.get('spider_name')
    project_name = request.form.get('project_name')
    project = scrapy_projects.get(project_name)
    if project:
        project.start_spider(spider_name)
        return "Spider started"
    else:
        return "Project not found"


@app.route('/project/<project_name>', methods=['GET'])
def project(project_name):
    global scrapy_projects
    for project in scrapy_projects:
        if project.settings.get('BOT_NAME') == project_name:
            # Projekt gefunden, rendern der Vorlage
            spiders = project.get_spiders()
            print(f"scrapy_projects: {scrapy_projects}")  # Debugging-Ausgabe

            return render_template('index.html',
                                    spiders=spiders, 
                                    project=project,
                                    scrapy_projects=scrapy_projects)

    # Kein Projekt mit dem angegebenen BOT_NAME gefunden
    return "Projekt nicht gefunden"

    
@app.route('/')
def home():
    #flask_app_logger.info("home() function called")
    global scrapy_projects
    # Logik für die Hauptseite
    #flask_app_logger.info(scrapy_projects)
    return render_template('index.html', scrapy_projects=scrapy_projects)



if __name__ == '__main__':
    init_app()
    #app.run(host="0.0.0.0", port=5000, debug=True)
    app.run()
    