import sqlalchemy
import datetime

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def UUIDColumn(name=None):
    if name is None:
        return Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    else:
        return Column(name, UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    
#id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
class UserModel(BaseModel):
    __tablename__ = 'users'

    id = UUIDColumn()


class ThesesModel(BaseModel):
    __tablename__ = 'theses'

    id = UUIDColumn()
    name = Column(String)
    abstract = Column(String)
    date = Column(datetime.datetime) #najít dattyp pro datum
    assignment_name = Column(String)
    assignment_description = Column(String)
    assignment_goals = Column(String)

    author_id = Column(ForeignKey("users.id"))

    lastchange = Column(DateTime, default=datetime.datetime.now)

class RoleModel(BaseModel):
    __tablename__ = 'theses_roles'

    id = UUIDColumn()

    user_id = Column(ForeignKey("users.id"))
    roletype_id = Column(ForeignKey("theses_roletypes.id"))

class RoleTypesModel(BaseModel):
    __tablename__ = 'theses_roletypes'

    id = UUIDColumn()

    name = Column(String)

    #externalId = Column(BigInteger, index=True)

    #sections = relationship('SectionModel',back_populates = 'form')
    #datum + zadání + název práce + autorovo FK UUID //thesis
    #mimo nás - konzultanti(nová tabulka s UUID konzultantů + rolema(uuid-fk + uuid-fk) // role assignment slovník rolí(uuid - PK + name))  
    #Role a RoleType gql modely jsou obsazeny!!
###########################################################################################################################





from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker """
    asyncEngine = create_async_engine(connectionstring) 

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print('BaseModel.metadata.drop_all finished')
        if makeUp:
            await conn.run_sync(BaseModel.metadata.create_all)    
            print('BaseModel.metadata.create_all finished')

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker

import os
def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
       Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database =  os.environ.get("POSTGRES_DB", "data")
    hostWithPort =  os.environ.get("POSTGRES_HOST", "postgres:5432")
    
    driver = "postgresql+asyncpg" #"postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring