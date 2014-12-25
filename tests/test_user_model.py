import unittest
import time
from datetime import datetime
from xtu import create_app, db
from xtu.models import User, AnonymousUser, Role, Permission

class test_roles_and_permissions(self):
    Role.insert_roles()
    u = User(email="john@example.com", password="cat")
    self.assertTrue(u.can(Permission.WRITE_ARTICLES))
    self.assertFalse(u.can(Permission.MODERATE_COMMENTS))


class test_anonymous_user(self):
    u = Anonymoususer()
    self.assertFalse(u.can(Permission.FOLLOW))