from shop.models import Category, Order
from django import template

register = template.Library()


@register.filter('shop_split')
# this filter split array to given number
def shop_split(value, args):
    args_int = int(args)
    return value[:args_int]


@register.inclusion_tag('inc/cart.html', takes_context=True)
def cart(context):
    request = context['request']

    try:
        orders = Order.objects.get(user=request.user, ordered=False)
    except:
        orders = None

    return {'orders': orders, 'request': request}

@register.inclusion_tag('inc/login_nav.html', takes_context=True)
def login(context):
    request = context['request']
    return {'request': request}

@register.inclusion_tag('inc/search.html')
def search():
    categories = Category.objects.all()

    return {'categories': categories}
