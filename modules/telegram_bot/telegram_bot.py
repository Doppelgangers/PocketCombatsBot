import requests


class TelegramBot:

    def __init__(self, api_token: str, chat_id: int, name: str):
        self.api_token = api_token
        self.chat_id = chat_id
        self.name = name

    def say(self, msg: str):
        requests.get(f'https://api.telegram.org/bot{self.api_token}/sendMessage', params=dict(
            chat_id=self.chat_id,
            text=f"""{self.name}, {msg}."""
        ))
