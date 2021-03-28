import os
import sys

def load_postgres_settings():
    try:
        POSTGRES_USER = os.environ['POSTGRES_USER']
        POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
        return {
            'POSTGRES_USER': POSTGRES_USER,
            'POSTGRES_PASSWORD': POSTGRES_PASSWORD
        }
    except KeyError as e:
        sys.exit(1)
