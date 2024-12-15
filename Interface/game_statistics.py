

import sys
sys.path.insert(0, "dependencies")  # Add the dependencies folder to the search path


from query_executor import execute_query
from prettytable import PrettyTable


def execute_query(connection, query, parameters=()):
    """Execute a parameterized SQL query and print the results."""
    try:
        cursor = connection.cursor(as_dict=True)
        cursor.execute(query, parameters)
        results = cursor.fetchall()

        if not results:
            print("No data found.")
            return

        # Dynamically create a table with column names from query results
        table = PrettyTable()
        table.field_names = results[0].keys()  # Column names are the keys of the first row

        for row in results:
            table.add_row(row.values())  # Add row values to the table

        print(table)
    except Exception as e:
        print("Failed to execute query. Error:", e)


def game_statistics_menu(connection):
    """Display the Game Statistics Queries submenu."""
    while True:
        print("+---------------------------------------+")
        print("| Game Statistics Queries               |")
        print("+---------------------------------------+")
        print("| 1. Top Games with Highest Total Shots |")
        print("| 2. Games with Most Hits Combined      |")
        print("| 3. Games with Most Power Play Chances |")
        print("| 4. Most One-Sided Wins                |")
        print("| 5. Advanced Search                    |")  # New Advanced Search option
        print("| 6. Back to Main Menu                  |")
        print("+---------------------------------------+")

        choice = input("Enter your choice: ")

        if choice == '6':
            print("Returning to Main Menu...")
            break

        queries = [
            # 1. Top Games with Highest Total Shots
            """
            SELECT TOP 10
                g.game_id,
                g.date_time_GMT,
                (gts_away.shots + gts_home.shots) AS total_shots,
                ti_away.teamName AS away_team,
                ti_home.teamName AS home_team
            FROM 
                game g
            JOIN 
                game_teams_stats gts_away ON g.game_id = gts_away.game_id AND gts_away.HoA = 'away'
            JOIN 
                game_teams_stats gts_home ON g.game_id = gts_home.game_id AND gts_home.HoA = 'home'
            JOIN 
                team_info ti_away ON gts_away.team_id = ti_away.team_id
            JOIN 
                team_info ti_home ON gts_home.team_id = ti_home.team_id
            ORDER BY 
                total_shots DESC;
            """,
            # 2. Games with Most Hits Combined
            """
            SELECT TOP 10
                g.game_id,
                g.date_time_GMT,
                (gts_away.hits + gts_home.hits) AS total_hits,
                ti_away.teamName AS away_team,
                ti_home.teamName AS home_team
            FROM 
                game g
            JOIN 
                game_teams_stats gts_away ON g.game_id = gts_away.game_id AND gts_away.HoA = 'away'
            JOIN 
                game_teams_stats gts_home ON g.game_id = gts_home.game_id AND gts_home.HoA = 'home'
            JOIN 
                team_info ti_away ON gts_away.team_id = ti_away.team_id
            JOIN 
                team_info ti_home ON gts_home.team_id = ti_home.team_id
            ORDER BY 
                total_hits DESC;
            """,
            # 3. Games with Most Power Play Opportunities
            """
            SELECT TOP 10
                g.game_id,
                g.date_time_GMT,
                (gts_away.powerPlayOpportunities + gts_home.powerPlayOpportunities) AS total_power_play_opportunities,
                ti_away.teamName AS away_team,
                ti_home.teamName AS home_team
            FROM 
                game g
            JOIN 
                game_teams_stats gts_away ON g.game_id = gts_away.game_id AND gts_away.HoA = 'away'
            JOIN 
                game_teams_stats gts_home ON g.game_id = gts_home.game_id AND gts_home.HoA = 'home'
            JOIN 
                team_info ti_away ON gts_away.team_id = ti_away.team_id
            JOIN 
                team_info ti_home ON gts_home.team_id = ti_home.team_id
            ORDER BY 
                total_power_play_opportunities DESC;
            """,
            # 4. Most One-Sided Wins
            """
            SELECT TOP 10
                g.game_id,
                g.date_time_GMT,
                ABS(gts_away.goals - gts_home.goals) AS goal_difference,
                ti_away.teamName AS away_team,
                ti_home.teamName AS home_team
            FROM 
                game g
            JOIN 
                game_teams_stats gts_away ON g.game_id = gts_away.game_id AND gts_away.HoA = 'away'
            JOIN 
                game_teams_stats gts_home ON g.game_id = gts_home.game_id AND gts_home.HoA = 'home'
            JOIN 
                team_info ti_away ON gts_away.team_id = ti_away.team_id
            JOIN 
                team_info ti_home ON gts_home.team_id = ti_home.team_id
            ORDER BY 
                goal_difference DESC;
            """
        ]

        # Validate and execute the selected query
        if choice.isdigit() and 1 <= int(choice) <= 4:
            query = queries[int(choice) - 1]
            execute_query(connection, query)
        elif choice == '5':  # Advanced Search
            while True:
                # Display all teams
                print("\nDisplaying all teams:")
                query = """
                    SELECT team_id, teamName
                    FROM team_info
                    ORDER BY teamName ASC;
                """
                execute_query(connection, query)

                # Ask user to select a team
                team_id = input("\nEnter the team_id for detailed search: ")

                # Display all games played by the selected team
                print(f"\nDisplaying all games for team_id: {team_id}")
                query = """
                    SELECT g.game_id, g.date_time_GMT, g.outcome, g.type, v.venue
                    FROM game g
                    JOIN Venue v ON g.venue_ID = v.venue_ID
                    JOIN game_teams_stats gts ON g.game_id = gts.game_id
                    WHERE gts.team_id = %s
                    ORDER BY g.date_time_GMT DESC;
                """
                cursor = connection.cursor(as_dict=True)
                cursor.execute(query, (team_id,))
                results = cursor.fetchall()

                if not results:
                    print(f"No games played by team with team_id: {team_id}. Please select another team.")
                    continue  # Ask the user to select another team

                # Display the games
                table = PrettyTable()
                table.field_names = ["game_id", "date_time_GMT", "outcome", "type", "venue"]
                for row in results:
                    table.add_row(row.values())
                print(table)

                # Ask user to select a game
                game_id = input("\nEnter the game_id for detailed stats: ")

                # Display detailed stats for the selected game and team
                print(f"\nDisplaying detailed stats for game_id: {game_id} and team_id: {team_id}")
                query = """
                    SELECT gts.HoA, gts.won, gts.goals, gts.shots, gts.hits, gts.pim, gts.blocked,
                           gts.powerPlayOpportunities, gts.powerPlayGoals, gts.faceOffWinPercentage,
                           gts.takeaways, gts.giveaways, gts.startRinkSide
                    FROM game_teams_stats gts
                    WHERE gts.game_id = %s AND gts.team_id = %s;
                """
                execute_query(connection, query, (game_id, team_id))
                break  # Exit the Advanced Search loop
        else:
            print("Invalid choice. Please select a valid option.")
