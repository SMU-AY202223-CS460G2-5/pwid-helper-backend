from unittest import mock

from tests.data import rest
from tests.test_base import BaseTestCase


class TestHealthAPI(BaseTestCase):
    def test_health(self) -> None:
        response = self.client.get("/health")
        assert rest.MockResponse.HEALTH in response.data
        assert response.status_code == 200


class TestWebhookAPI(BaseTestCase):
    @mock.patch("src.telegram.TelegramApiWrapper.send_message")
    def test_start_command(self, mock_send_message: mock.Mock) -> None:
        mock_send_message.return_value = rest.MockResponse.START_COMMAND
        response = self.client.post(
            "/webhook",
            json=rest.MockRequests.START_COMMAND,
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 200
