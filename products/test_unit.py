from unittest import TestCase
from products.views import ProductsViewSet, ProductPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

#structure view as is since we testing it

class ProductViewUnitTest(TestCase):
    def test_viewset_config(self):
        view = ProductsViewSet()
        self.assertIn(IsAuthenticated, view.permission_classes)
        self.assertEqual(view.pagination_class, ProductPagination)
        self.assertIn(UserRateThrottle, view.throttle_classes)

    def test_pagination_page_size(self):
        paginator = ProductPagination
        self.assertEqual(paginator.page_size, 5)


