from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="adm1n_P@ss"
        )
        cls.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="dr1ver_P@ss",
            license_number="TES77587"
        )

        cls.search_manufacturer = Manufacturer.objects.create(
            name="search_car",
            country="search_country"
        )
        cls.filter_manufacturer = Manufacturer.objects.create(
            name="filter_car",
            country="filter_country"
        )

        cls.car_search_match = Car.objects.create(
            model="search_model",
            manufacturer=cls.search_manufacturer
        )
        cls.car_filter_match = Car.objects.create(
            model="filter_model",
            manufacturer=cls.filter_manufacturer
        )
        cls.car_no_match = Car.objects.create(
            model="no_match_model",
            manufacturer=cls.search_manufacturer
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.admin_user)

    def test_driver_license_number_listed(self):
        self.assertContains(
            self.client.get(
                reverse("admin:taxi_driver_changelist")
            ),
            self.driver.license_number
        )

    def test_driver_detail_license_number_listed(self):
        self.assertContains(
            self.client.get(
                reverse(
                    "admin:taxi_driver_change",
                    args=[self.driver.id]
                )
            ),
            self.driver.license_number
        )

    def test_driver_create_license_number_listed(self):
        self.assertContains(
            self.client.get(reverse("admin:taxi_driver_add")),
            "License number"
        )

    def test_search_by_model(self):
        response = self.client.get(
            reverse("admin:taxi_car_changelist"),
            {"q": "search"}
        )

        self.assertContains(response, self.car_search_match.model)
        self.assertNotContains(response, self.car_filter_match.model)
        self.assertNotContains(response, self.car_no_match.model)

    def test_filter_by_manufacturer(self):
        response = self.client.get(
            reverse("admin:taxi_car_changelist"),
            {"manufacturer__id__exact": self.filter_manufacturer.id}
        )

        self.assertContains(response, "Manufacturer")
        self.assertContains(response, self.car_filter_match.model)
        self.assertNotContains(response, self.car_search_match.model)
        self.assertNotContains(response, self.car_no_match.model)
