import os
import sys
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(project_dir)
from config.config import DIRS 
LOG_DIR = DIRS['DIR_LOG']


LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'flask_app': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'flask_app.log'),
            'formatter': 'default',
            'level': 'DEBUG'
        },
        'database': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'database.log'),
            'formatter': 'default',
            'level': 'DEBUG'
        }
    },
    'loggers': {
        'flask_app': {
            'handlers': ['flask_app'],
            'level': 'DEBUG',
            'propagate': False
        },
        'database': {
            'handlers': ['database'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
