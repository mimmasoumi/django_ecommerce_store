from django.core import paginator
from django.db.models.query_utils import Q
from shop.forms import CommentForm, ShippingForm
from shop.models import Brand, Category, Comments, Item, Order, OrderedItem, Shipping, Slider, SubCategory
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class IndexView(View):

    def get(self, request):
        products = Item.objects.order_by('-created')
        categories = Category.objects.all()
        slides = Slider.objects.all()
        product_view = Item.objects.order_by('-visit')

        context = {
            'products': products,
            'categories': categories,
            'slides': slides,
            'product_view': product_view

        }

        return render(request, 'index.html', context)


class DetailView(View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():

            content = form.cleaned_data['content']
            stars = form.cleaned_data['stars']
            item = Item.objects.get(pk=pk)
            stars_v = ''

            for i in range(int(stars)):
                stars_v += '<i class="fa fa-star"></i>'

            if int(stars) < 5:
                for i in range(int(5 - int(stars))):
                    stars_v += '<i class="fa fa-star-o empty"></i>'

            new_comment = Comments.objects.create(
                item=item,
                username=request.user,
                content=content,
                stars=stars_v,
            )

            return redirect(f'/detail/{pk}')
        return redirect(f'/detail/{pk}')

    def get(self, request, pk):
        product = get_object_or_404(Item, id=pk)
        product.visit += 1
        product.save()
        products = Item.objects.filter(
            category=product.category).exclude(id=product.id)
        comments = Comments.objects.filter(item=product)

        context = {
            'product': product,
            'products': products,
            'comments': comments,

        }

        return render(request, 'detail.html', context)


class RemoveSingleFromCart(LoginRequiredMixin, View):
    def get(self, request, slug):
        item = get_object_or_404(Item, slug=slug)

        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]

            if order.items.filter(item__slug=item.slug).exists():
                ordered_item = OrderedItem.objects.filter(
                    user=request.user,
                    item=item,
                )[0]
                if ordered_item.quantity > 1:
                    ordered_item.quantity -= 1
                    ordered_item.save()
                else:
                    order.items.remove(ordered_item)
                    ordered_item.delete()
                    if order.items.count() == 0:
                        order.delete()
                return redirect('shop:order_summary')

            else:
                return redirect('shop:order_summary')

        else:
            print('this item is not exist')


class RemoveFromCart(LoginRequiredMixin, View):
    def get(self, request, slug):
        item = get_object_or_404(Item, slug=slug)

        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]

            if order.items.filter(item__slug=item.slug).exists():
                ordered_item = OrderedItem.objects.filter(
                    user=request.user,
                    item=item,
                )[0]
                order.items.remove(ordered_item)
                ordered_item.delete()
                if order.items.count() == 0:
                    order.delete()
                return redirect('shop:order_summary')

            else:
                return redirect('shop:order_summary')

        else:
            print('this item is not exist')


class AddToCart(LoginRequiredMixin, View):
    def get(self, request, slug):

        item = get_object_or_404(Item, slug=slug)
        ordered_item, created = OrderedItem.objects.get_or_create(
            item=item,
            user=request.user,
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                ordered_item.quantity += 1
                ordered_item.save()
                return redirect("shop:order_summary")

            else:
                order.items.add(ordered_item)
                return redirect("shop:order_summary")
        else:
            order_date = timezone.now()
            order = Order.objects.create(
                user=request.user,
                ordered_date=order_date
            )
            order.items.add(ordered_item)

        return redirect("shop:order_summary")


class OrderSummary(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            orders = Order.objects.get(user=request.user, ordered=False)
        except:
            orders = None

        return render(request, 'order_summary.html', {'orders': orders})


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'checkout.html')

    def post(self, request):
        form = ShippingForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']

            shipping_address = Shipping.objects.create(
                user=request.user,
                firstname=firstname,
                lastname=lastname,
                address=address,
                phone=phone,
                city=city,
                zipcode=zipcode
            )
            order = Order.objects.get(user=request.user, ordered=False)
            order.shipping = shipping_address
            order.save()
            return redirect('shop:index')
        return redirect('shop:checkout')


class CategoryListView(View):
    def get(self, request, slug):
        category = Category.objects.all()
        sort = request.GET.get('sort')
        brand = request.GET.get('brand_name')
        page = request.GET.get('page')

        products = Item.objects.filter(category__slug=slug)

        if brand:
            if Brand.objects.get(title=brand):
                products = Item.objects.filter(
                    Q(brand__slug=brand) & Q(category__slug=slug))

        if sort:
            if sort == 'inc':
                products = products.order_by('-price')
            elif sort == 'dec':
                products = products.order_by('price')

        paginator = Paginator(products, 10)

        try:
            products = paginator.page(page)

        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        except PageNotAnInteger:
            products = paginator.page(1)

        return render(request, 'archive.html', {'products': products, 'page': page, 'categories': category})


class SearchView(View):
    def get(self, request):
        q = request.GET.get('q')
        category_id = request.GET.get('category')
        page = request.GET.get('page')

        if category_id == '0':
            products = Item.objects.filter(title__icontains = q)
        else:
            products = Item.objects.filter(category__id = category_id)
            products = products.filter(title__icontains = q)

        paginator = Paginator(products, 2)

        try:
            products = paginator.page(page)

        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        except PageNotAnInteger:
            products = paginator.page(1)
        return render(request, 'search.html', {'products': products, 'page': page, 'q':q, 'category_id':category_id})

