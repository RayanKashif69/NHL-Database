
import sys
sys.path.insert(0, "dependencies")  # Add the dependencies folder to the search path



from prettytable import PrettyTable

def event_statistics_menu(connection):
    """Handle Event Statistics Queries."""
    try:
        # Step 1: Display all teams
        print("\nDisplaying all teams:")
        query_teams = """
            SELECT team_id, teamName
            FROM team_info
            ORDER BY teamName ASC;
        """
        cursor = connection.cursor(as_dict=True)
        cursor.execute(query_teams)
        teams = cursor.fetchall()

        if not teams:
            print("No teams found in the database.")
            return

        # Display teams in a table
        table_teams = PrettyTable()
        table_teams.field_names = ["Number", "Team ID", "Team Name"]
        for i, team in enumerate(teams, start=1):
            table_teams.add_row([i, team["team_id"], team["teamName"]])
        print(table_teams)

        # Step 2: User selects a team
        team_number = int(input("\nSelect a team by entering the corresponding number: "))
        if team_number < 1 or team_number > len(teams):
            print("Invalid selection. Please try again.")
            return
        selected_team_id = teams[team_number - 1]["team_id"]

        # Step 3: Display all games for the selected team
        print(f"\nDisplaying all games for team ID: {selected_team_id}")
        query_games = """
            SELECT g.game_id, g.date_time_GMT, g.outcome, g.type
            FROM game g
            JOIN game_teams_stats gts ON g.game_id = gts.game_id
            WHERE gts.team_id = %s
            ORDER BY g.date_time_GMT DESC;
        """
        cursor.execute(query_games, (selected_team_id,))
        games = cursor.fetchall()

        if not games:
            print(f"No games found for team ID: {selected_team_id}.")
            return

        # Display games in a table
        table_games = PrettyTable()
        table_games.field_names = ["Game ID", "Date & Time (GMT)", "Outcome", "Type"]
        for game in games:
            table_games.add_row([game["game_id"], game["date_time_GMT"], game["outcome"], game["type"]])
        print(table_games)

        # Step 4: User selects a game
        selected_game_id = input("\nEnter the Game ID to view events: ")

        # Step 5: User inputs a period
        selected_period = int(input("\nEnter the period (1, 2, or 3): "))
        if selected_period not in [1, 2, 3]:
            print("Invalid period. Please enter 1, 2, or 3.")
            return

        # Step 6: Query and display events for the selected game and period
        print(f"\nDisplaying events for game ID: {selected_game_id}, period: {selected_period}")
        query_events = """
            SELECT play_id, event, periodTime
            FROM Event
            WHERE game_id = %s AND period = %s
            ORDER BY periodTime;
        """
        cursor.execute(query_events, (selected_game_id, selected_period))
        events = cursor.fetchall()

        if not events:
            print(f"No events found for game ID: {selected_game_id} in period {selected_period}.")
            return

        # Display events in a table
        table_events = PrettyTable()
        table_events.field_names = ["Play ID", "Event", "Period Time"]
        for event in events:
            table_events.add_row([event["play_id"], event["event"], event["periodTime"]])
        print(table_events)

    except Exception as e:
        print(f"An error occurred: {e}")
