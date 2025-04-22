import csv
from django.core.management.base import BaseCommand
from products.models import Product, Tag, PromotionTag, Label

class Command(BaseCommand):
    help = "CSV 파일로부터 Product 데이터 import"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        success_count = 0
        error_count = 0

        with open(csv_file, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    # 필수 필드 체크
                    if not row['product_name'].strip():
                        continue

                    product = Product.objects.create(
                        product_name=row['product_name'],
                        price=int(row['price']),
                        product_description=row['product_description'],
                        image_url=row['image_url']
                    )

                    # --- Tag 처리 ---
                    tag_list = [t.strip() for t in row['tag'].split(",") if t.strip()]
                    for tag_name in tag_list:
                        tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                        product.tags.add(tag_obj)

                    # --- PromotionTag 처리 ---
                    if row['promotion_tag'].strip():
                        promo_tags = [t.strip() for t in row['promotion_tag'].split(",") if t.strip()]
                        for promo_name in promo_tags:
                            promo_obj, _ = PromotionTag.objects.get_or_create(name=promo_name)
                            product.promotion_tags.add(promo_obj)

                    # --- Label 처리 ---
                    if row['label'].strip():
                        label_list = [l.strip() for l in row['label'].split(",") if l.strip()]
                        for label_name in label_list:
                            label_obj, _ = Label.objects.get_or_create(name=label_name)
                            product.labels.add(label_obj)

                    success_count += 1

                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(
                        f"[❌ ERROR] '{row.get('product_name', 'Unknown')}' → {e}"
                    ))

        self.stdout.write(self.style.SUCCESS(f"✅ 성공: {success_count}개"))
        if error_count:
            self.stdout.write(self.style.WARNING(f"⚠️ 실패: {error_count}개"))
