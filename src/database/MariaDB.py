import mariadb
import sys
from config import config as cfg
import logging
import logging.config
from config.logging_config import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)
database_logger = logging.getLogger('database')

class MariaDatabase:
    '''
    Klasse zur Verbindung mit der MariaDB Datenbank
    
    Attribute:
        host (str): Hostname des Datenbankservers
        port (int): Portnummer des Datenbankservers
        user (str): Username zur Anmeldung an der Datenbank
        password (str): Passwort zur Anmeldung an der Datenbank
        database (str): Name der Datenbank
        connection (mariadb.connection): Verbindung zur Datenbank
        cursor (mariadb.cursor): Cursor zur Datenbankabfrage
    '''
    def __init__(self, host=cfg.db_host, port=cfg.db_port, user=cfg.db_user, password=cfg.db_password, database=cfg.db_database):
        '''
        Konstruktor der Klasse MariaDatabase
        
        Args:
            host (str): Hostname des Datenbankservers
            port (int): Portnummer des Datenbankservers
            user (str): Username zur Anmeldung an der Datenbank
            password (str): Passwort zur Anmeldung an der Datenbank
            database (str): Name der Datenbank
        Returns:
            None
        '''
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        '''
        Methode zur Herstellung der Verbindung zur Datenbank
        Args:
            None
        
        Returns:
            None
        '''
        try:
            self.connection = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            database_logger.info("Verbindung zur Datenbank hergestellt")
            self.cursor = self.connection.cursor()
        except mariadb.Error as e:
            database_logger.error(f"Fehler bei der verbindung zur Datenbank: {e}")
            sys.exit(1)


    def disconnect(self):
        '''
        Methode zur Trennung der Verbindung zur Datenbank
        Args:
            None
            
        Returns:
            None
        '''
        if self.connection:
            self.cursor.close()
            self.connection.close()
            database_logger.info("Verbindung zur Datenbank geschlossen")


    def execute_query(self, query):
        '''
        Methode zur Ausführung einer Abfrage an die Datenbank
        Args:
            query (str): SQL-Abfrage an die Datenbank
        
        Returns:
            None
        '''
        try:
            self.cursor.execute(query)
            database_logger.info("Abfrage erfolgreich ausgeführt: " + query)
        except mariadb.Error as e:
            database_logger.error(f"Fehler bei der Ausführung der Abfrage: {e}")
            

    def fetch_results(self):
        '''
        Methode zum Abrufen der Ergebnisse einer Abfrage
        Args:
            None
        Returns:
            results (list): Liste der Ergebnisse
        '''
        try:
            results = self.cursor.fetchall()
            return results
        except mariadb.Error as e:
            database_logger.error(f"Fehler beim Abrufen der Ergebnisse: {e}")
            return []

    def create_table(self, table_name, columns):
        '''
        Methode zur Erstellung einer Tabelle
        Args:
            table_name (str): Name der Tabelle
            columns (str): Spalten der Tabelle

        Returns:
            None
        '''
        try:
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
            self.execute_query(query)
            database_logger.info(f"Tabelle {table_name} erstellt")
        except mariadb.Error as e:
            database_logger.error(f"Fehler beim Erstellen der Tabelle: {e}")
            sys.exit(1)


    def insert_update(self, table_name, item, primary_key):
        columns = ', '.join([f"`{column}`" for column in item.keys()])
        values = ', '.join([f"'{value}'" for value in item.values()])
        
        update_clause = ', '.join([f"`{column}` = VALUES(`{column}`)" for column in item.keys() if column != primary_key])

        query = f"""
            INSERT INTO `{table_name}` ({columns})
            VALUES ({values})
            ON DUPLICATE KEY UPDATE {update_clause}
        """
        try:
            self.cursor.execute(query)
            self.connection.commit()
            database_logger.info(f"Eintrag in {table_name} erfolgreich eingefügt oder aktualisiert.")
        except mariadb.Error as e:
            database_logger.error(f"Fehler beim Einfügen oder Aktualisieren des Eintrags in {table_name}: {e} {query}")



