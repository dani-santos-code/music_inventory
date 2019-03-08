from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import BOOLEAN, TEXT, TIMESTAMP, VARCHAR
import datetime

Base = declarative_base()

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
    description = Column(String(500), nullable = False)
    credit = Column(String(80))
    picture = Column(String(250), nullable = False)
    region_id = Column(Integer,ForeignKey('region.id'))
    region = relationship(Region)
    user_id = Column(Integer)
    user_name = Column(String(250))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name': self.name,
           'id': self.id,
           'description': self.description,
           'region': self.region.name,
           'picture_url': self.picture,
           'credit': self.credit,
           'user_name': self.user_name,
       }

engine = create_engine('sqlite:///instruments.db')

Base.metadata.create_all(engine)

if __name__ == '__main__':
    print("----> Database Setup complete")
