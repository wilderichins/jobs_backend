import factory

from django.contrib.auth.models import User
from mars.models import ( Job,
                          JobImage,
                          Review,
                          Dispute,
                          Category )

class JobFactory(factory.DjangoModelFactory):
    class Meta:
        model = Job

class JobImageFactory(factory.DjangoModelFactory):
    class Meta:
        model = JobImage

class ReviewFactory(factory.DjangoModelFactory):
    class Meta:
        model = Review

class DisputeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Dispute

class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category

class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
