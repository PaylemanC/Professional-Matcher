from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import ProfessionalProfile, CareerItem
from datetime import date

class CareerItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.profile = ProfessionalProfile.objects.create(fk_user=self.user)

        self.career_item = CareerItem.objects.create(
            fk_profile=self.profile,
            item_type='education',
            title='Licenciatura en Sistemas',
            description='Estudios universitarios',
            institution='UBA (Universidad de Buenos Aires, Argentina)',
            start_date=date(2018, 3, 1),
            end_date=date(2022, 12, 1)
        )

    def test_career_item_creation(self):
        self.assertEqual(self.career_item.fk_profile, self.profile)
        self.assertEqual(self.career_item.item_type, 'education')
        self.assertEqual(self.career_item.title, 'Licenciatura en Sistemas')

    def test_get_end_date_display(self):
        self.assertEqual(self.career_item.get_end_date_display(), "December 2022")

    def test_get_end_date_display_present(self):
        self.career_item.end_date = None
        self.career_item.save()
        self.assertEqual(self.career_item.get_end_date_display(), "Actualidad")
