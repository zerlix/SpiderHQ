from config.config import *
from src.ScrapyUtils import dump_scrapy_settings
from src.init import init
import src.database.MariaDB as mdb
from scrapy.utils.project import get_project_settings
from multiprocessing import Process
import os



def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    # Projektverzeichnis
    #os.environ['SCRAPY_SETTINGS_MODULE'] = 'ufp_de.settings'
    #print(dump_scrapy_settings(get_project_settings()))
    info('function f')
    print('hello', name)


def test():  
    #os.environ['SCRAPY_SETTINGS_MODULE'] = 'ufp_de.settings'
    #print(dump_scrapy_settings(get_project_settings()))
    
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
    

if __name__ == "__main__":
    init()
    test()
    