from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, account_type, password=None, first_name=None, last_name=None):
        # Creates and saves a User with the given email and password.
        if not email:
            raise ValueError('Users must have an email address')

        first_name = '' if first_name is None else first_name

        last_name = '' if last_name is None else last_name

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.account_type = account_type
        user.first_name = first_name
        user.last_name = last_name
        user.save(using=self._db)

        return user

    def create_staffuser(self, email, password, first_name=None, last_name=None):
        # Creates a non super admin

        user = self.create_user(
            email,
            password=password,
            account_type=3,
            first_name=first_name,
            last_name=last_name
        )
        user.staff = True
        user.verified = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name=None, last_name=None):
        # Creates and saves a superuser with the given email and password.
        user = self.create_user(
            email,
            password=password,
            account_type=3,
            first_name=first_name,
            last_name=last_name
        )
        user.staff = True
        user.admin = True
        user.verified = True
        user.save(using=self._db)
        return user
