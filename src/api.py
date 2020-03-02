import requests as req
import json
import pandas as pd
from bs4 import BeautifulSoup
import datetime as dt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def main():
  api_key = 'KRQbxApMXRKqEZG451Wm87DG1DKc3SdW'
  api_url_base = 'https://api.nytimes.com/svc/movies/v2'
  full_url = api_url_base + '/reviews/picks.json?api-key=' + api_key
  analyser = SentimentIntensityAnalyzer()
  resp = req.get(full_url)
  data = resp.json()
  data = data['results']

  #print(data)
  titles = list(map(lambda item: item["display_title"], data))
  open_dates = list(map(lambda item: item["opening_date"], data))
  dates_update = list(map(lambda item: item["date_updated"], data))
  authors = list(map(lambda item: item["byline"], data))
  review_links = list(map(lambda item: item["link"]["url"], data))

  reviews = []
  sem_anal = []

  for item in review_links:
    requ = req.get(item)
    soppie = BeautifulSoup(requ.text, "html.parser")
    paragraphs = soppie.find('article').find_all('p')
    temp = ""

    for p in paragraphs:
      temp = temp + ' ' + p.text
    
    reviews.append(temp)

  for item in reviews:
    sem_anal.append(analyser.polarity_scores(item))

  movies = []
  for i in range(len(titles)):
    if open_dates[i] is not None:
      temp = (str(sem_anal[i]['neg'] * 100) + "% Negative, "
        + str(sem_anal[i]['neu'] * 100) + "% Neutral, " 
        + str(sem_anal[i]['pos'] * 100) + "% Positive")
      movies.append({
      "Title" : titles[i],
      "Opening date" : open_dates[i],
      "Date updated" : dates_update[i],
      "Author" : authors[i],
      "Review" : reviews[i],
      "Analysis" : temp
    })

  movies.sort(key=lambda x: dt.datetime.strptime(x['Opening date'], '%Y-%m-%d'),
    reverse=True)

  j = 1;
  for i in movies:
    if j > 15:
      break  
    for key, val in i.items():
      print(key, ':', val)
    print("")
    j = j + 1;

if __name__ == "__main__":
    main()