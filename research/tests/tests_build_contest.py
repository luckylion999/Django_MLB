from django.test import TestCase
from django.contrib.auth.models import User, Group

from paksite.settings import DATABASES

# only change this for loaddata command.
DATABASES['default']['OPTIONS'] = {
   "init_command": "SET foreign_key_checks = 0;",
}
    
class BuildContestCase(TestCase):
    fixtures = ['contenttypes.json', 'test_users.json',]
      
    def test_build_contest(self):
        users = User.objects.all()
        for u in users:
            print u 