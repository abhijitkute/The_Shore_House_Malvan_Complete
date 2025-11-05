The Shore House Malvan - Complete Django starter

Run:
1. python -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py createsuperuser
7. python manage.py runserver

Notes:
- Set EMAIL_HOST_PASSWORD in environment or in settings.py before using email.
- Replace {VPA} in payment QR payload via admin or directly editing Payment.qr_payload.
