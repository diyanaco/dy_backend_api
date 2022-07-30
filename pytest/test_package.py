import asyncio
import aiohttp
import random
import random
import string
import pytest
import global_fields
from test_level import test_get_all_level
from test_package_set import test_get_all_package_set
from test_subject import test_get_all_subject

GLOBAL_ID = ""
ENDPOINT_MODEL_URL = "package/"
BASE_URL = "http://127.0.0.1:5000/"
URL = BASE_URL + ENDPOINT_MODEL_URL
rand = random.randint(0, 10000)
letters = string.ascii_lowercase
randomFavSub = ""
randomFavSub.join(random.choice(letters) for i in range(10))


@pytest.mark.asyncio
async def test_post_package():
    request_dict = {
        "name": "Class Test 123",
        "level_id": global_fields.CROSS_LEVEL_ID_1,
        "package_set_id": global_fields.CROSS_PACKAGE_SET_ID_1,
        "subject_id": global_fields.CROSS_SUBJECT_ID_1,
    }
    for i, j in request_dict.items():
        print("The key value are : '%s' and '%s'" % (i, j))
    global GLOBAL_ID
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=request_dict) as response:
            if response.status == 200:
                data = await response.json()
                data_package = data['data']
                data_package_first = data_package[0]
                GLOBAL_ID = data_package_first['id']
                assert GLOBAL_ID, "GLOBAL_ID couldn't be created"
            else:
                data = await response.text()
                assert False, 'retrieve Failure response is text'

    for key, value in request_dict.items():
        assert value == data_package_first[key], "create FAILURE key" + key


@pytest.mark.asyncio
async def test_get_package():
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
async def test_put_package():
    randomFavSub = ""
    randomFavSub = randomFavSub.join(random.choice(letters) for i in range(10))
    request_dict = {
        "name": "Guardian" + randomFavSub,
        "level_id": global_fields.CROSS_LEVEL_ID_2,
        "package_set_id":global_fields.CROSS_PACKAGE_SET_ID_2,
        "subject_id": global_fields.CROSS_SUBJECT_ID_2,
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
                data_package = data['data']
                data_package_first = data_package[0]
            else:
                data = await response.text()
                assert False, "modify Failure response is text " + \
                    str(response.status)

    # TODO #38 Generalize the assert to all conditions
    for key, value in request_dict.items():
        assert (value == data_package_first[key]), "modify FAILURE " + key


@pytest.mark.asyncio
async def test_delete_package():
    async with aiohttp.ClientSession() as session:
        async with session.delete(URL + GLOBAL_ID) as response:
            if response.status == 200:
                data = await response.json()
                data_package = data['data']
                data_package_first = data_package[0]
            else:
                data = response.text()
                assert False, "delete Failure response is text"

    assert data_package_first['id'] == GLOBAL_ID, "remove FAILURE"

# Calling Functions
if __name__ == "__main__":
    asyncio.run(test_get_all_level())
    asyncio.run(test_get_all_package_set())
    asyncio.run(test_get_all_subject())
    asyncio.run(test_post_package())
    asyncio.run(test_get_package())
    asyncio.run(test_put_package())
    asyncio.run(test_delete_package())
