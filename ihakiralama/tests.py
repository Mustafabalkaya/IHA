from django.test import TestCase
from django.urls import reverse
from .models import CustomUser, UAV, Rent
from datetime import datetime, timedelta

class TestViews(TestCase):
    def setUp(self):
        # Test verilerini oluştur
        self.user = CustomUser.objects.create_user(username='test_user', password='test_password', phone='1234567890')
        self.uav = UAV.objects.create(uav_name='Test UAV', uav_brand='Brand', uav_model='Model', uav_weight=10.5, uav_range=100.0, uav_quantity=5, daily_rental_fee=50.0)
        self.rent = Rent.objects.create(user=self.user, uav=self.uav, date_start=datetime.now().date(), date_end=(datetime.now() + timedelta(days=3)).date(), total_fee=150.0)

    def test_get_uavs(self):
        response = self.client.post(reverse('get_uavs'), data={'search[value]': 'Test UAV'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test UAV')

    def test_getUavDetails(self):
        response = self.client.get(reverse('get_uav_details'), {'uav_id': self.uav.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test UAV')

    def test_get_users(self):
        response = self.client.post(reverse('get_users'), data={'search[value]': 'test_user'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_user')

    def test_get_uav_brands(self):
        response = self.client.get(reverse('get_uav_brands'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Brand')

    def test_get_uav_models(self):
        response = self.client.post(reverse('get_uav_models'), data={'brand': 'Brand'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Model')

    def test_search_uavs(self):
        response = self.client.post(reverse('search_uavs'), data={'brand': 'Brand', 'model': 'Model', 'start_date': datetime.now().date(), 'end_date': (datetime.now() + timedelta(days=3)).date()})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test UAV')

    def test_rent_uav(self):
        response = self.client.post(reverse('rent_uav'), data={'uav_id': self.uav.pk, 'date_start': datetime.now().date(), 'date_end': (datetime.now() + timedelta(days=3)).date()})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get('success'))

    def test_get_rents(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.post(reverse('get_rents'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test UAV')

    def test_get_all_rents(self):
        response = self.client.post(reverse('get_all_rents'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test UAV')
