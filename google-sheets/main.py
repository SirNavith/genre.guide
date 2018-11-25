from csv import writer
from itertools import groupby
from operator import attrgetter
from os import getenv

from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/drive.readonly"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("client.secret.json", scope)

client = authorize(credentials)

genre_sheet = client.open_by_key(getenv("SHEET_KEY"))

catalog = genre_sheet.worksheet("Main")

catalog_header = catalog.row_values(1)
all_tracks = catalog.range(2, 1, catalog.row_count, catalog.col_count)

with open("./src/csv/all_tracks.csv", "w") as csv_file:
	csv_writer = writer(csv_file, delimiter="\t")
		
	for row_number, row in groupby(all_tracks, key=attrgetter("row")):
		csv_writer.writerow(map(attrgetter("value"), row))