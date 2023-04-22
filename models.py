from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self,username, email, password=None):
        """
    ایجاد کاربر با استفاده از نام کاربری و ایمیل و رمز عبور
        """
        if not username:
            raise ValueError("نام کاربری خود را وارد کنید")

        user = self.model(username=username, email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        ایجاد کاربر ادمین با استفاده از ایمیل و نام کاربری و رمز عبور
        """
        user = self.create_user(email=email, password=password, username=username)

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True, verbose_name='نام کاربری')
    email = models.EmailField( max_length=255, verbose_name="آدرس ایمیل")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_admin = models.BooleanField(default=False, verbose_name="ادمین")

    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "ایا کاربر مجوز خاصی دارد؟"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "ایا کاربر مجوز مشاهده برنامه برچسب برنامه را دارد؟"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "ایا کاربر عضو کارکنان است؟"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر ها"
