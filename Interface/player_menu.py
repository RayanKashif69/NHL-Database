from query_executor import execute_query


def general_stats_menu(connection):
    """Display the General Stats submenu and execute queries with prepared statements."""
    while True:
        print("+---------------------------------------+")
        print("| General Stats Queries                 |")
        print("+---------------------------------------+")
        print("| 1. Top Scorers                        |")
        print("| 2. Most Penalty Minutes by Team       |")
        print("| 3. Most Game-Winning Goals            |")
        print("| 4. Top Performers by Birth City       |")
        print("| 5. Most Assists in Power Play         |")
        print("| 6. Best Face-Off Win Percentage       |")
        print("| 7. Most Time on Ice                   |")
        print("| 8. Best Save Percentage               |")
        print("| 9. Most Takeaways                     |")
        print("| 10. Back to Player Performance Menu   |")
        print("+---------------------------------------+")
        
        choice = input("Enter your choice: ")

        if choice == '10':
            print("Returning to Player Performance Menu...")
            break

        # Mapping of queries
        queries = [
            # 1. Top Scorers
            """
            SELECT TOP 10
                pi.firstName, 
                pi.lastName, 
                SUM(gss.goals) AS total_goals
            FROM 
                game_skater_stats gss
            JOIN 
                player_info pi ON gss.player_id = pi.player_id
            JOIN 
                game g ON gss.game_id = g.game_id
            GROUP BY 
                pi.firstName, pi.lastName
            ORDER BY 
                total_goals DESC;
            """,
            # 2. Most Penalty Minutes by Team
            """
            SELECT TOP 10
                ti.teamName,
                pi.firstName,
                pi.lastName,
                SUM(gss.penaltyMinutes) AS total_penalty_minutes
            FROM 
                game_skater_stats gss
            JOIN 
                player_info pi ON gss.player_id = pi.player_id
            JOIN 
                team_info ti ON gss.team_id = ti.team_id
            GROUP BY 
                ti.teamName, pi.firstName, pi.lastName
            ORDER BY 
                total_penalty_minutes DESC;
            """,
            # 3. Most Game-Winning Goals
            """
            SELECT TOP 10
                pi.firstName,
                pi.lastName,
                COUNT(gg.play_id) AS game_winning_goals
            FROM 
                game_goals gg
            JOIN 
                Performs p ON gg.play_id = p.play_id
            JOIN 
                player_info pi ON p.player_id = pi.player_id
            WHERE 
                gg.gameWinningGoal = 1
            GROUP BY 
                pi.firstName, pi.lastName
            ORDER BY 
                game_winning_goals DESC;
            """,
            # 4. Top Performers by Birth City
            """
            SELECT TOP 10
                pi.birthCity,
                pi.firstName,
                pi.lastName,
                SUM(gss.goals) AS total_goals
            FROM 
                game_skater_stats gss
            JOIN 
                player_info pi ON gss.player_id = pi.player_id
            GROUP BY 
                pi.birthCity, pi.firstName, pi.lastName
            HAVING 
                SUM(gss.goals) > 10
            ORDER BY 
                total_goals DESC;
            """,
            # 5. Most Assists in Power Play
            """
            SELECT TOP 10
                pi.firstName,
                pi.lastName,
                SUM(gss.powerPlayAssists) AS total_power_play_assists
            FROM 
                game_skater_stats gss
            JOIN 
                player_info pi ON gss.player_id = pi.player_id
            GROUP BY 
                pi.firstName, pi.lastName
            ORDER BY 
                total_power_play_assists DESC;
            """,
            # 6. Best Face-Off Win Percentage
            """
            SELECT TOP 10
                pi.firstName,
                pi.lastName,
                SUM(gss.faceOffWins) AS total_face_off_wins,
                SUM(gss.faceoffTaken) AS total_faceoffs_taken,
                (SUM(gss.faceOffWins) * 100.0 / SUM(gss.faceoffTaken)) AS win_percentage
            FROM 
                game_skater_stats gss
            JOIN 
                player_info pi ON gss.player_id = pi.player_id
            GROUP BY 
                pi.firstName, pi.lastName
            HAVING 
                SUM(gss.faceoffTaken) > 50
            ORDER BY 
                win_percentage DESC;
            """,
            # 7. Most Time on Ice
            """
            SELECT TOP 10
                pi.firstName,
                pi.lastName,
                SUM(gss.timeOnIce) AS total_time_on_ice
            FROM 
                game_skater_stats gss
            JOIN 
                player_info pi ON gss.player_id = pi.player_id
            GROUP BY 
                pi.firstName, pi.lastName
            ORDER BY 
                total_time_on_ice DESC;
            """,
            # 8. Best Save Percentage
            """
            SELECT TOP 10
                pi.firstName,
                pi.lastName,
                SUM(ggs.saves) AS total_saves,
                SUM(ggs.shots) AS total_shots,
                (SUM(ggs.saves) * 100.0 / SUM(ggs.shots)) AS save_percentage
            FROM 
                game_goalie_stats ggs
            JOIN 
                player_info pi ON ggs.player_id = pi.player_id
            GROUP BY 
                pi.firstName, pi.lastName
            HAVING 
                SUM(ggs.shots) >= 100
            ORDER BY 
                save_percentage DESC;
            """,
            # 9. Most Takeaways
            """
            SELECT TOP 10
                pi.firstName,
                pi.lastName,
                SUM(gss.takeaways) AS total_takeaways
            FROM 
                game_skater_stats gss
            JOIN 
                player_info pi ON gss.player_id = pi.player_id
            GROUP BY 
                pi.firstName, pi.lastName
            ORDER BY 
                total_takeaways DESC;
            """
        ]

        # Validate and execute the selected query
        if choice.isdigit() and 1 <= int(choice) <= 9:
            query = queries[int(choice) - 1]
            execute_query(connection, query, parameters=())  # No parameters are passed in these queries
        else:
            print("Invalid choice. Please select a valid option.")




def advanced_search_menu(connection):
    """Display the Advanced Search Menu."""
    while True:
        print("+---------------------------------------+")
        print("| Advanced Search                      |")
        print("+---------------------------------------+")
        
        # Step 1: List all teams (only displayed once)
        query_teams = """
        SELECT 
            team_id, 
            teamName 
        FROM 
            team_info
        ORDER BY 
            teamName ASC;
        """
        print("Fetching list of teams...")
        execute_query(connection, query_teams)

        # Step 2: Choose a team
        team_id = input("Enter the Team ID to view its players (or type 'back' to return): ").strip()
        if team_id.lower() == 'back':
            break
        
        while True:  # Loop for player selection and stats
            # Step 3: List players for the selected team
            query_players = """
            SELECT 
                pi.player_id, 
                CONCAT(pi.firstName, ' ', pi.lastName) AS fullName
            FROM 
                player_info pi
            JOIN 
                game_skater_stats gss ON pi.player_id = gss.player_id
            WHERE 
                gss.team_id = %s
            GROUP BY 
                pi.player_id, pi.firstName, pi.lastName
            ORDER BY 
                fullName ASC;
            """
            print(f"Fetching players for Team ID: {team_id}")
            execute_query(connection, query_players, parameters=(team_id,))

            # Step 4: Choose a player
            player_id = input("Enter the Player ID to view stats (or type 'back' to return to team selection): ").strip()
            if player_id.lower() == 'back':
                break

            # Step 5: Show aggregated season stats for the player
            query_player_stats = """
            SELECT 
                g.season,
                SUM(gss.goals) AS total_goals,
                SUM(gss.assists) AS total_assists,
                SUM(gss.shots) AS total_shots,
                SUM(gss.hits) AS total_hits,
                SUM(gss.penaltyMinutes) AS total_penalty_minutes,
                SUM(gss.powerPlayGoals) AS power_play_goals,
                SUM(gss.shortHandedGoals) AS short_handed_goals,
                SUM(gss.takeaways) AS total_takeaways,
                SUM(gss.giveaways) AS total_giveaways
            FROM 
                game_skater_stats gss
            JOIN 
                game g ON gss.game_id = g.game_id
            WHERE 
                gss.player_id = %s
            GROUP BY 
                g.season
            ORDER BY 
                g.season DESC;
            """
            print(f"Fetching aggregated season stats for Player ID: {player_id}")
            execute_query(connection, query_player_stats, parameters=(player_id,))
            input("\nPress Enter to return to the player list...\n")



def player_performance_menu(connection):
    """Display the Player Performance Queries submenu."""
    while True:
        print("+---------------------------------------+")
        print("| Player Performance Queries            |")
        print("+---------------------------------------+")
        print("| 1. General Stats                      |")
        print("| 2. Advanced Search                    |")
        print("| 3. Back to Main Menu                  |")
        print("+---------------------------------------+")
        
        choice = input("Enter your choice: ")

        if choice == '3':
            print("Returning to Main Menu...")
            break
        elif choice == '1':
            general_stats_menu(connection)
        elif choice == '2':
            advanced_search_menu(connection)  # Call Advanced Search Menu
        else:
            print("Invalid choice. Please select a valid option.")
