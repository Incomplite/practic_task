from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Building
from django.contrib.gis.geos import Polygon

class BuildingTests(APITestCase):
    def setUp(self):
        self.valid_polygon1 = Polygon(((0, 0), (1, 0), (1, 1), (0, 1), (0, 0)))
        self.valid_polygon2 = Polygon(((0, 0), (3, 0), (2, 2), (0, 2), (0, 0)))
        self.valid_polygon3 = Polygon(((2, 2), (3, 2), (3, 3), (2, 3), (2, 2)))
        self.valid_polygon4 = Polygon(((5, 5), (6, 5), (6, 6), (5, 6), (5, 5)))
        Building.objects.create(geom=self.valid_polygon1, address="Valid Building 1")
        Building.objects.create(geom=self.valid_polygon2, address="Valid Building 2")
        Building.objects.create(geom=self.valid_polygon3, address="Valid Building 3")
        Building.objects.create(geom=self.valid_polygon4, address="Valid Building 4")

    def test_create_valid_building(self):
        url = reverse('building-list')
        data = {'geom': self.valid_polygon1.geojson, 'address': "New Building"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_building(self):
        invalid_polygon = Polygon(((0, 0), (1, 1), (1, 0), (0, 1), (0, 0)))
        url = reverse('building-list')
        data = {'geom': invalid_polygon.geojson, 'address': "Invalid Building"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_building_by_area(self):
        url = reverse('building-list') + '?min_area=1.0&max_area=1.0'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 3)

        url = reverse('building-list') + '?min_area=2.0'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 1)

    def test_filter_building_by_distance(self):
        # Координаты (1, 1) с радиусом 100000 метров (100 км)
        url = reverse('building-list') + '?longitude=1&latitude=1&max_distance=100000'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 2)

        # Координаты (5, 5) с радиусом 500000 метров (500 км)
        url = reverse('building-list') + '?longitude=5&latitude=5&max_distance=500000'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 3)