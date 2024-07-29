from scrapy import logformatter

class CustomLogFormatter(logformatter.LogFormatter):
    def dropped(self, entry, exception, extras):
        # Überschreibe die dropped-Methode, um den Formattername nicht zu protokollieren
        return self._format_entry(entry, exception)
