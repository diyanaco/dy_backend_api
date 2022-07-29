import global_fields
import requests
import asyncio
import aiohttp
import random
import pytest

GLOBAL_ID = ""
BASE_URL = "http://127.0.0.1:5000/"
ENDPOINT_MODEL_URL = "user/"
URL = BASE_URL + ENDPOINT_MODEL_URL

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
    global GLOBAL_ID 
    async with aiohttp.ClientSession() as session:
        async with session.post(URL + "signup", json=request_dict) as response:
            if response.status == 201:
                data = await response.json()
                data_user = data['user']
                #Here we dont retrieve the first array, because 
                #the user response is not an array
                GLOBAL_ID = data_user['id']
                # global_fields.GLOBAL_USER_ID = GLOBAL_ID
                assert GLOBAL_ID, "GLOBAL_ID does not exist"
            else :
                data = await response.text()
                assert False, 'retrieve Failure response is text'
    for key, value in request_dict.items():
        if key=="password":continue
        assert value == data_user[key], "create FAILURE key"

@pytest.mark.asyncio
async def test_get_user():
    headers = {
        'content-type': 'application/json',
        'Accepts': 'application/json'
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(URL + GLOBAL_ID) as response:
            if response.status == 200:
                data = await response.json()
            else :
                data = await response.text()
                assert False, 'retrieve Failure response is text'
    assert data, "retrieve FAILURE"

@pytest.mark.asyncio
async def test_put_user():
    request_dict = {
        "first_name": "Test User Diyana Updated",
        "last_name": "From Client Updated",
        "email": str(rand) + "@diyana.co",
        "password": "123"
    }
    headers = {
        'content-type': 'application/json',
        'Accepts': 'application/json'
    }
    # response = requests.put(BASE + "user/" + GLOBAL_ID, json=request_dict)
    async with aiohttp.ClientSession(headers = headers) as session:
        async with session.put(URL + GLOBAL_ID, json=request_dict) as response:
            if response.status == 200:
                data = await response.json()
                data_user = data['user']
                data_user_first = data_user[0]
            else :
                data = await response.text()
                assert False, "modify Failure response is text"

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
    async with aiohttp.ClientSession() as session:
        async with session.delete(URL + GLOBAL_ID ) as response:
            if response.status == 200:
                data = await response.json()
                data_user = data['user']
                data_user_first = data_user[0]
            else:
                data = response.text()
                assert False, "delete Failure response is text"
    
    assert data_user_first['id'] == GLOBAL_ID, "remove FAILURE"

# Calling Functions
if __name__ == "__main__":
    asyncio.run(test_post_user())
    asyncio.run(test_get_user())
    asyncio.run(test_put_user())
    asyncio.run(test_delete_user())

