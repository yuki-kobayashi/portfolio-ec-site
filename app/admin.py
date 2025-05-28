from django.contrib import admin
from .models import Item, OrderItem, Order, Payment, CarouselItem, CarouselTitle, Favorite

admin.site.register(Item)
admin.site.register(CarouselTitle)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Favorite)