from query_executor import execute_query

def team_performance_menu(connection):
    """Display the Team Performance Queries submenu."""
    while True:
        print("+---------------------------------------+")
        print("| Team Performance Queries              |")
        print("+---------------------------------------+")
        print("| 1. Teams with Most Goals              |")
        print("| 2. Teams with Best Defense            |")
        print("| 3. Teams with Most Penalty Minutes    |")
        print("| 4. Teams with Best Power Play         |")
        print("| 5. Teams with Best Faceoff Win Rate   |")
        print("| 6. Teams with Most Hits               |")
        print("| 7. Teams with Most Shutouts           |")
        print("| 8. Team Schedule                      |")
        print("| 9. Back to Main Menu                  |")
        print("+---------------------------------------+")

        choice = input("Enter your choice: ")

        if choice == '9':
            print("Returning to Main Menu...")
            break

        queries = [
            # 1. Teams with Most Goals
            """
            SELECT 
                ti.teamName, 
                SUM(gts.goals) AS total_goals
            FROM 
                game_teams_stats gts
            JOIN 
                team_info ti ON gts.team_id = ti.team_id
            GROUP BY 
                ti.teamName
            ORDER BY 
                total_goals DESC;
            """,
            # 2. Teams with Best Defense (Fewest Goals Against)
            """
            SELECT 
                ti.teamName, 
                SUM(gts.goals) AS goals_conceded
            FROM 
                game_teams_stats gts
            JOIN 
                team_info ti ON gts.team_id = ti.team_id
            WHERE 
                gts.HoA = 'away'
            GROUP BY 
                ti.teamName
            ORDER BY 
                goals_conceded ASC;
            """,
            # 3. Teams with Most Penalty Minutes
            """
            SELECT 
                ti.teamName, 
                SUM(gts.pim) AS total_penalty_minutes
            FROM 
                game_teams_stats gts
            JOIN 
                team_info ti ON gts.team_id = ti.team_id
            GROUP BY 
                ti.teamName
            ORDER BY 
                total_penalty_minutes DESC;
            """,
            # 4. Teams with Best Power Play (Most Power Play Goals)
            """
            SELECT 
                ti.teamName, 
                SUM(gts.powerPlayGoals) AS total_power_play_goals,
                SUM(gts.powerPlayOpportunities) AS power_play_opportunities,
                (SUM(gts.powerPlayGoals) * 100.0 / SUM(gts.powerPlayOpportunities)) AS power_play_percentage
            FROM 
                game_teams_stats gts
            JOIN 
                team_info ti ON gts.team_id = ti.team_id
            GROUP BY 
                ti.teamName
            ORDER BY 
                power_play_percentage DESC;
            """,
            # 5. Teams with Best Faceoff Win Rate
            """
            SELECT 
                ti.teamName, 
                AVG(gts.faceOffWinPercentage) AS average_faceoff_win_rate
            FROM 
                game_teams_stats gts
            JOIN 
                team_info ti ON gts.team_id = ti.team_id
            GROUP BY 
                ti.teamName
            ORDER BY 
                average_faceoff_win_rate DESC;
            """,
            # 6. Teams with Most Hits
            """
            SELECT 
                ti.teamName, 
                SUM(gts.hits) AS total_hits
            FROM 
                game_teams_stats gts
            JOIN 
                team_info ti ON gts.team_id = ti.team_id
            GROUP BY 
                ti.teamName
            ORDER BY 
                total_hits DESC;
            """,
            # 7. Teams with Most Shutouts
            """
            SELECT 
                ti.teamName, 
                COUNT(*) AS total_shutouts
            FROM 
                game_goalie_stats ggs
            JOIN 
                team_info ti ON ggs.team_id = ti.team_id
            WHERE 
                ggs.goals = 0
            GROUP BY 
                ti.teamName
            ORDER BY 
                total_shutouts DESC;
            """,
            # 8. Team Schedule
            """
            SELECT 
                g.game_id, 
                CASE 
                    WHEN g.away_team_id = ti.team_id THEN (SELECT teamName FROM team_info WHERE team_id = g.home_team_id)
                    ELSE (SELECT teamName FROM team_info WHERE team_id = g.away_team_id)
                END AS opponent,
                g.date_time_GMT AS game_date,
                v.venue AS venue,
                g.outcome AS game_outcome
            FROM 
                game g
            JOIN 
                team_info ti ON ti.team_id = %s
            LEFT JOIN 
                Venue v ON g.venue_ID = v.venue_ID
            WHERE 
                g.away_team_id = ti.team_id OR g.home_team_id = ti.team_id
            ORDER BY 
                g.date_time_GMT;
            """
        ]

        # If choice is 8, handle the Team Schedule
        if choice == '8':
            # Show all teams and ask for a team_id input
            print("Available Teams:")
            teams_query = """
            SELECT team_id, teamName FROM team_info;
            """
            execute_query(connection, teams_query)
            team_id = input("Enter the team_id to view the schedule: ")

            # Validate team_id input and execute the Team Schedule query
            if team_id.isdigit():
                schedule_query = queries[7]
                execute_query(connection, schedule_query, (team_id,))
            else:
                print("Invalid team ID. Please try again.")
        
        # Validate and execute the selected query using prepared statements
        elif choice.isdigit() and 1 <= int(choice) <= 7:
            query = queries[int(choice) - 1]
            execute_query(connection, query)
        else:
            print("Invalid choice. Please select a valid option.")
