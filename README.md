# SpiderHQ

SpiderHQ ist eine Webanwendung zum Überwachen und Steuern von Scrapy-Spiders. Die extrahierten Daten werden zur späteren Verarbeitung in einem MariaDB-Datenbankserver gespeichert. Die Anwendung ist unter http://127.0.0.1:5000 erreichbar.

# Features

* Einfaches Erstellen von Spider-Projekten (scrapy startproject Projektname)
* Unterstützung für Selenium, Scrapy, Scrapy-Splash, BeautifulSoup4 und andere Bibliotheken
* Aktivierbare Proxy-Funktion, um Bans vorzubeugen
* aktualisiert automatisch die Proxy Liste (tmp/proxy_list.tmp)
* Webanwendung mit Flask zum Überwachen der Spiders und Steuern der Scrapy-Projekte (noch nicht implemtiert)
* Extrahierte Daten werden auf einem separaten MariaDB-Datenbankserver gespeichert
* Verbindung zum Datenbankserver über einen SSH-Tunnel (z.B. HeidiSQL) möglich, um aus den Daten eine CSV-Datei zu erzeugen. Andere Datenformate, wie z.B. JSON, werden ebenfalls unterstützt

# Proxyliste
Die Proxyliste kann in der [config/ebakeryConfig.py](https://github.com/ebakery-de/EbakerySpiderHQ/blob/main/config/ebakeryConfig.py) geändert werden. 
```
##############################################
# Proxys
###############################################
proxy_list_download = 'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt'
```
Es werden nur http oder https Proxys unterstützt. Das format der Dateien muss folgenden Schema folgen
```
http://host1:port
http://username:password@host2:port
https://host3:port
```
