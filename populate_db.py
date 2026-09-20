import os
import sys
import django

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apex_project.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Product, Review
from decimal import Decimal

def seed():
    print("🌱 Начинаем наполнение базы данных APEX NUTRITION...")

    # 1. Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@apexnutrition.io', 'admin123')
        print("✅ Суперпользователь создан: логин 'admin', пароль 'admin123'")
    else:
        print("ℹ️ Суперпользователь 'admin' уже существует")

    # 2. Categories
    cat_protein, _ = Category.objects.get_or_create(
        slug='protein',
        defaults={
            'name': 'Протеины и Изоляты',
            'description': 'Максимальный анаболический отклик, ультра-микрофильтрация и чистейший белок.',
            'icon': 'zap'
        }
    )

    cat_gainers, _ = Category.objects.get_or_create(
        slug='gainers',
        defaults={
            'name': 'Гейнеры для набора массы',
            'description': 'Высококалорийные матрицы сложных углеводов и белков для взрывного роста массы.',
            'icon': 'flame'
        }
    )

    cat_energy, _ = Category.objects.get_or_create(
        slug='energy-preworkout',
        defaults={
            'name': 'Энергетики и Предтрены',
            'description': 'Предельный фокус, выносливость и чистая энергия без спадов.',
            'icon': 'battery-charging'
        }
    )

    cat_amino, _ = Category.objects.get_or_create(
        slug='amino-acids',
        defaults={
            'name': 'Аминокислоты и Памп',
            'description': 'Мощный пампинг, оксид азота и ускоренное восстановление мышечных волокон.',
            'icon': 'shield-check'
        }
    )

    # 3. Products
    products_data = [
        {
            'category': cat_protein,
            'title': 'Optimum Nutrition Gold Standard 100% Whey',
            'slug': 'gold-standard-100-whey',
            'tagline': "World's Best Selling Protein • Мировой эталон",
            'short_description': 'Золотой эталон среди сывороточных протеинов. 24 грамма ультрачистого изолята и концентрата сыворотки с непревзойденной растворимостью.',
            'full_description': 'Gold Standard 100% Whey от Optimum Nutrition — признанный мировой лидер чистоты и эффективности. В каждой мерной ложке содержится 24 грамма ультрафильтрованного сывороточного протеина и 5.5 грамм натуральных BCAA. Идеален для построения сухой мышечной массы и ускоренного восстановления после тяжелых силовых тренировок.',
            'price': Decimal('4990.00'),
            'old_price': Decimal('5890.00'),
            'image': 'products/on_gold_whey.jpg',
            'servings': '74 порции',
            'weight_volume': '2.27 кг',
            'flavor': 'Extreme Milk Chocolate',
            'rating': 5.0,
            'reviews_count': 312,
            'badge': 'ХИТ №1 В МИРЕ',
            'is_featured': True,
            'is_bestseller': True,
            'in_stock': True,
            'specs_json': {
                'Белок на порцию': '24 г',
                'BCAA': '5.5 г',
                'Глютамин и предшественники': '4.0 г',
                'Сахар': '1.0 г',
                'Калорийность': '120 ккал',
                'Степень очистки': 'WPI + WPC Microfiltration'
            }
        },
        {
            'category': cat_energy,
            'title': 'G FUEL Energy Formula (Grape Edition)',
            'slug': 'gfuel-energy-formula-grape',
            'tagline': 'Feel The Energy • Focus & Mental Reaction',
            'short_description': 'Легендарный энергетический комплекс с сочным вкусом спелого винограда. Взрывной ментальный фокус и чистая энергия без сахара и отката.',
            'full_description': 'G FUEL Energy Formula разработан для максимальной концентрации внимания, скорости реакции и взрывной выносливости. Ноль сахара, комплекс из 19 фруктовых антиоксидантов и мощная витаминная матрица. Подходит как для экстремальных тренировок, так и для длительных соревновательных сессий.',
            'price': Decimal('3890.00'),
            'old_price': Decimal('4490.00'),
            'image': 'products/gfuel_grape.jpg',
            'servings': '40 порций',
            'weight_volume': '280 г',
            'flavor': 'Juicy Concord Grape',
            'rating': 4.9,
            'reviews_count': 189,
            'badge': 'ЭНЕРГИЯ & ФОКУС',
            'is_featured': True,
            'is_bestseller': True,
            'in_stock': True,
            'specs_json': {
                'Кофеин безводный': '140 мг',
                'Комплекс антиоксидантов': '19 фруктовых экстрактов',
                'Сахар': '0 г',
                'Витамины': 'C + E + B6 + B12',
                'Калории': '15 ккал',
                'Время действия': '4-6 часов стабильной энергии'
            }
        },
        {
            'category': cat_amino,
            'title': 'GAT Sport L-Arginine Free Form Amino Acid',
            'slug': 'gat-sport-l-arginine',
            'tagline': 'Fuels Muscle Pumps • Nitric Oxide Booster',
            'short_description': 'Ультрачистый L-аргинин в свободной форме для мощного пампинга мышц, расширения сосудов и насыщения клеток питательными веществами.',
            'full_description': 'GAT Sport L-Arginine — это условно незаменимая аминокислота, являющаяся прямым предшественником оксида азота (NO). Повышает кровоток к работающим мышечным группам, создает эффект мощного венозного пампа и ускоряет доставку строительного белка в мышцы.',
            'price': Decimal('2690.00'),
            'old_price': Decimal('3190.00'),
            'image': 'products/gat_l_arginine.jpg',
            'servings': '180 капсул',
            'weight_volume': '180 таб.',
            'flavor': 'Pure Unflavored Caps',
            'rating': 4.9,
            'reviews_count': 94,
            'badge': 'MAX PUMP',
            'is_featured': False,
            'is_bestseller': True,
            'in_stock': True,
            'specs_json': {
                'L-Аргинин на порцию': '1000 мг',
                'Форма вещества': 'Free Form Amino Acid',
                'Эффект оксида азота': 'Повышение вазодилатации',
                'Количество в банке': '180 таблеток',
                'Сертификация': 'cGMP Verified'
            }
        },
        {
            'category': cat_gainers,
            'title': 'Cellucor COR-Performance High Protein Mass Gainer',
            'slug': 'cellucor-cor-gainer',
            'tagline': 'High Protein Mass Matrix • 60g Protein',
            'short_description': 'Высокобелковый гейнер для качественного набора плотной массы. 60г белка и 200г премиальных углеводов в каждой порции.',
            'full_description': 'Cellucor COR-Performance Gainer разработан для атлетов, стремящихся преодолеть тренировочное плато. Сочетает мультикомпонентную белковую матрицу, сложные углеводы с разной скоростью усвоения и полезные жиры для постоянного анаболического эффекта.',
            'price': Decimal('5490.00'),
            'old_price': Decimal('6200.00'),
            'image': 'products/cellucor_gainer.jpg',
            'servings': '16 мощных порций',
            'weight_volume': '2.3 кг',
            'flavor': 'Creamy Vanilla',
            'rating': 4.8,
            'reviews_count': 112,
            'badge': 'ВЗРЫВНОЙ НАБОР',
            'is_featured': True,
            'is_bestseller': False,
            'in_stock': True,
            'specs_json': {
                'Белок в порции': '60 г',
                'Углеводная матрица': '200 г',
                'Добавленные BCAA': '2.5 г',
                'Калорийность порции': '1050 ккал',
                'Глютен': '0% Gluten Free'
            }
        },
        {
            'category': cat_gainers,
            'title': 'MuscleTech Mass-Tech Elite Chocolate Fudge',
            'slug': 'muscletech-masstech-elite',
            'tagline': 'Scientifically Superior Musclebuilding Mass Gainer',
            'short_description': 'Научно разработанный гейнер элитного уровня с клинически выверенной дозой креатина и 80 граммами анаболического протеина.',
            'full_description': 'Mass-Tech Elite от MuscleTech содержит нутриенты высокой биологической ценности для гипертрофии мышечных волокон. Клинические испытания доказали значительное увеличение силовых показателей и чистой сухой массы за счет добавления микронизированного креатина.',
            'price': Decimal('6190.00'),
            'old_price': Decimal('7200.00'),
            'image': 'products/muscletech_masstech.jpg',
            'servings': '18 порций',
            'weight_volume': '3.18 кг',
            'flavor': 'Chocolate Fudge Cake',
            'rating': 5.0,
            'reviews_count': 176,
            'badge': 'ELITE FORMULA',
            'is_featured': False,
            'is_bestseller': True,
            'in_stock': True,
            'specs_json': {
                'Протеин': '80 г (на порцию с молоком)',
                'Креатин моногидрат HPLC': '10 г',
                'BCAA': '17 г',
                'Калорийность': '1000 ккал',
                'Про-аминокислотный комплекс': '156 г'
            }
        },
        {
            'category': cat_protein,
            'title': 'Smart Way Vegan Plant Protein BPI Sports',
            'slug': 'smart-way-vegan-protein',
            'tagline': '100% Natural Vegetable Protein • Essential Aminos',
            'short_description': 'Чистейший растительный протеин со сбалансированным аминокислотным профилем, железом и цинком. Легкое усвоение без вздутия.',
            'full_description': 'Smart Way Vegan Protein изготовлен из отборных растительных источников (гороховый и рисовый изоляты). Обладает нежнейшим шоколадным вкусом, не содержит искусственных подсластителей, лактозы и глютена. Идеален для веганов и людей с чувствительным пищеварением.',
            'price': Decimal('3490.00'),
            'old_price': Decimal('3990.00'),
            'image': 'products/vegan_protein.jpg',
            'servings': '25 порций',
            'weight_volume': '1.0 кг',
            'flavor': 'Natural Dark Chocolate',
            'rating': 4.9,
            'reviews_count': 88,
            'badge': '100% VEGAN',
            'is_featured': False,
            'is_bestseller': False,
            'in_stock': True,
            'specs_json': {
                'Растительный белок': '20 г на порцию',
                'Сахар и лактоза': '0 г',
                'Глютен и соя': 'Полностью отсутствуют',
                'Микроэлементы': 'Обогащен Iron + Zinc',
                'Биодоступность': '98% Fermented Matrix'
            }
        },
    ]

    for pdata in products_data:
        prod, created = Product.objects.update_or_create(
            slug=pdata['slug'],
            defaults=pdata
        )
        status = "Создан" if created else "Обновлен"
        print(f"  📦 {status}: {prod.title}")

    # 4. Reviews
    reviews_data = [
        {
            'author': 'Александр Громов',
            'role_or_city': 'Мастер спорта по пауэрлифтингу, Москва',
            'rating': 5,
            'text': 'Заказываю Gold Standard Whey уже третий раз. Качество 100% оригинальное, проверял по батч-коду. Доставка в постамат за 1 день. Растворимость в шейкере идеальная, вкус шоколада лучший на рынке!',
            'avatar_text': 'АГ'
        },
        {
            'author': 'Дмитрий Волков',
            'role_or_city': 'Фитнес-тренер WorldClass, СПб',
            'rating': 5,
            'text': 'Mass-Tech Elite дал отличный скачок по силовым и весу уже за первый месяц цикла. Никаких проблем с ЖКТ, чистый результат. Рекомендую своим клиентам.',
            'avatar_text': 'ДВ'
        },
        {
            'author': 'Екатерина Соловьева',
            'role_or_city': 'Кроссфит атлет, Казань',
            'rating': 5,
            'text': 'G-Fuel с виноградом — просто пушка для утренних кардио и функциональных тренировок! Нет тахикардии, голова кристально чистая, бодрость держится стабильно 5 часов.',
            'avatar_text': 'ЕС'
        },
        {
            'author': 'Максим Решетников',
            'role_or_city': 'Бодибилдинг Men’s Physique, Екатеринбург',
            'rating': 5,
            'text': 'L-Arginine от GAT дает сумасшедший памп на тренировках груди и рук! Вены проявляются уже со второго подхода. Отдельный респект магазину за премиальный сервис и быструю отправку.',
            'avatar_text': 'МР'
        }
    ]

    for rdata in reviews_data:
        Review.objects.get_or_create(
            author=rdata['author'],
            defaults=rdata
        )

    print("🎉 База данных успешно наполнена товарами, категориями и отзывами!")

if __name__ == '__main__':
    seed()
