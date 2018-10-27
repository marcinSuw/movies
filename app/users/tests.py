from django.test import TestCase


class MoviesBaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        pass
    def setUp(self):
        super().setUp()


class UserViewSetTestCase(MoviesBaseTestCase):
    pass
