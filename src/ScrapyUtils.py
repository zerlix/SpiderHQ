# Hilfsfuntkionen für Scrapy
from scrapy.settings import BaseSettings

def dump_scrapy_settings(settings):
    # Dump scrpay settings
    for setting, value in settings.items():
        if isinstance(value, BaseSettings):
            value = value.copy_to_dict()
        print(f"{setting}: {value}")