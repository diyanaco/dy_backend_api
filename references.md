'''
first() will return none if there was no result.
one() will raise an error if the result was
print(user.__dict__)
api.add_resource(User, "/user/<string:first_name>")
'''

# Serializing json
json_object = json.dumps(result, indent = 4)
response = json.dumps(marshal_with(result,resource_fields))

# db url : to point to current directory of the db file
sqlite:///./nameOfdb.db

# sqlalchemy 
- to create index : Index is usually created to query data based on the index field or column
        simply supply 'index = True' in the column definition
        '''
        name = Column(String, unique=True, index=True)
        '''

# angular 
- Remove error of variables without initialization
        "strictPropertyInitialization": false