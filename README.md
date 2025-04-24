# 🛠️ CU 상품 API Django 서버

CU(씨유) 상품 정보를 저장하고 **필터·검색·가격 범위** 기능이 있는 REST API를 제공합니다.

| 기능 | 엔드포인트 | 설명 |
|------|------------|------|
| **상품 목록 (페이지네이션)** | `GET /api/products/` | `search`, `price_min`, `price_max`, `tags__name`, `labels__name`, `promotion_tags__name` 필터 지원.<br>응답에 `min_price`, `max_price` 포함 |
| **상품 목록 (전체)** | `GET /api/products/all/` | 동일 필터 파라미터 지원, 페이지네이션 없음 |
| **태그 목록** | `GET /api/tags/` | 전체 태그 1 000건 반환 |
| **라벨 목록** | `GET /api/labels/` | 전체 라벨 반환 |
| **프로모션 태그 목록** | `GET /api/promotion-tags/` | 전체 프로모션 태그 반환 |
| **CSV 일괄 로드** | `python manage.py import_csv <file>.csv` | 태그·라벨·프로모션 태그까지 함께 생성·연결 |

---

## 📦 기술 스택

- Python 3.11
- Django 5.x
- **Django REST Framework**
- **django‑filter**
- SQLite (개발 DB)

---

## 📁 프로젝트 구조

```text
<project_root>/               # Django 프로젝트 루트
├── manage.py                  # Django 관리 커맨드 진입점
├── csv_files/                 # 샘플 CSV 데이터 저장소
├── cu_backend/                # 프로젝트 설정 및 환경 파일
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── products/                  # 메인 앱: 모델, 뷰, 시리얼라이저, 커맨드
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py             # Product / Tag / Label / PromotionTag
    ├── serializers.py        # DRF 시리얼라이저
    ├── views.py              # APIView + 전체/페이지네이션 뷰
    ├── urls.py               # /api/... 라우팅
    ├── management/
    │   └── commands/
    │       └── import_csv.py  # CSV → DB 로드
    └── migrations/           # 마이그레이션 파일들
        ├── 0001_initial.py
        ├── 0002_remove_product_launch_date.py
        ├── 0003_label_promotiontag_tag.py
        ├── 0004_remove_product_label_remove_product.py
        └── __init__.py
```

---

## 🚀 빠른 시작

```bash
# 1) 가상환경 준비
python -m venv venv
source venv/bin/activate            # Windows: .\venv\Scripts\activate

# 2) 패키지 설치
pip install -r requirements.txt     # Django, DRF, django-filter 포함

# 3) 마이그레이션 실행
python manage.py migrate

# 4) CSV 데이터 로드
python manage.py import_csv csv_files/cu_products_v0.2.csv

# 5) 개발 서버 실행
python manage.py runserver
```

---

## 🌐 API 사용 예

| 목적 | 호출 예시 |
|------|-----------|
| 1천~2천원 & ‘샌드위치’ 태그 | `/api/products/?price_min=1000&price_max=2000&tags__name=샌드위치` |
| 모든 상품(전체) | `/api/products/all/` |
| 키워드 검색 (치즈) | `/api/products/?search=치즈` |

### 페이지네이션 응답 예 (`/api/products/`)

```json
{
  "count": 9393,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "min_price": 60,
  "max_price": 109000,
  "results": [
    {
      "id": 1,
      "product_name": "샌)크래프트더블치즈샌드",
      "price": 2700,
      "product_description": "...",
      "image_url": "...jpg",
      "tags": [ { "name": "샌드위치" }, { "name": "간편식사" } ],
      "labels": [ { "name": "New" } ],
      "promotion_tags": []
    }
  ]
}
```

### 전체 응답 예 (`/api/products/all/`)

```json
[
  {
    "id": 1,
    "product_name": "샌)크래프트더블치즈샌드",
    "price": 2700,
    "product_description": "..."
  },
  ...
]
```

---

## 📄 CSV 포맷

| 헤더 | 설명 | 필수 |
|------|------|------|
| `product_name` | 상품명 | ✅ |
| `price` | 정가(원) | ✅ |
| `product_description` | 설명 |  |
| `image_url` | 썸네일 URL |  |
| `tag` | 쉼표(,) 구분 다중 태그 |  |
| `promotion_tag` | 쉼표 구분 다중 |  |
| `label` | 쉼표 구분 다중 |  |

> **TIP** : UTF‑8 BOM 파일은 `utf-8-sig` 로 자동 처리.

예시:

```csv
product_name,price,product_description,tag,image_url,promotion_tag,label
딸기우유,1800,상큼한 딸기맛 우유,음료,https://img...jpg,1+1,1+1
```

---

## 🔧 추가 설정

- `TIME_ZONE = 'Asia/Seoul'`
- `REST_FRAMEWORK.DEFAULT_RENDERER_CLASSES` 에서 `BrowsableAPIRenderer` 삭제 → JSON only
- 대량 요청 시 클라이언트가 `page_size` 쿼리 파라미터로 페이지 크기 지정 가능 (최대 100)

---

## 📖 Swagger UI 사용

Swagger UI는 API를 시각화하고 문서를 탐색하며 요청을 직접 실행해 볼 수 있는 웹 인터페이스입니다. 기본 경로는 다음과 같습니다:

- **Swagger UI 접속**: `http://localhost:8000/swagger/`

### 주요 사용법

1. **엔드포인트 목록 확인**  
   상단의 드롭다운 메뉴 또는 페이지 좌측의 탐색 패널에서 제공되는 모든 API 엔드포인트를 확인할 수 있습니다.

2. **파라미터 입력**  
   각 엔드포인트를 클릭하면 요청 가능한 메서드(GET, POST 등)와 입력 가능한 쿼리 파라미터, 요청 바디 예시가 표시됩니다.  
   - `Try it out` 버튼을 클릭하여 입력 필드를 활성화합니다.  
   - 필요한 값을 입력하거나 선택합니다.

3. **요청 실행**  
   입력이 완료되면 `Execute` 버튼을 눌러 실제 API 요청을 전송할 수 있습니다.

4. **응답 확인**  
   요청을 실행하면  
   - **요청 URL**  
   - **요청 헤더 및 바디**  
   - **응답 상태 코드** (예: 200 OK)  
   - **응답 헤더**  
   - **응답 바디** (JSON 포맷)  
   등을 한눈에 확인할 수 있습니다.

5. **코드 생성**  
   요청 섹션에서 **`Code`** 버튼을 클릭하면 cURL, Python, JavaScript 등 다양한 언어의 예제 코드를 복사할 수 있습니다.

6. **ReDoc 인터페이스**  
   대안 문서 뷰가 필요하면 `http://localhost:8000/redoc/`에 접속해 ReDoc 스타일의 문서를 이용할 수 있습니다.

---

## 🧪 간단 테스트

```bash
# 가격 3000원 이하 & 'New' 라벨
curl 'http://localhost:8000/api/products/?price_max=3000&labels__name=New'

# 전체 상품 JSON 다운로드
curl 'http://localhost:8000/api/products/all/' -o products.json
```

👍 문제나 개선사항이 있으면 Issue 등록 부탁드립니다.

