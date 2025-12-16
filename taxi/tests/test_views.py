from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")

CAR_DETAIL_URL = reverse(
    "taxi:car-detail",
    kwargs={"pk": 1}
)
DRIVER_DETAIL_URL = reverse(
    "taxi:driver-detail",
    kwargs={"pk": 1}
)


class PublicPagesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

        cls.car = Car.objects.create(
            model="test_model",
            manufacturer=cls.manufacturer
        )

        cls.driver = get_user_model().objects.create_user(
            username="test",
            password="t5st_P@ss",
            first_name="testus",
            last_name="testenko",
            license_number="TES77587"
        )

    def test_login_required_index(self):
        self.assertNotEqual(
            self.client.get(INDEX_URL).status_code, 200
        )

    def test_login_required_manufacturer(self):
        self.assertNotEqual(
            self.client.get(MANUFACTURER_LIST_URL).status_code, 200
        )

    def test_login_required_car(self):
        self.assertNotEqual(
            self.client.get(CAR_LIST_URL).status_code, 200
        )

    def test_login_required_driver(self):
        self.assertNotEqual(
            self.client.get(DRIVER_LIST_URL).status_code, 200
        )

    def test_login_required_car_detail(self):
        self.assertNotEqual(
            self.client.get(CAR_DETAIL_URL).status_code, 200
        )

    def test_login_required_driver_detail(self):
        self.assertNotEqual(
            self.client.get(DRIVER_DETAIL_URL).status_code, 200
        )

