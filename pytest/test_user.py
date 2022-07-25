import global_fields
import requests
import asyncio
import aiohttp
import random
import pytest

GLOBAL_ID = ""
BASE = "http://127.0.0.1:5000/"
rand = random.randint(0,10000)
#TODO #40 Fixe on test put for pytest
@pytest.mark.asyncio
async def test_post_user():
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
            data_user = data['user']
            print(data['user'])
            GLOBAL_ID = data_user['id']
            global_fields.GLOBAL_USER_ID = GLOBAL_ID
            assert GLOBAL_ID, "GLOBAL_ID does not exist"
    for key, value in request_dict.items():
        if key=="password":continue
        assert value == data_user[key], "create FAILURE key"

    #assert x == y , "test failed"

@pytest.mark.asyncio
async def test_get_user():
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

@pytest.mark.asyncio
async def test_put_user():
    request_dict = {
        "first_name": "Test User Diyana Updated",
        "last_name": "From Client Updated",
        "email": str(rand) + "@diyana.co",
        "password": "123"
    }
    # response = requests.put(BASE + "user/" + GLOBAL_ID, json=request_dict)
    async with aiohttp.ClientSession() as session:
        async with session.put(BASE + "user/" + GLOBAL_ID, json=request_dict) as response:
            print(response.status)
            data = await response.json()
            print(data)
            data_user = data['user']
            data_user_first = data_user[0]
            print(data_user_first['id'])

    # assert data['user'] == request_dict, "modify FAILURE"
    #TODO #38 Generalize the assert to all conditions
    for key, value in request_dict.items():
        if key == "password" : continue
        #If assert false, return string
        assert (value == data_user_first[key]), "modify FAILURE " + key
    # assert (
    #         (data_user[0]['first_name'] == request_dict['first_name']) and
    #         (data_user[0]['last_name'] == request_dict['last_name'])
    #         ), "modify FAILURE"

@pytest.mark.asyncio
async def test_delete_user():
    # response = requests.delete(BASE + "user/" + GLOBAL_ID)
    # if global_id_optional : id = global_id_optional
    # else : id = GLOBAL_ID
    async with aiohttp.ClientSession() as session:
        async with session.delete(BASE + "user/"  + GLOBAL_ID ) as response:
            data = await response.json()
            data_user = data['user']
            data_user_first = data_user[0]
    
    assert data_user_first['id'] == GLOBAL_ID, "remove FAILURE"

# Calling Functions
if __name__ == "__main__":
    asyncio.run(test_post_user())
    asyncio.run(test_get_user())
    asyncio.run(test_put_user())
    asyncio.run(test_delete_user())

