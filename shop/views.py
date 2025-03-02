from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

from shop.models import *
from shop.utils import get_cart
from django import forms



#nuevo
from django.views.generic import ListView, DetailView
#

#nuevo
from django.views.generic.edit import CreateView

#nuevo
from shop.forms import CartAddProductForm


#antigua vista de product list
# def product_list(request):
#     categories = Category.objects.all()
#     products = Product.objects.all()
#     context = {
#         'categories': categories,
#         'products': products
#     }
#     return render(request, 'shop/product/list.html', context)

class ProductList(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'


#antiguo product detail
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context = {
#         'product': product
#     }
#     return render(request, 'shop/product/detail.html', context)


class ProductDetail(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        return context




#antiguo product create
# def product_create(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         price = request.POST.get('price')
#         category = request.POST.get('category')
#         category = Category.objects.get(id=category)
#         product = Product.objects.create(
#             name=name,
#             description=description,
#             price=price,
#             category=category
#         )
#         return redirect('shop:product-detail', pk=product.id)

#     context = {
#         'categories': Category.objects.all()
#     }
#     return render(request, 'shop/product/form.html', context)


#nuevo
class ProductForm(forms.ModelForm):
    #short_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3,'class':'form-control'}),required=False)
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category','image']

    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #     if Product.objects.filter(name=name).exists():
    #         raise forms.ValidationError('El producto ya existe')
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Product.objects.filter(name=name).exists():
            raise forms.ValidationError('El producto ya existe')
        return name


#nuevo product create
class ProductCreate(CreateView):  
    model = Product
    #fields = ['name', 'description', 'price', 'category']
    form_class = ProductForm
    template_name = 'shop/product/form.html'
    success_url = '/'
   
    def form_invalid(self, form):
        print("POST data:", self.request.POST)
        print("Form errors:", form.errors.as_data())
        return super().form_invalid(form)










# Shopping Cart Views

def cart_detail(request):
    cart = get_cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'shop/cart/detail.html', context)

def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_cart(request)
    quantity = request.POST.get('quantity')
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += int(quantity)
        cart_item.save()
    return redirect('shop:cart-detail')

def cart_remove(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return redirect('shop:cart-detail')

def cart_update(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    quantity = request.POST.get('quantity')
    cart_item.quantity = quantity
    cart_item.save()
    return redirect('shop:cart-detail')