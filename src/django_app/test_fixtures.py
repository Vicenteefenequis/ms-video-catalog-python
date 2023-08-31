import pytest


@pytest.fixture(params=[1, 2])
def num_seq(request):
    return request.param


@pytest.mark.parametrize('num', [1, 2])
def test_xpto1(num):
    assert 1 == num
