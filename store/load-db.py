from random import choice

from faker import Faker

from data import db, Product


fake = Faker()

if __name__ == '__main__':
    on_hand_range = list(range(1000))
    price_range = list(range(50, 59999, 1))  # pennies
    with db.atomic():
        for _ in range(50):
            name = fake.bs()
            purchase_price = choice(price_range) / 100
            Product.create(
                name=name,
                slug=fake.slug(name),
                description='\n'.join(fake.paragraphs(choice(range(2, 4)))),
                purchase_price=f'{purchase_price:0.2f}',
                sale_price=f'{purchase_price * 1.75:0.2f}',
                on_hand=choice(on_hand_range)
            )
        db.commit()
