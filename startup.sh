python startup.py

#echo $FIREBASE_SERVICE_ACCOUNT > bandex_services_account.json

python heroku_cache.py
gunicorn app:app --timeout 90
