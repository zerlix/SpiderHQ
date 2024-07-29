import os

################################################
# Spider liste
#################################################
scrapyProjects = ['ufp_de', 'idealo']
#scrapyProjects = ['ufp_de']


################################################
# Datenbank
################################################
db_host = "192.168.1.100" 
#db_host = "192.168.0.107"
db_port = 3306
db_user = "EbakerySpiderHQ"
db_password = "EbakerySpiderHQ"
db_database = "EbakerySpiderHQ"

###############################################
# Flask Configuration
##############################################
USERNAME = 'user'
PASSWORD = 'pass'


################################################
# System Verzeichnisse
################################################
DIR_APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = {
    'DIR_APP': DIR_APP,
    'DIR_SCRAPY': os.path.join(DIR_APP, 'scrapy_projects'),
    'DIR_LOG': os.path.join(DIR_APP, 'log'),
    'DIR_TMP': os.path.join(DIR_APP, 'tmp'),
}
for dir_name in DIRS.values():
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


##############################################
# Proxys
###############################################
proxy_list_download = 'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt'
proxy_file = os.path.join(DIRS['DIR_TMP'], 'proxy_list.tmp')



