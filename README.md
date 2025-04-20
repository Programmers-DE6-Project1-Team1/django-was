# 🛠️ Django API 서버 (CU 상품 데이터)

CU 상품 정보를 저장하고, 필터링 가능한 REST API로 제공하는 Django 백엔드 서버입니다.

## 📦 기술 스택

- Django 5.x
- Django REST Framework
- django-filter
- SQLite (개발용 DB)

## 📁 주요 파일 구성

```
django-was/
├── manage.py
├── cu_backend/             # 프로젝트 설정
└── products/               # 상품 모델/뷰/API
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── serializers.py
    └── migrations/
```

## 🚀 실행 방법

### 1. 가상환경 및 설치

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> `requirements.txt`는 `django`, `djangorestframework`, `django-filter` 포함

### 2. 마이그레이션 및 실행

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 테스트 데이터 import (CSV)

```bash
python manage.py import_csv sample_products.csv
```

## 🌐 API 예시

```
GET /api/products/
GET /api/products/?price_min=1000&price_max=2000
GET /api/products/?label=1+1
```

> 응답은 JSON으로 제공됩니다 (`DEFAULT_RENDERER_CLASSES` 설정 적용)

## 📄 API 응답 예시

```json
[
  {
    "product_name": "딸기우유",
    "promotion_tag": "1+1",
    "price": 1800,
    "product_description": "상큼한 딸기맛 우유",
    "tag": "음료",
    "image_url": "https://cu.bgfretail.com/images/strawberry.jpg",
    "label": "1+1"
  }
]
```

## 🔒 기타 설정

- KST 시간 기준 적용 (`TIME_ZONE = 'Asia/Seoul'`)
- `BrowsableAPIRenderer` 제거 → 기본 응답은 JSON

## 📄 샘플 CSV 구조

```csv
product_name,promotion_tag,price,product_description,tag,image_url,label
딸기우유,1+1,1800,상큼한 딸기맛 우유,음료,https://...jpg,1+1
```

## 🧪 테스트 커맨드

```bash
curl http://localhost:8000/api/products/?price_min=1500
```

---

