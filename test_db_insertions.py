# import unittest
# from database_setup import Base, User, Instrument, Region
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# class appDBTests(unittest.TestCase):
#     """Test insertions in the database,
#     making sure all required fields are valid
#     """
#
#     def test_user_insertion(self):
#         """Test if user was inserted correctly"""
#         engine = create_engine('sqlite:///instruments.db')
#         Base.metadata.bind = engine
#         DBSession = sessionmaker(bind=engine)
#         session = DBSession()
#
#         user = User(name="Dani", email='patkennedy79@gmail.com')
#         session.add(user)
#         session.commit()
#
#         Base.metadata.drop_all(engine)
#
#     def test_instrument_insertion(self):
#         """Test if instrument was inserted correctly
#         with all minimum requirements"""
#         engine = create_engine('sqlite:///instruments.db')
#         Base.metadata.bind = engine
#         DBSession = sessionmaker(bind=engine)
#         session = DBSession()
#
#         instrument = Instrument(name="My Instrument", description="blabla", picture="lala")
#         session.add(instrument)
#         session.commit()
#
#
#     def test_region_insertion(self):
#         """Test if region was inserted correctly
#         with all minimum requirements"""
#         engine = create_engine('sqlite:///instruments.db')
#         Base.metadata.bind = engine
#         DBSession = sessionmaker(bind=engine)
#         session = DBSession()
#
#         region = Region(name="My Region")
#         session.add(region)
#         session.commit()
