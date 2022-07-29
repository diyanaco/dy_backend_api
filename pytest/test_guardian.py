import asyncio
import aiohttp
import random
import random
import string
import pytest

GLOBAL_ID = ""
ENDPOINT_MODEL_URL = "guardian/"
BASE_URL = "http://127.0.0.1:5000/"
URL = BASE_URL + ENDPOINT_MODEL_URL
rand = random.randint(0, 10000)
letters = string.ascii_lowercase
randomFavSub = ""
randomFavSub.join(random.choice(letters) for i in range(10))

@pytest.mark.asyncio
async def test_post_guardian():
    request_dict = {
        "primary_user_id": "012dc0bb-46ff-493f-9374-cf075292091a",
        "secondary_user_id": "02f78ea3-f9c2-4036-8d63-d9ae172a02de"
    }

    global GLOBAL_ID
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=request_dict) as response:
            if response.status == 200:
                data = await response.json()
                data_guardian = data['guardian']
                data_guardian_first = data_guardian[0]
                GLOBAL_ID = data_guardian_first['id']
                assert GLOBAL_ID, "GLOBAL_ID couldn't be created"
            else:
                data = await response.text()
                assert False, 'retrieve Failure response is text'

    for key, value in request_dict.items():
        assert value == data_guardian_first[key], "create FAILURE key"


@pytest.mark.asyncio
async def test_get_guardian():
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
async def test_put_guardian():
    randomFavSub = ""
    randomFavSub = randomFavSub.join(random.choice(letters) for i in range(10))
    request_dict = {
        "primary_user_id": "0610076a-40c9-4cc1-bf19-88ec491478c4",
        "secondary_user_id": "062fbc08-0092-420a-886c-c1b0b97dcc2a"
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
                data_guardian = data['guardian']
                data_guardian_first = data_guardian[0]
            else:
                data = await response.text()
                assert False, "modify Failure response is text " + str(response.status)

    # TODO #38 Generalize the assert to all conditions
    for key, value in request_dict.items():
        assert (value == data_guardian_first[key]), "modify FAILURE " + key


@pytest.mark.asyncio
async def test_delete_guardian():
    async with aiohttp.ClientSession() as session:
        async with session.delete(URL + GLOBAL_ID) as response:
            if response.status == 200:
                data = await response.json()
                data_guardian = data['guardian']
                data_guardian_first = data_guardian[0]
            else:
                data = response.text()
                assert False, "delete Failure response is text"

    assert data_guardian_first['id'] == GLOBAL_ID, "remove FAILURE"

# Calling Functions
if __name__ == "__main__":
    asyncio.run(test_post_guardian())
    asyncio.run(test_get_guardian())
    asyncio.run(test_put_guardian())
    asyncio.run(test_delete_guardian())
