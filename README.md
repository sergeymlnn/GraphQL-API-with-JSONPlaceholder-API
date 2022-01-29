### About

The project provides an example of how to integrate a simple GraphQL API using Python's library Graphene and widely knwon JSONPlaceholder API


### Installation

```
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip && python -m pip install -r requirements.txt
```

### Running API Server

```
uvicorn app.main:app --reload
```

### Open [PlayGround](http://127.0.0.1:8000/graphql)


### Usage

Get All Users
```
query GetUsers{
  users{
    name
    username
    email
    address { city street zipcode }
  }
}
```


Get One User:
```
query GetUser{
  user(id: "2"){
    id
    name
    email
    address { city geo { lat lng } }
    company{ name }
  }
}
```

Create User:
```
mutation CreateUser{
  createUser(user: {
    name: "John Smith",
    username: "johnsmith123",
    email: "johnsmith@example.com",
    company: {name: "Ubisoft", catchPhrase:"My Games"},
    address:{city: "London", street: "NC Av.34 b.19", geo: {lat: 92.18283, lng: -87.22}}
  }){
    id
    name
    username
    email
    address { city geo { lat lng } }
    company { name }
  }
}
```

Update User:
```
mutation UpdateUser{
  updateUser(id: "7", user:{
    email: "ervinhowell@example.com",
    address:{ city: "London" street: "H. Maria Av. 57.1"}
    company: {name: "Ubisoft"}
  }){
    email
    address { city }
    company { name }
    
  }
}
```

Delete User:
```
mutation DeleteUser{
  deleteUser(id: "1"){
    ok
  }
}
```

