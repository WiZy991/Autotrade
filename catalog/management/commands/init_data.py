from django.core.management.base import BaseCommand
from catalog.models import Country, CarType


class Command(BaseCommand):
    help = 'Инициализация начальных данных: страны и типы кузова'

    def handle(self, *args, **options):
        # Создаем страны
        countries_data = [
            {
                'code': 'japan',
                'name': 'Япония',
                'description': 'Автомобили из Японии - это качество, надежность и передовые технологии. Мы предлагаем широкий выбор японских автомобилей различных марок.',
                'flag_emoji': '🇯🇵'
            },
            {
                'code': 'korea',
                'name': 'Корея',
                'description': 'Корейские автомобили сочетают в себе современный дизайн, отличное качество и доступные цены. Популярные марки: Hyundai, Kia, Genesis.',
                'flag_emoji': '🇰🇷'
            },
            {
                'code': 'china',
                'name': 'Китай',
                'description': 'Китайские автомобили - это отличное соотношение цены и качества. Мы предлагаем автомобили ведущих китайских производителей.',
                'flag_emoji': '🇨🇳'
            }
        ]

        for country_data in countries_data:
            country, created = Country.objects.get_or_create(
                code=country_data['code'],
                defaults=country_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана страна: {country.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Страна уже существует: {country.name}'))

        # Создаем типы кузова
        car_types = [
            'Седан',
            'Хэчбек',
            'Кроссовер',
            'Внедорожник',
            'Универсал',
            'Купе',
            'Кабриолет',
            'Минивэн',
            'Пикап',
            'Лифтбек'
        ]

        for type_name in car_types:
            slug = type_name.lower().replace('ё', 'e').replace(' ', '-')
            car_type, created = CarType.objects.get_or_create(
                slug=slug,
                defaults={'name': type_name}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан тип кузова: {car_type.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Тип кузова уже существует: {car_type.name}'))

        self.stdout.write(self.style.SUCCESS('Инициализация данных завершена!'))

