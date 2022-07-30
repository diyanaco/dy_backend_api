import asyncio
import aiohttp
import random
import random
import string
import pytest

GLOBAL_ID = ""
ENDPOINT_MODEL_URL = "branch/"
BASE_URL = "http://127.0.0.1:5000/"
URL = BASE_URL + ENDPOINT_MODEL_URL
rand = random.randint(0, 10000)
letters = string.ascii_lowercase
randomFavSub = ""
randomFavSub.join(random.choice(letters) for i in range(10))

@pytest.mark.asyncio
async def test_post_branch():
    request_dict = {
        "name": "Form Test 123",
        "type": "tuition"
    }

    global GLOBAL_ID
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=request_dict) as response:
            if response.status == 200:
                data = await response.json()
                data_branch = data['data']
                data_branch_first = data_branch[0]
                GLOBAL_ID = data_branch_first['id']
                assert GLOBAL_ID, "GLOBAL_ID couldn't be created"
            else:
                data = await response.text()
                assert False, 'retrieve Failure response is text'

    for key, value in request_dict.items():
        assert value == data_branch_first[key], "create FAILURE key"


@pytest.mark.asyncio
async def test_get_branch():
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
async def test_put_branch():
    randomFavSub = ""
    randomFavSub = randomFavSub.join(random.choice(letters) for i in range(10))
    request_dict = {
        "name": "Guardian" + randomFavSub,
        "type": "tuition ++"
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
                data_branch = data['data']
                data_branch_first = data_branch[0]
            else:
                data = await response.text()
                assert False, "modify Failure response is text " + str(response.status)

    # TODO #38 Generalize the assert to all conditions
    for key, value in request_dict.items():
        assert (value == data_branch_first[key]), "modify FAILURE " + key


@pytest.mark.asyncio
async def test_delete_branch():
    async with aiohttp.ClientSession() as session:
        async with session.delete(URL + GLOBAL_ID) as response:
            if response.status == 200:
                data = await response.json()
                data_branch = data['data']
                data_branch_first = data_branch[0]
            else:
                data = response.text()
                assert False, "delete Failure response is text"

    assert data_branch_first['id'] == GLOBAL_ID, "remove FAILURE"

# Calling Functions
if __name__ == "__main__":
    asyncio.run(test_post_branch())
    asyncio.run(test_get_branch())
    asyncio.run(test_put_branch())
    asyncio.run(test_delete_branch())
