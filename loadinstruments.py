from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

from database_setup import Base, User, Region, Instrument

engine = create_engine('sqlite:///instruments.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy users
User1 = User(name="Donald Duck", email="donald@duck.com", active=True, tokens="7351623abvasd7", avatar="http://www.hsb.com/duck.jpeg", created_at=datetime.datetime.now())
session.add(User1)
session.commit()

User2 = User(name="Freddy Mercury", email="freddy@mercury.com", active=True, tokens="r423abnsvx7365nxd", avatar="http://www.hsb.com/freddyself.jpeg", created_at=datetime.datetime.now())
session.add(User2)
session.commit()

User3 = User(name="Mary Poppins", email="mary@poppins.com", active=False, tokens="17632ssd", avatar="http://www.hsb.com/mary.jpeg", created_at=datetime.datetime.now())
session.add(User3)
session.commit()

# Instruments in Africa
region1 = Region(name="Africa")

session.add(region1)
session.commit()

instrument1 = Instrument(user_id=1, name="Djembe",
                         description="Originating from West Africa, the djembe (also known as jembe is a small goblet drum that a musician generally plays with their bare hands.",
                         picture="https://s3.amazonaws.com/images.static.steveweissmusic.com/products/images/uploads/1132207_25730_popup.jpg",
                         region=region1, credit="Steve Weiss Music")

session.add(instrument1)
session.commit()

instrument2 = Instrument(user_id=2, name="Mbira",
                         description="Originating in African culture, particularly in the Democratic Republic of Congo, the mbira consists of metal teeth attached to a wooden board.",
                         picture="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Mbira_dzavadzimu_1.jpg/1069px-Mbira_dzavadzimu_1.jpg",
                         region=region1, credit="Wikipedia")

session.add(instrument2)
session.commit()

# Instruments in the South America

region2 = Region(name="South America")

session.add(region2)
session.commit()

instrument1 = Instrument(user_id=2, name="Idiophones",
                         description="Idiophones produce musical sound by vibrating when the body of the instrument itself is struck, stamped, shaken, scraped, rubbed, or plucked.",
                         picture="https://cdn.britannica.com/s:700x450/91/150591-004-44609FB8.jpg",
                         region=region2, credit="Britannica")

instrument2 = Instrument(user_id=3, name="Membranophones",
                         description="Membranophones are instruments that have a skin or membrane stretched over a frame; musical sound is produced by striking or rubbing the membrane or by setting the membrane into motion with sound waves (as with a kazoo).",
                         picture="https://cdn.britannica.com/s:300x300/89/150589-004-B285F698.jpg",
                         region=region2, credit="Britannica")
session.add(instrument2)
session.commit()

# Instruments in Asia

region3 = Region(name="Asia")

session.add(region3)
session.commit()

instrument1 = Instrument(user_id=1, name="Ocarina",
                         description="Originating within China approximately 12,000 years ago, the ocarina is an ancient flute instrument usually made from ceramic or clay. ",
                         picture="https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/2016-01_Ocarina_front.jpg/500px-2016-01_Ocarina_front.jpg",
                         region=region3, credit="Wikipedia")

session.add(instrument1)
session.commit()

instrument2 = Instrument(user_id=2, name="Ghungroos",
                         description="An ancient and classic instrument from India, a ghungroos is a metallic anklet that Indian dancers place around their feet while performing  in ceremonies.",
                         picture="https://4.imimg.com/data4/DN/PQ/MY-107458/ghungroo-500x500.jpg",
                         region=region3)

session.add(instrument2)
session.commit()

# Instruments in Europe

region4 = Region(name="Europe")

session.add(region4)
session.commit()

instrument1 = Instrument(user_id=3, name="Octobass",
                         description="Hector Berlioz was an ardent admirer of these massive, three-stringed, whale-like instruments, referring to them in his famous Treatise on Orchestration.",
                         picture="https://rbma.imgix.net/_NRK4545_copy_1600_1067_90.624993dd.jpg?auto=format&w=400",
                         region=region4)

session.add(instrument1)
session.commit()

# Instruments in Oceania

region5 = Region(name="Oceania")

session.add(region5)
session.commit()

instrument1 = Instrument(user_id=1, name="Didgeridoo",
                         description="From indigenous Australians comes the ever exotic didgeridoo which is rumored to have been around for over a thousand years.",
                         picture="https://images-na.ssl-images-amazon.com/images/I/61ffnSrQkAL._SL1500_.jpg",
                         region=region5, credit="Kent State University")

session.add(instrument1)
session.commit()

# Instruments in North america

region6 = Region(name="North America")

session.add(region6)
session.commit()

instrument1 = Instrument(user_id=1, name="Guitarron",
                         description="The Guitarron is a large bass guitar. Guitarron translates to large guitar. The suffix means big or large. It has 6 strings.",
                         picture="http://content.westmusic.com/wp-content/uploads/2019/02/Guitarron.png",
                         region=region6, credit="West Music")


session.add(instrument1)
session.commit()

print ("added instruments to DB!")
