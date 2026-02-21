import mysql.connector
from flask import g, current_app
import logging

logger = logging.getLogger(__name__)

def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB'],
            port=current_app.config['MYSQL_PORT'],
            autocommit=True
        )

        except Exception as e:
            logger.error(f"Database error: {e}")
            return None
        return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db:
        db.close()

def init_db(app):
    app.teardown_appcontext(close_db)

def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    db = get_db()
    if not db:
        return None
    
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = cursor.rowcount
        
        if commit:
            db.commit()
            result = cursor.lastrowid or cursor.rowcount
        
        return result
    except Exception as e:
        logger.error(f"Query error: {e}")
        if commit:
            db.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
