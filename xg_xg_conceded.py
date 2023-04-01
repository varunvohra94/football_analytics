import understat
import aiohttp
import pandas as pd
import asyncio

# Create a dictionary to store the xG and xG conceded for each team
xg_dict = {}
xgc_dict = {}

async def main():
    async with aiohttp.ClientSession() as session:
        # Create an understat object to access the data
        understat_obj = understat.Understat(session)

        # Get the English Premier League data for the current season
        league_data = await understat_obj.get_league_results("epl", 2022)

        # Loop through each match in the data
        for match in league_data:
            
            # Get the home and away teams for the match
            home_team = match["h"]["title"]
            away_team = match["a"]["title"]

            # Get the home and away xG and xG conceded for the match
            home_xg = float(match["xG"]["h"])
            away_xg = float(match["xG"]["a"])
            home_xgc = away_xg
            away_xgc = home_xg

            # Update the home team's xG and xG conceded dictionaries
            if home_team not in xg_dict:
                xg_dict[home_team] = []
                xgc_dict[home_team] = []
            xg_dict[home_team].append(home_xg)
            xgc_dict[home_team].append(home_xgc)

            # Update the away team's xG and xG conceded dictionaries
            if away_team not in xg_dict:
                xg_dict[away_team] = []
                xgc_dict[away_team] = []
            xg_dict[away_team].append(away_xg)
            xgc_dict[away_team].append(away_xgc)

        # Create a dataframe to store the xG and xG conceded data
        data = {"Team": [], "Home xG": [], "Home xG conceded": [], "Away xG": [], "Away xG conceded": []}

        # Loop through each team and calculate their xG and xG conceded in the last 5 matches
        for team in xg_dict:

            # Get the team's xG and xG conceded lists
            xg_list = xg_dict[team]
            xgc_list = xgc_dict[team]

            # Calculate the team's xG and xG conceded in the last 5 home matches
            home_xg = sum(xg_list[-5:]) if len(xg_list) >= 5 else sum(xg_list)
            home_xgc = sum(xgc_list[-5:]) if len(xgc_list) >= 5 else sum(xgc_list)

            # Calculate the team's xG and xG conceded in the last 5 away matches
            away_xg = sum(xg_list[:5]) if len(xg_list) >= 5 else sum(xg_list)
            away_xgc = sum(xgc_list[:5]) if len(xgc_list) >= 5 else sum(xgc_list)

            # Add the data to the dataframe
            data["Team"].append(team)
            data["Home xG"].append(home_xg)
            data["Home xG conceded"].append(home_xgc)
            data["Away xG"].append(away_xg)
            data["Away xG conceded"].append(away_xgc)

        # Create a dataframe from the data dictionary
        df = pd.DataFrame(data)

        # Print the dataframe
        print(df)
        
        return df

if __name__ == '__main__':
    df = asyncio.run(main())