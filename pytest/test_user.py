import pytest
import requests
import asyncio
import aiohttp
import random

GLOBAL_ID = ""

async def test_post_user():
    BASE = "http://127.0.0.1:5000/"
    rand = random.randint(0,10000)
    request_dict = {
        "first_name": "Test User Diyana1213",
        "last_name": "From Client1",
        "email": str(rand) + "@diyana.co",
        "password": "123"
    }
    # s = requests.Session()
    # response = s.post(BASE + "user/signup", json=request_dict)
    # print(response.json()['user'])
    global GLOBAL_ID 

    async with aiohttp.ClientSession() as session:
        async with session.post(BASE + "user/signup", json=request_dict) as response:
            data = await response.json()
            GLOBAL_ID = data['user']['id']
            print(GLOBAL_ID)

    assert GLOBAL_ID, "create FAILURE"
    #assert x == y , "test failed"


async def test_get_user():
    BASE = "http://127.0.0.1:5000/"
    # response = requests.get(BASE + "user/" + GLOBAL_ID)
    headers = {
        'content-type': 'application/json',
        'Accepts': 'application/json'
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        print(GLOBAL_ID)
        async with session.get(BASE + "user/" + GLOBAL_ID) as response:
            print(response.status)
            print(await response.text())
            data = await response.json()
            print(data)

    assert data, "retrieve FAILURE"
    #assert x == y , "test failed"


async def test_put_user():
    request_dict = {
        "first_name": "Test User Diyana Updated",
        "last_name": "From Client Updated",
        "email": "testuserdiyanaUPDATED@user.co",
        "password": "123"
    }
    BASE = "http://127.0.0.1:5000/"
    # response = requests.put(BASE + "user/" + GLOBAL_ID, json=request_dict)
    async with aiohttp.ClientSession() as session:
        async with session.put(BASE + "user/" + GLOBAL_ID, json=request_dict) as response:
            print(response.status)
            data = await response.json()
            print(data)
            data_user = data['user']
            print(data_user[0]['id'])

    # assert data['user'] == request_dict, "modify FAILURE"
    #TODO #38 Generalize the assert to all conditions
    assert (
            (data_user[0]['first_name'] == request_dict['first_name']) and
            (data_user[0]['last_name'] == request_dict['last_name'])
            ), "modify FAILURE"

async def test_delete_user():
    BASE = "http://127.0.0.1:5000/"
    # response = requests.delete(BASE + "user/" + GLOBAL_ID)
    async with aiohttp.ClientSession() as session:
        async with session.delete(BASE + "user/" + GLOBAL_ID) as response:
            data = await response.json()
    
    assert data, "remove FAILURE"


# Calling Functions
# test_post_user()
if __name__ == "__main__":
    asyncio.run(test_post_user())
    asyncio.run(test_get_user())
    asyncio.run(test_put_user())
    asyncio.run(test_delete_user())
    # asyncio.run(main())
# test_get_user()
# test_put_user()
# test_delete_user()

