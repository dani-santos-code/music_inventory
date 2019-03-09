from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

from database_setup import Base, Region, Instrument

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

# Instruments in Africa
region1 = Region(name="Africa")

session.add(region1)
session.commit()

instrument1 = Instrument(user_id=11, name="Djembe",
                         description="Originating from West Africa, the djembe (also known as jembe is a small goblet drum that a musician generally plays with their bare hands.",
                         picture="https://s3.amazonaws.com/images.static.steveweissmusic.com/products/images/uploads/1132207_25730_popup.jpg",
                         region=region1, credit="Steve Weiss Music", user_name="Michael Jackson")

session.add(instrument1)
session.commit()

instrument2 = Instrument(user_id=10, name="Mbira",
                         description="Originating in African culture, particularly in the Democratic Republic of Congo, the mbira consists of metal teeth attached to a wooden board.",
                         picture="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Mbira_dzavadzimu_1.jpg/1069px-Mbira_dzavadzimu_1.jpg",
                         region=region1, credit="Wikipedia", user_name="Mary Poppins")

session.add(instrument2)
session.commit()

instrument3 = Instrument(user_id=10, name="Shekere",
                         description="The Shekere is one of the most famous shakers in Africa. The instrument consists of closely woven beads that form a net. The net is placed around a gourd. Sound is produced by either shaking it or slamming it against the hands. The Shekere is mainly found in West Africa in countries such as Nigeria, Senegal, Ivory Coast, Togo, Ghana and many others.",
                         picture="https://answersafrica.com/wp-content/uploads/2014/08/Shekere.jpg",
                         region=region1, credit="Answers Africa", user_name="Mary Poppins")

session.add(instrument3)
session.commit()

# Instruments in the South America

region2 = Region(name="South America")

session.add(region2)
session.commit()

instrument4 = Instrument(user_id=2, name="Idiophones",
                         description="Idiophones produce musical sound by vibrating when the body of the instrument itself is struck, stamped, shaken, scraped, rubbed, or plucked.",
                         picture="https://cdn.britannica.com/s:700x450/91/150591-004-44609FB8.jpg",
                         region=region2, credit="Britannica", user_name="R. Kelley")


session.add(instrument4)
session.commit()

instrument5 = Instrument(user_id=6, name="Membranophones",
                         description="Membranophones are instruments that have a skin or membrane stretched over a frame; musical sound is produced by striking or rubbing the membrane or by setting the membrane into motion with sound waves (as with a kazoo).",
                         picture="https://cdn.britannica.com/s:300x300/89/150589-004-B285F698.jpg",
                         region=region2, credit="Britannica", user_name="Lady Gaga")

session.add(instrument5)
session.commit()

instrument6 = Instrument(user_id=6, name="Pandeiro",
                         description="The pandeiro is a type of hand frame drum popular in Brazil, and which has been described as an unofficial instrument of that nation.[citation needed] The drumhead is tunable, and the rim holds metal jingles (platinelas), which are cupped creating a crisper, drier and less sustained tone on the pandeiro than on the tambourine",
                         picture="https://upload.wikimedia.org/wikipedia/commons/6/65/Pandeiro.jpg",
                         region=region2, credit="Britannica", user_name="Lady Gaga")

session.add(instrument6)
session.commit()

# Instruments in Asia

region3 = Region(name="Asia")

session.add(region3)
session.commit()

instrument7 = Instrument(user_id=1, name="Ocarina",
                         description="Originating within China approximately 12,000 years ago, the ocarina is an ancient flute instrument usually made from ceramic or clay. ",
                         picture="https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/2016-01_Ocarina_front.jpg/500px-2016-01_Ocarina_front.jpg",
                         region=region3, credit="Wikipedia", user_name="Freddy Meercury")

session.add(instrument7)
session.commit()

instrument8 = Instrument(user_id=2, name="Ghungroos",
                         description="An ancient and classic instrument from India, a ghungroos is a metallic anklet that Indian dancers place around their feet while performing  in ceremonies.",
                         picture="https://4.imimg.com/data4/DN/PQ/MY-107458/ghungroo-500x500.jpg",
                         region=region3, user_name="David Bowie")

session.add(instrument8)
session.commit()

instrument9 = Instrument(user_id=9, name="Erhu",
                         description="The erhu is a two-stringed bowed musical instrument and is known in the Western world as the 'Chinese violin' or a 'Chinese two-stringed fiddle.'",
                         picture="https://hamiltonphilharmonic.files.wordpress.com/2014/05/erhu1.jpg",
                         region=region3, credit="Hamilton Philarmonic", user_name="Mark Robson")

session.add(instrument9)
session.commit()

instrument10 = Instrument(user_id=2, name="Guzheng",
                         description="The guzheng is a 21-stringed zither, which is an instrument that has strings stretched over movable bridges across a long, flat body. Originally made with silk strings, contemporary guzhengs now have strings made from metal-nylon. The instrument is usually plucked with shells of hawksbill.",
                         picture="https://hamiltonphilharmonic.files.wordpress.com/2014/05/931.jpg?w=600&h=450",
                         region=region3, credit="Hamilton Philarmonic", user_name="Alfredo Manfredi")

session.add(instrument10)
session.commit()

instrument11 = Instrument(user_id=4, name="Pipa",
                         description="The pipa is a four-stringed Chinese musical instrument. The instrument has a pear-shaped wooden body with frets like those on a guitar. It sounds like a banjo.",
                         picture="https://images.chinahighlights.com/2012/10/ba4d7f5b39574dba921f4648_ch_300x240.jpg",
                         region=region3, credit="China Highlights", user_name="Jan Lee")

session.add(instrument11)
session.commit()

instrument12 = Instrument(user_id=7, name="Sur Bahar",
                          description="Hand-crafted by Nahasapimapetalan, Sharma & Co., this professional quality bass sitar is imported directly from India for Lawrence-Hodge. Double toomba, 7 main strings, fully carved. Includes lovely case.",
                          picture="http://people.bu.edu/plawrenc/instruments/SITAR/Surbahar.jpe",
                          region=region3, credit="BU", user_name="Lynn Adam")

session.add(instrument12)
session.commit()

# Instruments in Europe

region4 = Region(name="Europe")

session.add(region4)
session.commit()

instrument13 = Instrument(user_id=8, name="Octobass",
                          description="Hector Berlioz was an ardent admirer of these massive, three-stringed, whale-like instruments, referring to them in his famous Treatise on Orchestration.",
                          picture="https://rbma.imgix.net/_NRK4545_copy_1600_1067_90.624993dd.jpg?auto=format&w=400",
                          region=region4, user_name="Mark Ronson")

session.add(instrument13)
session.commit()

instrument14 = Instrument(user_id=8, name="Hurdy-gurdy",
                          description="The hurdy-gurdy is a stringed instrument that produces sound by a hand crank-turned, rosined wheel rubbing against the strings. The wheel functions much like a violin bow, and single notes played on the instrument sound similar to those of a violin.",
                          picture="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Louvet_Drehleier.JPG/500px-Louvet_Drehleier.JPG",
                          region=region4, user_name="Mark Ronson")

session.add(instrument14)
session.commit()

instrument15 = Instrument(user_id=6, name="Bodhran",
                          description="Bodhran is an Irish frame drum.",
                          picture="https://upload.wikimedia.org/wikipedia/commons/1/1a/Bodhran.jpg",
                          region=region4, user_name="Lady Gaga")

session.add(instrument15)
session.commit()

# Instruments in Oceania

region5 = Region(name="Oceania")

session.add(region5)
session.commit()

instrument16 = Instrument(user_id=14, name="Didgeridoo",
                          description="From indigenous Australians comes the ever exotic didgeridoo which is rumored to have been around for over a thousand years.",
                          picture="https://images-na.ssl-images-amazon.com/images/I/61ffnSrQkAL._SL1500_.jpg",
                          region=region5, credit="Kent State University", user_name="Queen Elizabeth")

session.add(instrument16)
session.commit()

instrument17 = Instrument(user_id=8, name="Mbita-Ni-Tanga",
                          description="From Fiji, nose flutes are played by blowing the instrument with the nose rather than the mouth. Holding one nostril shut with thumb or finger, the musician blows into a small hole near the top of the instrument with the other nostril.",
                          picture="https://www.metmuseum.org/toah/images/hb/hb_89.4.795.jpg",
                          region=region5, credit="The Met", user_name="Mark Ronson")

session.add(instrument17)
session.commit()

instrument18 = Instrument(user_id=8, name="Taonga puro",
                          description="The instruments previously fulfilled many functions within Maori society including a call to arms, dawning of the new day, communications with the gods and the planting of crops",
                          picture="https://static1.squarespace.com/static/53218f7ce4b01580f3c745e4/5af8f5118a922d06174e5420/5af8f670aa4a99214407bf2a/1526287501130/_43O9926.JPG?format=2500w",
                          region=region5, credit="Rob Thorne", user_name="Mark Ronson")

session.add(instrument18)
session.commit()

# Instruments in North america

region6 = Region(name="North America")

session.add(region6)
session.commit()

instrument19 = Instrument(user_id=13, name="Guitarron",
                          description="The Guitarron is a large bass guitar. Guitarron translates to large guitar. The suffix means big or large. It has 6 strings.",
                          picture="http://content.westmusic.com/wp-content/uploads/2019/02/Guitarron.png",
                          region=region6, credit="West Music", user_name="Karl Marx")


session.add(instrument19)
session.commit()

instrument20 = Instrument(user_id=6, name="American Flute",
                          description="The Native American flute is a flute that is held in front of the player, has open finger holes, and has two chambers: one for collecting the breath of the player and a second chamber which creates sound. The player breathes into one end of the flute without the need for an embouchure.",
                          picture="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Native_American_Flute_by_Chief_Arthur_Two_Crows.jpg/500px-Native_American_Flute_by_Chief_Arthur_Two_Crows.jpg",
                          region=region6, credit="Wikipedia", user_name="Lady Gaga")


session.add(instrument20)
session.commit()

instrument21 = Instrument(user_id=13, name="Water Drum",
                          description="Water drums are a category of membranophone characterized by the filling of the drum chamber with some amount of water to create a unique resonant sound. Water drums are used all over the world, including American Indian music, and are made of various materials, with a membrane stretched over a hard body such as a metal, clay, or wooden pot.",
                          picture="https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Wassertrommeln.jpg/440px-Wassertrommeln.jpg",
                          region=region6, credit="Wikipedia", user_name="Karl Marx")


session.add(instrument21)
session.commit()

print ("added instruments to DB!")
