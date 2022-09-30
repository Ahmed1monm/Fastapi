from tortoise import Model, fields
from pydantic import BaseModel
from datetime import datetime


class User(Model):
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(unique=True, max_length=20, null=False)
    email = fields.CharField(unique=True, max_length=200, null=False)
    password = fields.CharField(max_length=100, null=False)
    is_verified = fields.BooleanField(default=False)
    join_data = fields.DateField(default=datetime.utcnow)


class Business(Model):
    id = fields.IntField(pk=True, index=True, )
    business_name = fields.CharField(max_length=20, null=False)
    City = fields.CharField(max_length=100, null=False, default="Unspecified")
    region = fields.CharField(max_length=100, null=False, default="Unspecified")
    business_description = fields.TextField(null=True)
    logo = fields.CharField(max_length=200, null=False, default="default.png")
    owner = fields.ForeignKeyField("models.User", related_name="business")


class Product(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=200, index=True, null=False)
    category = fields.CharField(max_length=30, index=True)
    original_price = fields.DecimalField(max_digits=12, decimal_places=2)
    now_price = fields.DecimalField(max_digits=12, decimal_places=2)
    percentage_discount = fields.IntField()
    offer_expiration_date = fields.DateField(default=datetime.utcnow)
    product_image = fields.CharField(max_length=200, null=False, default="productDefault.jpg")
    business = fields.ForeignKeyField("models.Business", related_name="products")
