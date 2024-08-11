from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class myUser(AbstractUser):
    mobile=models.CharField(max_length=12,verbose_name='Contact Number')
    def __str__(self):
        return self.first_name+" "+self.last_name
class Category(models.Model):
    c_id=models.AutoField(primary_key=True)
    c_name=models.CharField(max_length=50,verbose_name='Category Name')
    def __str__(self):
        return self.c_name
class Product(models.Model):
    p_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    author = models.CharField(max_length=100,null=True, blank=True)
    prev_price = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    image=models.ImageField(upload_to='products/')
    category=models.ForeignKey(Category,on_delete=models.CASCADE)   

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)
    user=models.ForeignKey(myUser,on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} * {self.product.name}'    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=255)
    payment_id=models.CharField(max_length=255)
    address=models.TextField()  
class Orderr(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=255)
    payment_id=models.CharField(max_length=255)
    address=models.TextField()         
    
