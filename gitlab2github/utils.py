async def get(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        return {
            "code": response.status,
            "response": await response.json()
        }

async def post(session, url, headers=None, data=None, json=None):
    async with session.post(url, headers=headers, data=data, json=json) as response:
        return {
            "code": response.status,
            "response": await response.json()
        }