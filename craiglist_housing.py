from craigslist import CraigslistHousing
from slackclient import SlackClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
import settings
import private

engine = create_engine('sqlite:///listings.db', echo=False)

Base = declarative_base()

class Listing(Base):
    """
    A table to store data on craigslist listings.
    """

    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    cl_id = Column(Integer, unique=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def in_box(coords, box):
	if box[0][0] < coords[0] < box[1][0] and box[1][1] < coords[1] < box[0][1]:
		return True
	return False

def scrape():
	sc = SlackClient(private.SLACK_TOKEN)
	cl = CraigslistHousing(site='sfbay', area='sfc', category='apa',
		filters={'max_price': settings.MAX_PRICE})

	results = cl.get_results(sort_by='newest', geotagged=True, limit=20)
	for result in results:
		# Check if listing is already posted
		listing = session.query(Listing).filter_by(cl_id=result['id']).first()

		if listing is None:
			# If there is no string identifying which neighborhood the result is from, skip it.
			if result["where"] is None:
				continue

			area_found = False
			area = ""
			geotag = result["geotag"]
			# check with our bounding boxes
			if geotag is not None:
				print(geotag)
				for a, coords in settings.BOXES.items():

					if in_box(geotag, coords):
						area = a
						area_found = True

			location = result["where"]
			if location is not None:
				for hood in settings.NEIGHBORHOODS:
					if hood in location.lower():
						area = hood
						area_found = True

			if area_found:
				# Create listing object
				new_listing = Listing(
					link=result["url"],
					cl_id=result["id"]
				)

				# Save listing so we don't grab it again
				session.add(new_listing)
				session.commit()

				# Post to slack channel
				desc = "{0} | {1} | {2} | {3}".format(area, result["price"], result["name"], result["url"])
				sc.api_call(
						"chat.postMessage", channel=settings.SLACK_CHANNEL, text=desc,
						username="dalek", icon_emoji=":robot_face:"
					)


		