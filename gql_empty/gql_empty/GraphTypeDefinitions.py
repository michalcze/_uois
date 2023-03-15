from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
import datetime

def AsyncSessionFromInfo(info):
    return info.context['session']

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
#
# priklad rozsireni UserGQLModel
#
from gql_empty.GraphResolvers import resolve_theses_model_by_id, resolve_theses_model_page
@strawberryA.federation.type(keys=["id"], description="""Entity containing theses""")
class ThesesGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolve_theses_model_by_id (AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition
        return result
    
    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID: #ID je atribut z tabulky!
        return self.id
    
    @strawberryA.field(description="""name""")
    def id(self) -> str: 
        return self.name
    
    @strawberryA.field(description="""date""")
    def id(self) -> datetime.datetime: 
        return self.date
    
    @strawberryA.field(description="""assignment name""")
    def id(self) -> str: 
        return self.assignment_name
    
    @strawberryA.field(description="""assignment desctiption""")
    def id(self) -> str: 
        return self.assignment_description
    
    @strawberryA.field(description="""assignment goals""")
    def id(self) -> str: 
        return self.assignment_goals
    
    @strawberryA.field(description="""author id""")
    def id(self) -> strawberryA.id: #Nejspis spatne
        return self.author_id
    
    @strawberryA.field(description="""last change""")
    def id(self) -> datetime.datetime: 
        return self.lastchange
    
    
#tam kde je userID vracet userGQL model, stejně u roletypeID

@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id) # jestlize rozsirujete, musi byt tento vyraz

@strawberryA.federation.type(extend=False, keys=["id"])


#     zde je rozsireni o dalsi resolvery
#     @strawberryA.field(description="""Inner id""")
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(AsyncSessionFromInfo(info), self.id)
#         return result


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Finds theses by ID""")
    async def theses_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[ThesesGQLModel, None]:
        result = await resolve_theses_model_by_id(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ))