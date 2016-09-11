import os

SLACK_CHANNEL = "#apt"

MAX_PRICE = 4000
SLEEP_INTERVAL = 20 * 60

BOXES = {
	"near_caltrain": [
		[37.771571, -122.391601],
		[37.778507, -122.400484]
	],
	"south_beach": [
		[37.776287, -122.386687],
		[37.783222, -122.39557]
	],
	"potrero_hill": [
		[37.753327, -122.391729],
		[37.765583, -122.404282]
	],
	"mission_district": [
		[37.754843, -122.40602],
		[37.768527, -122.424007]
	],
}

NEIGHBORHOODS = ["mission creek", "south beach", "potrero hill", "mission district"]