import csv
from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'CSV 파일에서 Product 데이터 불러오기'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='불러올 CSV 파일 경로')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                product, created = Product.objects.get_or_create(
                    product_name=row['product_name'],
                    defaults={
                        'promotion_tag': row.get('promotion_tag'),
                        'price': int(row.get('price') or 0),
                        'product_description': row.get('product_description'),
                        'tag': row.get('tag'),
                        'image_url': row.get('image_url'),
                        'label': row.get('label'),
                    }
                )
                count += 1 if created else 0
        self.stdout.write(self.style.SUCCESS(f'{count}개 상품이 성공적으로 추가되었습니다.'))
