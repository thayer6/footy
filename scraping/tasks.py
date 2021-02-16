from config import celery_app
import datetime

#from scraping.models import Job
#from scraping.utils import indeed_scrape

#@celery_app.task()
# def scrape_task():
#     print('scrape task is running!')
#     print(datetime.datetime.now())
#     jobs = ["software engineer"]
#     places = [
#             {"city": "Austin", "state": "Texas"},
#     ]
#     num_pages = 1
#     scraper = indeed_scrape.IndeedScraper(
#             jobs=jobs, locations=places, num_pages=num_pages
#     )
#     scraper.large_search()

#     return 'scrape task ran!'
