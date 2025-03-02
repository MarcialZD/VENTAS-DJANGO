from django.test import TestCase

# Create your tests here.
from shop.models import Category, Product

class CategoryModelTest(TestCase):
    def setUp(self):
        Category.objects.create(name='test category')
        Product.objects.create(name='test product', price=10, description='test description', category=Category.objects.get(name='test category'))
        Product.objects.create(name='test product 2', price=10, description='test description', category=Category.objects.get(name='test category'))
    def test_product_category_id(self):
        product = Product.objects.get(name='test product')
        self.assertEqual(product.category.id, 1)
    def test_object_name_is_name(self):
        category = Category.objects.get(id=1)
        expected_object_name = f'Category {category.name}'
        self.assertEqual(expected_object_name, str(category))
    def test_total_products(self):
        category = Category.objects.get(id=1)
        self.assertEqual(category.products.count(), 2)

class ProductModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Pantalones')
        Product.objects.create(name='Pantalon1', price=10, description='Pantalon de mezclilla', category=category)
        Product.objects.create(name='Pantalon2', price=20, description='Pantalon de mezclla', category=category)
        Product.objects.create(name='Pantalon3', price=30, description='Pantalonilla', category=category)
    def test_product_list_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_product_list_view_queryset(self):
        response = self.client.get('/')
        self.assertEqual(len(response.context['products']), 3)
    def test_product_list_view_tittle(self):
        response = self.client.get('/')
        self.assertContains(response, '<h1>Productos</h1>')