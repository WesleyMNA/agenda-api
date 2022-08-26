from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self,
                    email,
                    username,
                    name,
                    genre,
                    phone_number,
                    password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not name:
            raise ValueError('Users must have a name')
        if not genre:
            raise ValueError('Users must have a genre')
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
            genre=genre,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         email,
                         username,
                         name,
                         genre,
                         phone_number,
                         password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            name=name,
            genre=genre,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create your models here.
class User(AbstractBaseUser):
    class Genre(models.TextChoices):
        MASCULINE = 'M'
        FEMININE = 'F'

    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    birthday = models.DateField(
        blank=True,
        null=True
    )
    genre = models.CharField(
        max_length=1,
        choices=Genre.choices
    )
    phone_number = models.CharField(max_length=20, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username', 'genre', 'phone_number']

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(
        blank=True,
        null=True
    )
    initial_date = models.DateTimeField()
    final_date = models.DateTimeField(
        blank=True,
        null=True
    )
    all_day = models.BooleanField(
        default=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
