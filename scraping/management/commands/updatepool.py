import django
from pandas.core.indexes.base import Index
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from tqdm import tqdm
import pandas as pd
import numpy as np
import re
# load class from models
from scraping.models import Table, PoolTable

class Command(BaseCommand):
    help = "collect epl data"

    # define logic of command -- tells django it is an admin command

    def handle(self, *args, **options) -> None:

        owners = ["Casey", "Megan", "Neo", "Jason", "CB"]
        casey_teams = ["Liverpool", "Everton", "Sheffield Utd", "Fulham"]
        megan_teams = ["Chelsea", "Arsenal", "West Ham", "Crystal Palace"]
        neo_teams = ["Leicester City", "Tottenham", "Newcastle Utd", "Aston Villa"]
        jason_teams = ["Manchester City", "Southampton", "Leeds United", "West Brom"]
        cb_teams = ["Manchester Utd", "Wolves", "Burnley", "Brighton"]
        teams_order = [casey_teams, megan_teams, neo_teams, jason_teams, cb_teams]

        squad_dict = {'Casey': casey_teams, 'Megan': megan_teams, 'Neo': neo_teams, 'Jason': jason_teams, 'CB': cb_teams}



        epl_table = pd.DataFrame.from_records(Table.objects.all().values_list('squad', 'points'))
        epl_table.columns = ['squad', 'points']
        #print(epl_table)

        casey_table = epl_table[epl_table.squad.isin(casey_teams)]
        casey_pts = sum(casey_table['points'])
        megan_table = epl_table[epl_table.squad.isin(megan_teams)]
        megan_pts = sum(megan_table['points'])
        neo_table = epl_table[epl_table.squad.isin(neo_teams)]
        neo_pts = sum(neo_table['points'])
        jason_table = epl_table[epl_table.squad.isin(jason_teams)]
        jason_pts = sum(jason_table['points'])
        cb_table = epl_table[epl_table.squad.isin(cb_teams)]
        cb_pts = sum(cb_table['points'])

        pts_order = [casey_pts, megan_pts, neo_pts, jason_pts, cb_pts]

        pool = []

        for i in range(0,len(owners)):
            pool.append({
                'owner': owners[i],
                'squads': str(teams_order[i]),
                'points': pts_order[i]
            })

        pool_table = pd.DataFrame(pool)

        # need to clean up squad names
        # for i in range(0, len(owners)):

        #     pool_table.iloc[i]['Squads'] = re.sub(r'\[', '', pool_table.iloc[i]['Squads'])

        PoolTable.objects.all().delete()
        
        for i in range(0,len(owners)):
            # initial creation of table
            try:
                PoolTable.objects.create(
                    owner = pool_table['owner'][i],
                    squads = pool_table['squads'][i],
                    points = pool_table['points'][i]
                )
                while (i==len(owners)):
                    print('table created')
            except django.db.utils.IntegrityError:
                print('not created')

            # Table.objects.filter(id=i).update(rank = df_table['rank'][i], squad = df_table['squad'][i], games = df_table['games'][i],
            #                                     wins = df_table['wins'][i], draws = df_table['draws'][i], losses = df_table['losses'][i],
            #                                     goals_for = df_table['goals_for'][i], goals_against = df_table['goals_against'][i],
            #                                     goals_difference = df_table['goal_diff'][i], points = df_table['points'][i])
            # if(i==19):
            #     print('table updated')
            #     print(df_table)

        return