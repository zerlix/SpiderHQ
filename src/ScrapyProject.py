import os
import sys
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.spiderloader import SpiderLoader



class ScrapyProject:
    '''
    Klasse zur Verwaltung eines Scrapy Projektes
    Attribute:
        project_dir (str): Verzeichnis des Projektes
        process (CrawlerProcess): Instanz des CrawlerProcess
        settings (scrapy.settings.Settings): Einstellungen des Scrapy Projektes
        crawler_process (CrawlerProcess): Instanz des CrawlerProcess 
    '''
    
    def __init__(self, project_dir):
        '''
        Konstruktor der Klasse ScrapyProject
        '''
        self.project_dir = project_dir
        self.name = self.project_dir.split('/')[-1]
        self.process = self.load_project()

    def load_project(self):
        '''
        Methode zum Laden eines Scrapy Projektes
        Args:
            None
        Returns:
            CrawlerProcess: Instanz des CrawlerProcess
        '''
        sys.path.append(os.path.abspath(self.project_dir))
        os.environ['SCRAPY_SETTINGS_MODULE'] = f"{os.path.basename(self.project_dir)}.settings"
        self.settings = get_project_settings()
        self.crawler_process = CrawlerProcess(self.settings)
        return self.crawler_process

    def start_spider(self, spider_name):
        '''
        Methoden zum Starten eines Spiders
        Args:
            spider_name (str): Name des Spiders
        Returns:
            None
        '''
        self.process.crawl(spider_name)
        self.process.start()

    def stop_spider(self, spider_name):
        pass
        # Implementieren Sie die Logik zum Stoppen eines Spiders

    def get_spider_status(self, spider_name):
        pass
        # Implementieren Sie die Logik zum Abrufen des Spider-Status

    def get_spider_stats(self, spider_name):
        pass
        # Implementieren Sie die Logik zum Abrufen der Spider-Statistiken
    
    def is_idle(self):
        '''
        Methode prüft, ob der Crawler gerade nicht läuft
        Returns:
            True, wenn der Crawler gerade nicht läuft, sonst False
        '''
        if not self.process.crawlers:
            return True
        return False
    
    def is_running(self):
        '''
        Methode prüft, ob der Crawler gerade läuft
        Returns:
            True, wenn der Crawler gerade läuft, sonst False
        '''
        if self.process.crawlers:
            return True
        return False
    

    def get_spiders(self):
        '''
        Methode gibt die Liste der Spidern von dem Projekt zurück
        Returns:
            Liste von Spidern
        '''
        loader = SpiderLoader.from_settings(self.settings)
        return loader.list()
    
    
    def get_logfile_path(self):
        '''
        Methode gibt den Pfad zum Logfile zurück
        Returns:
            Pfad zum Logfile
        '''
        return os.path.join(self.project_dir, 'logs', f'{self.name}.log')

    