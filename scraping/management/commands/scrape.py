import re

import django
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from tqdm import tqdm
import pandas as pd
# load class from models
from scraping.models import Table
#from scraping.utils import indeed_scrape
#from django.contrib.auth import get_user_model

#User = get_user_model()

class Command(BaseCommand):
    help = "collect epl data"

    # define logic of command -- tells django it is an admin command

    def handle(self, *args, **options) -> None:
        # scrape epl table
        url = "https://fbref.com/en/comps/9/Premier-League-Stats"
        page = requests.get(url)
        text = page.text
        soup = BeautifulSoup(text)
        table_features = ["squad", "games", "wins", "draws", "losses", "goals_for", "goals_against", "goal_diff", "points"]
        
        tables = soup.findAll('tbody')
        table = tables[0]

        features = table_features
        pre_df = dict()
        rows = table.find_all('tr')
        for row in rows:
            if(row.find('th',{"scope":"row"}) != None):
                for f in features:
                    cell = row.find('td', {"data-stat": f})
                    a = cell.text.strip().encode()
                    text = a.decode('utf-8')
                    if(text == ''):
                        text = '0'
                    if f in pre_df:
                        pre_df[f].append(text)
                    else:
                        pre_df[f] = [text]
        df_table = pd.DataFrame.from_dict(pre_df)
        df_table['rank'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        print(df_table)

        for i in range(0,20):
            # initial creation of table
            # try:
            #     Table.objects.create(
            #         rank = df_table['rank'][i],
            #         squad = df_table['squad'][i],
            #         games = df_table['games'][i],
            #         wins = df_table['wins'][i],
            #         draws = df_table['draws'][i],
            #         losses = df_table['losses'][i],
            #         goals_for = df_table['goals_for'][i],
            #         goals_against = df_table['goals_against'][i],
            #         goals_difference = df_table['goal_diff'][i],
            #         points = df_table['points'][i]
            #     )
            #     print('table created')
            #except django.db.utils.IntegrityError:
                # print('not created')
            Table.objects.filter(id=i).update(rank = df_table['rank'][i], squad = df_table['squad'][i], games = df_table['games'][i],
                                                wins = df_table['wins'][i], draws = df_table['draws'][i], losses = df_table['losses'][i],
                                                goals_for = df_table['goals_for'][i], goals_against = df_table['goals_against'][i],
                                                goals_difference = df_table['goal_diff'][i], points = df_table['points'][i])
            print('table updated')
        
        # scrape epl stats
        # scrape epl schedule
        
        # save in db tables

        return