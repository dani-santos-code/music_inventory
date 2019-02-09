from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name': self.name,
           'id': self.id,
           'email': self.email,
       }


class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name': self.name,
           'id': self.id,
       }

class Instrument(Base):
    __tablename__ = 'instrument'


    name = Column(String(120), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250), nullable = False)
    credit = Column(String(80))
    picture = Column(String(250), nullable = False)
    region_id = Column(Integer,ForeignKey('region.id'))
    region = relationship(Region)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name': self.name,
           'description' : self.description,
           'id': self.id,
           'picture': self.picture,
           'region': self.region,
           'user': self.user,
           'credit': sekf.credit,
       }


engine = create_engine('sqlite:///instruments.db')

Base.metadata.create_all(engine)
