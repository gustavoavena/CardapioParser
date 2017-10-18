python startup.py

python heroku_cache.py
gunicorn app:app --timeout 90
