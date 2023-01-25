import random
import string
from base64 import b64encode
from nacl import encoding, public

async def get(session, url, headers=None):
    """Send GET request"""
    async with session.get(url, headers=headers) as response:
        return {
            "code": response.status,
            "response": await response.json()
        }

async def post(session, url, headers=None, data=None, json=None):
    """Send POST requests"""
    async with session.post(url, headers=headers, data=data, json=json) as response:
        return {
            "code": response.status,
            "response": await response.json()
        }

async def make_request(method: str, session, url, headers=None, data=None, json=None) -> dict:
    """Send HTTP requests"""
    response = None
    if method.lower() == 'get':
        async with session.get(url, headers=headers) as response:
            return {
                "code": response.status,
                "response": await response.json()
            }
    elif method.lower() == 'post':
        async with session.post(url, headers=headers, data=data, json=json) as response:
            return {
                "code": response.status,
                "response": await response.json()
            }
    elif method.lower() == 'put':
        async with session.put(url, headers=headers, data=data, json=json) as response:
            return {
                "code": response.status,
                "response": await response.json() if response.status != 204 else await response.text()
            }
    else:
        return None

def encrypt(public_key: str ,secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")