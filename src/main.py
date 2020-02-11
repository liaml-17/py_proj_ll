import requests as req
import json
from datetime import datetime as dt
from datetime import timedelta as td

def main():
  api_key = 'KRQbxApMXRKqEZG451Wm87DG1DKc3SdW'
  api_url_base = 'https://api.nytimes.com/svc/movies/v2'
  full_url = api_url_base + '/reviews/picks.json?api-key=' + api_key
  resp = req.get(full_url)
  data = resp.json()

  titles = []
  dates = []
  last_mod = []
  author = []
  short_sum = []

  for item in data['results']:
    date = item['publication_date']
    year = int(date[0:4])  
    month = int(date[5:7])
    day = int(date[8:10])
    #print(date, year, month, day)

    if dt(year, month, day) > (dt.now() - td(weeks=4)):
      titles.append(item['display_title'])
      dates.append(item['publication_date'])
      last_mod.append(item['date_updated'])
      author.append(item['byline'])
      short_sum.append(item['summary_short'])
  print(set(zip(titles, dates, last_mod, author, short_sum)))

if __name__ == "__main__":
    main()