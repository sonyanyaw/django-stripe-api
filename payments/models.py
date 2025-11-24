from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255, help_text='Product name')
    description = models.TextField(blank=True, help_text='Product description')
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text='Product price')
    currency = models.CharField(max_length=3, default='usd', help_text='Product currency')

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item, help_text='Order items')
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, help_text='Discount')
    tax = models.ForeignKey('Tax', on_delete=models.SET_NULL, null=True, help_text='Tax')


    def total_price(self):
        total = sum(item.price for item in self.items.all())

        if self.discount:
            total = total * (1 - self.discount.discount_percentage / 100)

        if self.tax:
            total = total * (1 + self.tax.tax_percentage / 100)

        return "{:.2f}".format(total)
    
    def currency(self):
        first_item = self.items.first()
        print(first_item)
        return first_item.currency if first_item else "usd"



class Discount(models.Model):
    name = models.CharField(max_length=255, help_text='Discount name')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=0, default=0, help_text='Discount percentage')

    stripe_id_eur = models.CharField(max_length=255, blank=True, help_text='ID купона в Stripe EUR')
    stripe_id_usd = models.CharField(max_length=255, blank=True, help_text='ID купона в Stripe USD')

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=255, help_text='Tax name')
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=0, default=0, help_text='Tax percentage')

    stripe_id_eur = models.CharField(max_length=255, blank=True, help_text='Stripe Tax Rate ID EUR')
    stripe_id_usd = models.CharField(max_length=255, blank=True, help_text='Stripe Tax Rate ID USD')

    def __str__(self):
        return self.name