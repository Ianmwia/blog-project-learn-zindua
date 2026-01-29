from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from products.models import Product 

class ProductViewSetTest(APITestCase):
    #create user for authentication
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_authenticate(user=self.user)
        
        # Create sample products
        self.p1 = Product.objects.create(name="Laptop", description="High end", price=1200, stock=10)
        self.p2 = Product.objects.create(name="Mouse", description="Wireless", price=25, stock=10)
        self.url = reverse('v1:products-list') # Assumes router name 'product'

    def test_list_products_authenticated(self):
        """Ensure we can list products when logged in."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify Pagination (page_size = 5)
        self.assertIn('results', response.data)

    def test_search_functionality(self):
        """Test the SearchFilter on name/description."""
        response = self.client.get(self.url, {'search': 'Laptop'})
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Laptop")

    def test_ordering_functionality(self):
        """Test OrderingFilter by price."""
        response = self.client.get(self.url, {'ordering': 'price'})
        # Mouse (25) should be first, Laptop (1200) second
        self.assertEqual(response.data['results'][0]['name'], "Mouse")

    def test_unauthenticated_access_denied(self):
        """Ensure IsAuthenticated permission works."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ExampleViewTests(APITestCase):
    def test_throttling_message(self):
        url = reverse('v1:example-view') # Update with your actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "This is a rate-limited view")
