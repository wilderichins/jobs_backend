import pytest

from testing.factories import ( UserFactory,
                                CategoryFactory,
                                JobFactory )

@pytest.fixture
def review():
    return { 'rating': 5,
             'comment': 'Great work!' }

@pytest.fixture
def category():
    return { 'name': 'root category' }

@pytest.fixture
def child_category(category):
    return { 'name': 'child category',
             'parent': CategoryFactory(**category) }

@pytest.fixture
def owner():
    return { 'username': 'test owner',
             'password': 'owner_password',
             'email': 'owner@test.com',
             'first_name': 'OwnerFirst',
             'last_name': 'OwnerLast' }

@pytest.fixture
def worker():
    return { 'username': 'test worker',
             'password': 'worker_password',
             'email': 'owner@test.com',
             'first_name': 'WorkerFirst',
             'last_name': 'WorkerLast' }

@pytest.fixture
def job(owner, worker, category):
    return { 'owner': UserFactory(**owner),
             'worker': UserFactory(**worker),
             'category': CategoryFactory(**category) }

@pytest.fixture
def dispute(job):
    return { 'job': JobFactory(**job) }
