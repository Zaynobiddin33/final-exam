from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    
    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    body = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True)
    banner = models.ImageField()

    # @property
    # def image(self):
    #     images = ProductImage.objects.filter(product = self)
    #     return images
    
    # def __str__(self) -> str:
    #     return f"{self.title} > {self.id}"
    
    

class ProductImage(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name='images')


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    is_active = models.BooleanField(default = True)

    @property
    def total_price(self):
        products = CartProduct.objects.filter(cart = self)
        price = 0
        for i in products:
            price += i.price
        return price
    


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, related_name = 'cart_products')
    quantity = models.IntegerField(default = 1)

    @property
    def price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    cart_product = models.ForeignKey(CartProduct, on_delete = models.DO_NOTHING)
    address = models.TextField()
    status = models.SmallIntegerField(choices =(
        (1,"pending"),
        (2,"sent"),
        (3,"recieved"),
        (4,"returned")
    ))
    