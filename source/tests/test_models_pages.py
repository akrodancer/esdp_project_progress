from django.test import TestCase
from pages.models import PageModel, CarouselMainModel, CarouselSponsorsModel, CarouselReviewsModel, CarouselAdvantagesModel
from pages.page_choice import PageChoices


class PageModelTest(TestCase):
    def test_create_page(self):
        page = PageModel.objects.create(title='Test Page', path=PageChoices.HOME)
        self.assertEqual(PageModel.objects.count(), 1)
        self.assertEqual(page.path, PageChoices.HOME)


class CarouselMainModelTest(TestCase):
    def setUp(self):
        self.page = PageModel.objects.create(title='Test Page', path=PageChoices.HOME)

    def test_create_carousel_main(self):
        carousel_main = CarouselMainModel.objects.create(page=self.page, image='image.jpg')
        self.assertEqual(CarouselMainModel.objects.count(), 1)
        self.assertEqual(carousel_main.page, self.page)


class CarouselSponsorsModelTest(TestCase):
    def setUp(self):
        self.page = PageModel.objects.create(title='Test Page', path=PageChoices.HOME)

    def test_create_carousel_sponsors(self):
        carousel_sponsors = CarouselSponsorsModel.objects.create(page=self.page, image='image.jpg')
        self.assertEqual(CarouselSponsorsModel.objects.count(), 1)
        self.assertEqual(carousel_sponsors.page, self.page)


class CarouselReviewsModelTest(TestCase):
    def setUp(self):
        self.page = PageModel.objects.create(title='Test Page', path=PageChoices.HOME)

    def test_create_carousel_reviews(self):
        carousel_reviews = CarouselReviewsModel.objects.create(name='John Doe', review='Great!', image='image.jpg')
        self.assertEqual(CarouselReviewsModel.objects.count(), 1)
        self.assertEqual(carousel_reviews.name, 'John Doe')


class CarouselAdvantagesModelTest(TestCase):
    def setUp(self):
        self.page = PageModel.objects.create(title='Test Page', path=PageChoices.HOME)

    def test_create_carousel_advantages(self):
        carousel_advantages = CarouselAdvantagesModel.objects.create(page=self.page, text='Some text')
        self.assertEqual(CarouselAdvantagesModel.objects.count(), 1)
        self.assertEqual(carousel_advantages.text, 'Some text')
