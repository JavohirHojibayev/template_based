# Django Template-Based Blog

Template asosida yozilgan oddiy blog loyihasi. Foydalanuvchilar ro'yxatdan o'tadi, post joylaydi, postlarga izoh qoldiradi. Yangi postlar admin tasdiqlagandan keyin bosh sahifada ko'rinadi.

## Imkoniyatlar

- Foydalanuvchi ro'yxatdan o'tish, login, logout
- Post qo'shish (`title`, `content`, `image`, `category`, `tags`)
- Postlarga izoh yozish
- Admin tasdiqlash (`is_approved`) va tavsiya (`recommended`)
- Bosh sahifada bo'limlar:
  - Eng yangi postlar
  - Eng ko'p ko'rilgan postlar
  - Haftaning ommabop postlari
  - Oyning ommabop postlari
  - Tavsiya qilingan postlar
- Parol maydonlari uchun ko'rsatish/yashirish (eye icon)

## Texnologiyalar

- Python 3.12 tavsiya etiladi
- Django 5.2.7
- Pillow 11.1.0
- SQLite3

## O'rnatish va ishga tushirish

```bash
cd template_based
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8020
```

Brauzerda oching:

- `http://127.0.0.1:8020/`

## Admin akkaunt (development)

Loyihada development uchun maxsus buyruq mavjud:

```bash
python manage.py setup_dev_admin
```

Natija:

- login: `admin`
- parol: `admin`

Admin panel: `http://127.0.0.1:8020/admin/`

## Test

```bash
python manage.py test blog
```

## Loyiha tuzilmasi

```text
template_based/
├─ blog/
├─ config/
├─ static/blog/
├─ media/
├─ db.sqlite3
├─ manage.py
└─ requirements.txt
```

## Eslatma

- Bu loyiha o'quv va development maqsadida tayyorlangan.
- Production uchun `DEBUG=False`, maxfiy kalitlar (`SECRET_KEY`) va xavfsizlik sozlamalarini alohida boshqarish kerak.
