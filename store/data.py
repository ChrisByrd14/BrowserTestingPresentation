from datetime import datetime
from decimal import Decimal

import peewee


db = peewee.SqliteDatabase("store.db")


class __BaseModel(peewee.Model):
    class Meta:
        database = db

    id = peewee.PrimaryKeyField()
    created = peewee.DateTimeField(default=datetime.now)
    updated = peewee.DateTimeField(null=True)
    deleted = peewee.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.id:
            # this record has already been saved to the DB, so we must be updating
            self.updated = datetime.now()
        super().save(*args, **kwargs)


class Product(__BaseModel):
    name = peewee.CharField()
    slug = peewee.CharField()
    description = peewee.TextField()
    purchase_price = peewee.DecimalField(max_digits=9)
    sale_price = peewee.DecimalField(max_digits=9)
    on_hand = peewee.IntegerField()


class Cart(__BaseModel):
    session_id = peewee.CharField(unique=True)


class CartItem(__BaseModel):
    cart = peewee.ForeignKeyField(Cart, backref="items")
    product_id = peewee.ForeignKeyField(Product, backref="carts")
    quantity = peewee.IntegerField()


db.connect()
db.create_tables([Product, Cart, CartItem], safe=True)


def get_cart_items(session_id: str | None, **kwargs) -> list[CartItem]:
    if not session_id:
        return []

    return list(Cart.get(session_id=session_id).items)
