import re

import django
from pandas.core.indexes.base import Index
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from tqdm import tqdm
import pandas as pd
import numpy as np
# load class from models
from scraping.models import Table, ResultsFixtures, Stats
#from scraping.utils import indeed_scrape
#from django.contrib.auth import get_user_model

#User = get_user_model()

class Command(BaseCommand):
    help = "collect epl data"

    # define logic of command -- tells django it is an admin command

    def handle(self, *args, **options) -> None:

        # define function to get a table
        def get_table(url, features):
            url = url
            page = requests.get(url)
            text = page.text
            soup = BeautifulSoup(text, features="html.parser")
            table_features = features
            tables = soup.findAll('tbody')
            table = tables[0]

            pre_df = dict()
            rows = table.find_all('tr')
            for row in rows:
                if(row.find('th', {'scope':'row'}) != None):
                    for f in table_features:
                        cell = row.find('td', {"data-stat": f})
                        if(cell is None):
                            cell = str("N/A")
                            a = cell.encode()
                            text=a.decode('utf-8')
                        else:
                            a = cell.text.strip().encode()
                            text = a.decode('utf-8')
                        if f in pre_df:
                            pre_df[f].append(text)
                        else:
                            pre_df[f] = [text]
            df_table = pd.DataFrame.from_dict(pre_df)
            return df_table    

        # scrape epl table
        # url = "https://fbref.com/en/comps/9/Premier-League-Stats"
        # page = requests.get(url)
        # text = page.text
        # soup = BeautifulSoup(text)
        table_features = ["squad", "games", "wins", "draws", "losses", "goals_for", "goals_against", "goal_diff", "points"]
        #table_features = ["squad", "games", "wins", "draws", "losses", "goals_for", "goals_against", "goal_diff", "points", "xg_for", "xg_against", "xg_diff", "xg_diff_per90", "last_5", "attendance_per_g", "top_team_scorers", "top_keeper"]
        results_fix_features = ["gameweek", "dayofweek", "date", "time", "squad_a", "xg_a", "score", "xg_b", "squad_b", "attendance", "venue", "referee"]
        stats_features = ["players_used", "avg_age", "possession", "games", "games_starts", "minutes", "minutes_90s", "goals", "assists", "goals_pens", "pens_made", "pens_att", "cards_yellow", "cards_red", "goals_per90", "assists_per90", 
        "goals_assists_per90", "goals_pens_per90", "goals_assists_pens_per90", "xg", "npxg", "xa", "xa_per90", "xg_xa_per90", "npxg_per90", "npxg_xa_per90"]
        
        # tables = soup.findAll('tbody')
        # table = tables[0]

        # features = table_features
        # pre_df = dict()
        # rows = table.find_all('tr')
        # for row in rows:
        #     if(row.find('th',{"scope":"row"}) != None):
        #         for f in features:
        #             cell = row.find('td', {"data-stat": f})
        #             a = cell.text.strip().encode()
        #             text = a.decode('utf-8')
        #             if(text == ''):
        #                 text = '0'
        #             if f in pre_df:
        #                 pre_df[f].append(text)
        #             else:
        #                 pre_df[f] = [text]
        # df_table = pd.DataFrame.from_dict(pre_df)

        # reset table database
        #Table.objects.all().delete()

        table_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
        df_table = get_table(table_url, table_features)

        df_table['rank'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        #print(df_table)

        # reset resultsfix database
        #ResultsFixtures.objects.all().delete()
        
        results_fixtures_url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
        resfix_df = get_table(results_fixtures_url, results_fix_features)

        resfix_df['date'].replace('', np.nan, inplace=True)
        resfix_df = resfix_df.dropna(subset=['date']).reset_index(drop=True)
        for i in range(0,len(resfix_df['time'])):
            if (resfix_df['time'][i] == ""):
                resfix_df['time'][i] = '00:00'
            if (resfix_df['xg_a'][i] == ""):
                resfix_df['xg_a'][i] = 0
                resfix_df['xg_b'][i] = 0
        #print(resfix_df)

        # reset stats database
        #Stats.objects.all().delete()

        stats_url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
        stats_df = get_table(stats_url, stats_features)

        # get squad names
        page = requests.get(stats_url)
        content = page.text
        soup = BeautifulSoup(content, features="html.parser")
        tables = soup.findAll('tbody')
        table = tables[0]
        squad_pre_df = list()
        rows = table.find_all('tr')

        for i in range(0,20):
            cell = rows[i].find('th', {"data-stat":'squad'})
            a = cell.text.strip().encode()
            text = a.decode('utf-8')
            squad_pre_df.append(text)

        stats_df = stats_df[0:20]
        stats_df['squad'] = squad_pre_df
        stats_df["minutes"] = stats_df["minutes"].str.replace(",","").astype(float).astype(int)
        #print(stats_df)
        for i in range(0,20):
            # initial creation of table
            try:
                Table.objects.create(
                    rank = df_table['rank'][i],
                    squad = df_table['squad'][i],
                    games = df_table['games'][i],
                    wins = df_table['wins'][i],
                    draws = df_table['draws'][i],
                    losses = df_table['losses'][i],
                    goals_for = df_table['goals_for'][i],
                    goals_against = df_table['goals_against'][i],
                    goals_difference = df_table['goal_diff'][i],
                    points = df_table['points'][i]
                )
                while (i==20):
                    print('table created')
            except django.db.utils.IntegrityError:
                print('not created')
            # uncomment this to work
            # Table.objects.filter(id=i).update(rank = df_table['rank'][i], squad = df_table['squad'][i], games = df_table['games'][i],
            #                                     wins = df_table['wins'][i], draws = df_table['draws'][i], losses = df_table['losses'][i],
            #                                     goals_for = df_table['goals_for'][i], goals_against = df_table['goals_against'][i],
            #                                     goals_difference = df_table['goal_diff'][i], points = df_table['points'][i])
            # if(i==19):
            #     print('table updated')
            #     print(df_table)
        

        # # scrape epl schedule
        for i in range(0,len(resfix_df['date'])):
            #initial creation of table
            try:
                ResultsFixtures.objects.create(
                    week = resfix_df['gameweek'][i],
                    day = resfix_df['dayofweek'][i],
                    date = resfix_df['date'][i],
                    time = resfix_df['time'][i],
                    home = resfix_df['squad_a'][i],
                    xg_h = resfix_df['xg_a'][i],
                    score = resfix_df['score'][i],
                    xg_a = resfix_df['xg_b'][i],
                    away = resfix_df['squad_b'][i],
                    attendance = resfix_df['attendance'][i],
                    venue = resfix_df['venue'][i],
                    referee = resfix_df['referee'][i]
                )
                while(i==20):
                    print('results & fixtures table created')
            except django.db.utils.IntegrityError:
                print('not created')
        #     ResultsFixtures.objects.filter(id=i).update(
        #             week = resfix_df['gameweek'][i],
        #             day = resfix_df['dayofweek'][i],
        #             date = resfix_df['date'][i],
        #             time = resfix_df['time'][i],
        #             home = resfix_df['squad_a'][i],
        #             xg_h = resfix_df['xg_a'][i],
        #             score = resfix_df['score'][i],
        #             xg_a = resfix_df['xg_b'][i],
        #             away = resfix_df['squad_b'][i],
        #             attendance = resfix_df['attendance'][i],
        #             venue = resfix_df['venue'][i],
        #             referee = resfix_df['referee'][i]
        #     )
        # if(i==(len(resfix_df['date']) - 1)):
        #     print('results & fixtures updated')
        #     print(resfix_df)
        # scrape epl stats
        for i in range(0,20):
            # # initial creation of table
            try:
                Stats.objects.create(
                    squad = stats_df['squad'][i],
                    players_used = stats_df['players_used'][i],
                    avg_age = stats_df['avg_age'][i],
                    possession = stats_df['possession'][i],
                    games = stats_df['games'][i],
                    games_starts = stats_df['games_starts'][i],
                    minutes = stats_df['minutes'][i],
                    minutes_90 = stats_df['minutes_90s'][i],
                    goals = stats_df['goals'][i],
                    assists = stats_df['assists'][i],
                    goals_pens = stats_df['goals_pens'][i],
                    pens_made = stats_df['pens_made'][i],
                    pens_att = stats_df['pens_att'][i],
                    cards_yellow = stats_df['cards_yellow'][i],
                    cards_red = stats_df['cards_red'][i],
                    goals_per90 = stats_df['goals_per90'][i],
                    goals_assists_per90 = stats_df['goals_assists_per90'][i],
                    goals_pens_per90 = stats_df['goals_pens_per90'][i],
                    goals_assists_pens_per90 = stats_df['goals_assists_pens_per90'][i],
                    xg = stats_df['xg'][i],
                    npxg = stats_df['npxg'][i],
                    xa = stats_df['xa'][i],
                    xa_per90 = stats_df['xa_per90'][i],
                    xg_xa_per90 = stats_df['xg_xa_per90'][i],
                    npxg_per90 = stats_df['npxg_per90'][i],
                    npxg_xa_per90 = stats_df['npxg_xa_per90'][i] 
                )
                while (i==20):
                    print('stats table created')
            except django.db.utils.IntegrityError:
                print('not created')      
        #     for j in range(61,80):     
        #         Stats.objects.filter(id=j).update(
        #             squad = stats_df['squad'][i],
        #             players_used = stats_df['players_used'][i],
        #             avg_age = stats_df['avg_age'][i],
        #             possession = stats_df['possession'][i],
        #             games = stats_df['games'][i],
        #             games_starts = stats_df['games_starts'][i],
        #             minutes = stats_df['minutes'][i],
        #             minutes_90 = stats_df['minutes_90s'][i],
        #             goals = stats_df['goals'][i],
        #             assists = stats_df['assists'][i],
        #             goals_pens = stats_df['goals_pens'][i],
        #             pens_made = stats_df['pens_made'][i],
        #             pens_att = stats_df['pens_att'][i],
        #             cards_yellow = stats_df['cards_yellow'][i],
        #             cards_red = stats_df['cards_red'][i],
        #             goals_per90 = stats_df['goals_per90'][i],
        #             goals_assists_per90 = stats_df['goals_assists_per90'][i],
        #             goals_pens_per90 = stats_df['goals_pens_per90'][i],
        #             goals_assists_pens_per90 = stats_df['goals_assists_pens_per90'][i],
        #             xg = stats_df['xg'][i],
        #             npxg = stats_df['npxg'][i],
        #             xa = stats_df['xa'][i],
        #             xa_per90 = stats_df['xa_per90'][i],
        #             xg_xa_per90 = stats_df['xg_xa_per90'][i],
        #             npxg_per90 = stats_df['npxg_per90'][i],
        #             npxg_xa_per90 = stats_df['npxg_xa_per90'][i]
        #     )
        # if(i==19):
        #     print('stats updated')
        #     print(stats_df)
        return