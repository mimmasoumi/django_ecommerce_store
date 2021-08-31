from shop.models import Brand, Category, Comments, FeedFile, Item, ItemDetails, Order, OrderedItem, Shipping, Slider, SubCategory
from django.contrib import admin


admin.site.register(Item)
admin.site.register(Category)
admin.site.register(FeedFile)
admin.site.register(ItemDetails)
admin.site.register(SubCategory)
admin.site.register(OrderedItem)
admin.site.register(Comments)
admin.site.register(Order)
admin.site.register(Shipping)
admin.site.register(Slider)
admin.site.register(Brand)
