#python startup.py

echo $FIREBASE_SERVICE_ACCOUNT > bandex_services_account.json
echo $APNS_PROD_KEY_CONTENT > apns_key.pem
python heroku_cache.py
gunicorn app:app --timeout 90
