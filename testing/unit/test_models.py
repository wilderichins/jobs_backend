import pytest

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from mars.models import ( Job,
                          JobImage,
                          Review,
                          Dispute,
                          Category )

from testing.fixtures import ( review,
                               category,
                               child_category,
                               owner,
                               worker,
                               job,
                               dispute )

from testing.factories import ( CategoryFactory,
                                UserFactory,
                                JobFactory,
                                ReviewFactory,
                                DisputeFactory )

pytestmark = pytest.mark.django_db

def test_job(job, owner, worker, category):
    job_obj = JobFactory(**job)

    assert job_obj.owner.username == owner.get('username')
    assert job_obj.worker.username == worker.get('username')
    assert job_obj.post_time != None
    assert job_obj.assign_time == None
    assert job_obj.owner_review == None
    assert job_obj.worker_review == None
    assert job_obj.category.name == category.get('name')

def test_category(category, child_category):
    root_category = CategoryFactory(**category)

    assert root_category.name == category.get('name')
    assert root_category.parent == None

def test_child_category(child_category, category):
    sub_category = CategoryFactory(**child_category)

    assert sub_category.name == child_category.get('name')
    assert sub_category.parent.name == category.get('name')

def test_review():
    review = ReviewFactory()
    
    assert review.rating == None
    assert review.comment == None

invalid_ratings = [ (0), (6) ]
valid_ratings = range(1,6) 

@pytest.mark.parametrize("rating", invalid_ratings)
def test_review_invalid_rating(rating):
    with pytest.raises(ValidationError):
        review = ReviewFactory(rating=rating)
        review.full_clean()

@pytest.mark.parametrize("rating", valid_ratings)
def test_review_valid_ratings(rating):
    review = ReviewFactory(rating=rating)
    review.full_clean()
    assert review.rating == rating

valid_states = ['P', 'R', 'U']
@pytest.mark.parametrize("state", valid_states)
def test_dispute(dispute, job, state):
    dispute = DisputeFactory(**dispute)

    assert dispute.job.owner.username == job.get('owner').username
    assert dispute.state == 'N'

    dispute.state = state
    dispute.save()
    dispute.full_clean()

invalid_states = ['A', 'a', '1', 'W', 'Y', '123', 'PRU', '']
@pytest.mark.parametrize("state", invalid_states)
def test_dispute_invalid_states(dispute, state):
    dispute = DisputeFactory(**dispute)
    assert dispute.state == 'N'

    dispute.state = state
    dispute.save()

    with pytest.raises(ValidationError):
        dispute.full_clean()

user_pass_pairs = [ ('wilde0629', 'pass123'),
                    ('a+b_c-d', ')(*&^%$#@!'),
                    ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', '1234567890') ]
@pytest.mark.parametrize("username,password", user_pass_pairs)
def test_valid_users(username, password):
    user_info = {'username': username, 'password': password}
    user = UserFactory(**user_info)
    user.full_clean()

    assert username == user.username
    assert password == user.password


