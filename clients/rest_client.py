import hikari

class DiscordRestClient:
    def __init__(self, token: str):
        self.token = token
        self.client = hikari.RESTApp()

    async def print_my_user(self):
        async with self.client.acquire(self.token) as client:
            my_user = await client.fetch_my_user()
            print(my_user)