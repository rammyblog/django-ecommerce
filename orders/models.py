from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from accounts.models import UserProfile
from django.contrib.auth.models import User


class Order(models.Model):
    first_name= models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=254)
    address=models.CharField(max_length=200,)
    postal_code=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created=models.DateField(auto_now_add=True)
    updated=models.BooleanField(default=False)
    paid=models.BooleanField(default=False)
    braintree_id=models.CharField(max_length=150, blank=True)
    coupon=models.ForeignKey(Coupon, related_name='orders',
                            null=True,
                            blank=True,
                            on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                    validators=[MinValueValidator(0),
                                                MaxValueValidator(100)])
    class Meta:
        ordering = ('-created',)
    
    # def __str__(self):
    #     return 'Order {}'.format(str(self.id))
    
    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost *(self.discount/Decimal('100'))

class OrderItem(models.Model):
    order = models.ForeignKey(Order, 
                    related_name='items',
                     on_delete=models.CASCADE)

    product = models.ForeignKey(Product, 
                    related_name='order_items',
                     on_delete=models.CASCADE)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    # def __str__(self):
    #     return self.id

    def get_cost(self):
        return self.price * self.quantity


