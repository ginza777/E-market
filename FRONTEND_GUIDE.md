# E-commerce Store - Frontend Access Guide

## 🚀 Loyiha Muvaffaqiyatli Ishga Tushirildi!

### 📍 Kirish Manzillari

#### 🌐 Frontend (Asosiy Sahifa)
- **URL**: http://localhost:8001/
- **Tavsif**: To'liq frontend interfeysi, qidiruv, filterlar, mahsulotlar

#### 🔧 Admin Panel
- **URL**: http://localhost:8001/admin/
- **Email**: `admin@example.com`
- **Parol**: `123`
- **Tavsif**: Django Jazzmin bilan kuchaytirilgan admin panel

#### 📚 API Hujjatlari
- **Swagger UI**: http://localhost:8001/swagger/
- **ReDoc**: http://localhost:8001/redoc/
- **JSON Schema**: http://localhost:8001/swagger.json
- **YAML Schema**: http://localhost:8001/swagger.yaml

#### 🔍 Elasticsearch
- **URL**: http://localhost:9200/
- **Tavsif**: Qidiruv tizimi

#### 📊 Kibana
- **URL**: http://localhost:5601/
- **Tavsif**: Elasticsearch ma'lumotlarini tahlil qilish

### 🎯 Frontend Xususiyatlari

#### ✅ Qidiruv Tizimi
- **Mahsulotlar bo'yicha qidiruv**: Asosiy sahifada qidiruv paneli
- **Kategoriya bo'yicha filter**: Dropdown orqali kategoriya tanlash
- **Real-time qidiruv**: JavaScript orqali tez qidiruv
- **Elasticsearch integratsiyasi**: Kuchli qidiruv algoritmi

#### ✅ Filterlar
- **Narx oralig'i**: Min va max narx
- **Kategoriya**: Barcha kategoriyalar
- **Zaxira holati**: Mavjud, kam zaxira, tugagan
- **Saralash**: Yangi, eski, narx, nom bo'yicha

#### ✅ Mahsulotlar Ko'rsatish
- **Responsive dizayn**: Barcha qurilmalarda ishlaydi
- **Mahsulot kartasi**: Rasm, nom, narx, zaxira
- **Modal oynalar**: Batafsil ma'lumot
- **Savatga qo'shish**: Login qilgan foydalanuvchilar uchun

#### ✅ Autentifikatsiya
- **Ro'yxatdan o'tish**: Yangi foydalanuvchi yaratish
- **Kirish**: Email va parol bilan
- **Profil**: Foydalanuvchi ma'lumotlari
- **Chiqish**: Xavfsiz chiqish

### 🛠️ Texnik Xususiyatlar

#### Frontend Texnologiyalari
- **HTML5**: Semantik markup
- **CSS3**: Zamonaviy dizayn, animatsiyalar
- **Bootstrap 5**: Responsive framework
- **JavaScript**: Interaktiv funksionallik
- **jQuery**: DOM manipulyatsiya

#### Backend Texnologiyalari
- **Django 5.2**: Web framework
- **Django REST Framework**: API
- **PostgreSQL**: Ma'lumotlar bazasi
- **Elasticsearch**: Qidiruv tizimi
- **JWT**: Autentifikatsiya
- **Docker**: Konteynerizatsiya

### 📱 Responsive Dizayn

#### Desktop (1200px+)
- 4 ustunli mahsulotlar grid
- To'liq navigatsiya menyusi
- Keng qidiruv paneli

#### Tablet (768px - 1199px)
- 3 ustunli mahsulotlar grid
- Collapsible navigatsiya
- O'rta qidiruv paneli

#### Mobile (767px va undan kichik)
- 2 ustunli mahsulotlar grid
- Hamburger menyu
- Kichik qidiruv paneli

### 🎨 Dizayn Xususiyatlari

#### Ranglar
- **Asosiy**: Gradient blue-purple
- **Muvaffaqiyat**: Yashil
- **Xavf**: Qizil
- **Ogohlantirish**: Sariq
- **Ma'lumot**: Ko'k

#### Animatsiyalar
- **Hover effektlari**: Kartalar uchun
- **Loading spinner**: Yuklanish paytida
- **Toast notifications**: Xabarlar uchun
- **Smooth transitions**: Yumshoq o'tishlar

### 🔧 Rivojlantirish

#### Static Fayllar
```
static/
├── css/
│   └── style.css          # Asosiy CSS
├── js/
│   └── main.js            # Asosiy JavaScript
└── images/
    ├── no-image.png       # Placeholder rasm
    └── no-category.png    # Placeholder kategoriya
```

#### Templates
```
templates/
└── frontend/
    ├── base.html          # Asosiy template
    └── home.html          # Bosh sahifa
```

### 🚀 Keyingi Qadamlar

1. **Mahsulot rasmlari qo'shish**: Real rasmlar bilan
2. **Savat funksiyasi**: To'liq savat tizimi
3. **Buyurtma tizimi**: Checkout jarayoni
4. **To'lov integratsiyasi**: Payment gateway
5. **Email xabarlar**: Buyurtma tasdiqlari
6. **Push notifications**: Yangi mahsulotlar haqida

### 📞 Yordam

Agar muammo bo'lsa:
1. Docker konteynerlarni qayta ishga tushiring: `docker-compose restart`
2. Loglarni tekshiring: `docker-compose logs web`
3. Ma'lumotlar bazasini tekshiring: `docker-compose exec web python manage.py shell`

---

**🎉 Tabriklaymiz! Sizning e-commerce loyihangiz to'liq ishlamoqda!**
