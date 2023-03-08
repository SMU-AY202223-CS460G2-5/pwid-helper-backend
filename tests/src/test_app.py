from tests.data import rest
from tests.test_base import BaseTestCase


class TestHealthAPI(BaseTestCase):
    def test_health(self):
        response = self.client.get("/health")
        assert rest.MockResponse.HEALTH in response.data
