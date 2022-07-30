import asyncio
import aiohttp
import random
import random
import string
import pytest

GLOBAL_ID = ""
ENDPOINT_MODEL_URL = "class/"
BASE_URL = "http://127.0.0.1:5000/"
URL = BASE_URL + ENDPOINT_MODEL_URL
rand = random.randint(0, 10000)
letters = string.ascii_lowercase
randomFavSub = ""
randomFavSub.join(random.choice(letters) for i in range(10))

@pytest.mark.asyncio
async def test_post_class():
    request_dict = {
        "name": "Class Test 123",
    }

    global GLOBAL_ID
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=request_dict) as response:
            if response.status == 200:
                data = await response.json()
                data_class = data['data']
                data_class_first = data_class[0]
                GLOBAL_ID = data_class_first['id']
                assert GLOBAL_ID, "GLOBAL_ID couldn't be created"
            else:
                data = await response.text()
                assert False, 'retrieve Failure response is text'

    for key, value in request_dict.items():
        assert value == data_class_first[key], "create FAILURE key" + key


@pytest.mark.asyncio
async def test_get_class():
    headers = {
        'content-type': 'application/json',
        'Accepts': 'application/json'
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(URL + GLOBAL_ID) as response:
            if response.status == 200:
                data = await response.json()
            else:
                data = await response.text()
                assert False, 'retrieve Failure response is text'

    assert data, "retrieve FAILURE"


@pytest.mark.asyncio
async def test_put_class():
    randomFavSub = ""
    randomFavSub = randomFavSub.join(random.choice(letters) for i in range(10))
    request_dict = {
        "name": "Guardian" + randomFavSub,
    }
    headers = {
        'content-type': 'application/json',
        'Accepts': 'application/json'
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        await asyncio.sleep(5)
        async with session.put(URL + GLOBAL_ID, json=request_dict) as response:
            if response.status == 200:
                data = await response.json()
                data_class = data['data']
                data_class_first = data_class[0]
            else:
                data = await response.text()
                assert False, "modify Failure response is text " + str(response.status)

    # TODO #38 Generalize the assert to all conditions
    for key, value in request_dict.items():
        assert (value == data_class_first[key]), "modify FAILURE " + key


@pytest.mark.asyncio
async def test_delete_class():
    async with aiohttp.ClientSession() as session:
        async with session.delete(URL + GLOBAL_ID) as response:
            if response.status == 200:
                data = await response.json()
                data_class = data['data']
                data_class_first = data_class[0]
            else:
                data = response.text()
                assert False, "delete Failure response is text"

    assert data_class_first['id'] == GLOBAL_ID, "remove FAILURE"

# Calling Functions
if __name__ == "__main__":
    asyncio.run(test_post_class())
    asyncio.run(test_get_class())
    asyncio.run(test_put_class())
    asyncio.run(test_delete_class())
