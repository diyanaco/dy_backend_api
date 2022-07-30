import asyncio
import aiohttp
import random
import global_fields
import random
import string
import pytest
import global_fields

GLOBAL_ID = ""
ENDPOINT_MODEL_URL = "subject/"
BASE_URL = "http://127.0.0.1:5000/"
URL = BASE_URL + ENDPOINT_MODEL_URL
rand = random.randint(0, 10000)
letters = string.ascii_lowercase
randomFavSub = ""
randomFavSub.join(random.choice(letters) for i in range(10))


@pytest.mark.asyncio
async def test_post_subject():
    request_dict = {
        "name": "Science"
    }

    global GLOBAL_ID
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=request_dict) as response:
            if response.status == 200:
                data = await response.json()
                data_subject = data['data']
                data_subject_first = data_subject[0]
                GLOBAL_ID = data_subject_first['id']
                global_fields.CROSS_SUBJECT_ID_1 = GLOBAL_ID
                assert GLOBAL_ID, "GLOBAL_ID couldn't be created"
            else:
                data = await response.text()
                assert False, 'retrieve Failure response is text'

    for key, value in request_dict.items():
        assert value == data_subject_first[key], "create FAILURE key"


@pytest.mark.asyncio
async def test_get_subject():
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
async def test_put_subject():
    randomFavSub = ""
    randomFavSub = randomFavSub.join(random.choice(letters) for i in range(10))
    request_dict = {
        "name": "Subject" + randomFavSub
    }
    headers = {
        'content-type': 'application/json',
        'Accepts': 'application/json'
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        print(GLOBAL_ID)
        print(request_dict)
        await asyncio.sleep(5)
        async with session.put(URL + GLOBAL_ID, json=request_dict) as response:
            print(response.status)
            if response.status == 200:
                data = await response.json()
                data_subject = data['data']
                data_subject_first = data_subject[0]
            else:
                data = await response.text()
                assert False, "modify Failure response is text " + \
                    str(response.status)

    # TODO #38 Generalize the assert to all conditions
    for key, value in request_dict.items():
        assert (value == data_subject_first[key]), "modify FAILURE " + key


@pytest.mark.asyncio
async def test_delete_subject():
    async with aiohttp.ClientSession() as session:
        async with session.delete(URL + GLOBAL_ID) as response:
            if response.status == 200:
                data = await response.json()
                data_subject = data['data']
                data_subject_first = data_subject[0]
            else:
                data = response.text()
                assert False, "delete Failure response is text"

    assert data_subject_first['id'] == GLOBAL_ID, "remove FAILURE"

@pytest.mark.asyncio
async def test_get_all_subject():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL + "all") as response:
            print("URl is '%s' " % (URL))
            if response.status == 200:
                data = await response.json()
                data_subject = data['data']
                totalRecords = len(data_subject)
                global_fields.CROSS_SUBJECT_ID_1 = data_subject[0]['id']
                #Last subject ID
                global_fields.CROSS_SUBJECT_ID_2 = data_subject[totalRecords - 1]['id']

            else:
                data = response.text()
                assert False, "getAll Failure response is text"

    assert totalRecords, "getAll FAILURE"

# Calling Functions
if __name__ == "__main__":
    # Need to retrieve the userID first
    # asyncio.run(test_post_user())
    asyncio.run(test_post_subject())
    asyncio.run(test_get_subject())
    asyncio.run(test_put_subject())
    asyncio.run(test_delete_subject())
    # asyncio.run(test_delete_user(global_fields.GLOBAL_USER_ID))
