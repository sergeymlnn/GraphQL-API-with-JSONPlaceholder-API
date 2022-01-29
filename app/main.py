import graphene
from fastapi import FastAPI
from httpx import AsyncClient
from starlette_graphene3 import GraphQLApp, make_playground_handler, GraphQLError


class Geo(graphene.ObjectType):
  """Provides information about location of the place, where the user lives in"""
  lat = graphene.Float()
  lng = graphene.Float()


class Company(graphene.ObjectType):
  """Provides information about company in which the user works in"""
  name = graphene.String()
  catch_phrase = graphene.String()
  bs = graphene.String()


class Address(graphene.ObjectType):
  """Provides information about location, where the user lives at"""
  street = graphene.String()
  suite = graphene.String()
  city = graphene.String()
  zipcode = graphene.String()
  geo = graphene.Field(Geo)


class User(graphene.ObjectType):
  """Provides full information about user"""
  id = graphene.ID(required=True)
  name = graphene.String()
  username = graphene.String()
  email = graphene.String(required=True)
  address = graphene.Field(Address)
  phone = graphene.String()
  website = graphene.String()
  company = graphene.Field(Company)


class CompanyInput(graphene.InputObjectType):
  """Input fields to update information about company, where the user works in"""
  name = graphene.String(required=True)
  catch_phrase = graphene.String()
  bs = graphene.String()


class GeoInput(graphene.InputObjectType):
  """Input fields to update GEO location of the place, where the user lives in"""
  lat = graphene.Float(required=True)
  lng = graphene.Float(required=True)


class AddressInput(graphene.InputObjectType):
  """Input fields to updated general information about location, where the user lives in"""
  city = graphene.String(required=True)
  street = graphene.String(required=True)
  suite = graphene.String()
  zipcode = graphene.String()
  geo = graphene.InputField(GeoInput)


class CreateUserInput(graphene.InputObjectType):
  """Input fields to create a new user with the information about him/her"""
  name = graphene.String(required=True)
  username = graphene.String(required=True)
  email = graphene.String(required=True)
  phone = graphene.String()
  website = graphene.String()
  company = graphene.InputField(CompanyInput)
  address = graphene.InputField(AddressInput)


class UpdateUserInput(graphene.InputObjectType):
  """Input fields to update information about user"""
  name = graphene.String()
  username = graphene.String()
  email = graphene.String()
  phone = graphene.String()
  website = graphene.String()
  company = graphene.InputField(CompanyInput)
  address = graphene.InputField(AddressInput)


class CreateUser(graphene.Mutation):
  """Mutation to create a new user"""
  Output = User

  class Arguments:
    user = CreateUserInput(required=True)

  @staticmethod
  async def mutate(root, info, user):
    """Saves information about new user and returns the information itself"""
    async with AsyncClient() as client:
      response = await client.post(
        "https://jsonplaceholder.typicode.com/users",
        json=user,
        headers={"Content-type": "application/json; charset=UTF-8"}
      )
    return response.json()


class UpdateUser(graphene.Mutation):
  """Mutation to update information about specific user"""
  Output = User

  class Arguments:
    id = graphene.ID(required=True)
    user = UpdateUserInput()

  @staticmethod
  async def mutate(root, info, id, user):
    """Updates information about user, using id as identifier and returns the information itself"""
    async with AsyncClient() as client:
      response = await client.patch(
        f"https://jsonplaceholder.typicode.com/users/{id}",
        json=user,
        headers={"Content-type": "application/json; charset=UTF-8"}
      )
    return response.json()


class DeleteUser(graphene.Mutation):
  """Mutation to delete a specific user"""
  ok = graphene.Boolean()

  class Arguments:
    id = graphene.ID(required=True)

  @staticmethod
  async def mutate(root, info, id):
    """Deletes information about user, using id as identifier and returns a boolean response"""
    async with AsyncClient() as client:
      response = await client.delete(f"https://jsonplaceholder.typicode.com/users/{id}")
    ok = True if response.status_code == 200 else False
    return DeleteUser(ok=ok)



class Query(graphene.ObjectType):
  """Query to fetch information about one or all users from the API"""
  user = graphene.Field(User, id=graphene.String(required=True))
  users = graphene.List(User)

  @staticmethod
  async def resolve_users(root, info):
    """Fetches information about all users"""
    async with AsyncClient() as client:
      response = await client.get("https://jsonplaceholder.typicode.com/users")
    users = response.json()
    return users

  @staticmethod
  async def resolve_user(root, info, id):
    """Fetches information about specific user, using id to identify the user"""
    async with AsyncClient() as client:
      response = await client.get(f"https://jsonplaceholder.typicode.com/users/{id}")
    user = response.json()
    if not user:
      raise GraphQLError(f"User with id {id} not found")
    return user


class Mutations(graphene.ObjectType):
  """Collects and provides defined mutations to be available in the API"""
  create_user = CreateUser.Field()
  update_user = UpdateUser.Field()
  delete_user = DeleteUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
app = FastAPI()
graphql_app = GraphQLApp(schema, on_get=make_playground_handler())
app.mount("/graphql", graphql_app)
