import requests


class TelegramBot:
    api_token = ""
    chat_id = ""
    name = ""

    def say(self, msg):
        requests.get(f'https://api.telegram.org/bot{self.api_token}/sendMessage', params=dict(
            chat_id=self.chat_id,
            text=f""" {self.name}, {msg} """
        ))
