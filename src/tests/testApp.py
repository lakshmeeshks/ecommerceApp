from unittest import TestCase
from ..app import  app,User, signup,login,dashboard,logout

class TestAppClass(TestCase):
    """ Test App CLass"""

    def test_add_user(self):
        user = User()
