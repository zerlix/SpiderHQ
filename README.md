# SpiderHQ

SpiderHQ ist eine Webanwendung zum Überwachen und Steuern von Scrapy-Spiders. Die extrahierten Daten werden zur späteren Verarbeitung in einem MariaDB-Datenbankserver gespeichert. Die Anwendung ist unter http://127.0.0.1:5000 erreichbar.

# Features

* Einfaches Erstellen von Spider-Projekten (scrapy startproject Projektname)
* Unterstützung für Selenium, Scrapy, Scrapy-Splash, BeautifulSoup4 und andere Bibliotheken
* Aktivierbare Proxy-Funktion, um Bans vorzubeugen
* aktualisiert automatisch die Proxy Liste (tmp/proxy_list.tmp)
* Webanwendung mit Flask zum Überwachen der Spiders und Steuern der Scrapy-Projekte (noch nicht vollständig)


# Proxyliste
Die Proxyliste kann in der [config/config.py](Config.py](https://github.com/zerlix/SpiderHQ/blob/main/config/config.py)) geändert werden. 
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
