from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import ProfessionalProfile, Technology

class ProfessionalProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')

        self.profile = ProfessionalProfile.objects.create(
            fk_user=self.user,
            bio='Desarrolladora Backend',
            area='Desarrollo Web'
        )
        self.tech1 = Technology.objects.create(name='Python')
        self.tech2 = Technology.objects.create(name='Django')
        self.profile.technologies.set([self.tech1, self.tech2])

    def test_profile_creation(self):
        self.assertEqual(self.profile.fk_user.username, 'test_user')
        self.assertEqual(self.profile.bio, 'Desarrolladora Backend')
        self.assertEqual(self.profile.area, 'Desarrollo Web')
        self.assertEqual(self.profile.technologies.count(), 2)
