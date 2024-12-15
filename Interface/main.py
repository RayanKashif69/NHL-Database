from game_statistics import game_statistics_menu
from team_performance_menu import team_performance_menu
from player_menu import player_performance_menu
from config_loader import connect_to_database
from main_menu import main_menu
from event_statistics import event_statistics_menu
from query_executor import execute_query


def season_rankings(connection):
    """Rank teams by total number of wins in the season, showing only the team names and ranks."""
    query = """
        SELECT T.teamName
        FROM team_info T
        JOIN game_teams_stats G ON T.team_id = G.team_id
        WHERE G.won = 1
        GROUP BY T.teamName
        ORDER BY COUNT(G.won) DESC;
    """
    try:
        cursor = connection.cursor(as_dict=True)
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            print("\nSeason Rankings (Teams Ranked by Total Wins):")
            print("+------+----------------------+")
            print("| Rank | Team Name            |")
            print("+------+----------------------+")
            # Enumerate the results to show rankings starting from 1
            for rank, result in enumerate(results, start=1):
                print(f"| {rank:<4} | {result['teamName']:<20} |")
            print("+------+----------------------+")
        else:
            print("No data found for season rankings.")
    except Exception as e:
        print(f"An error occurred while fetching season rankings: {e}")






def scratches_stats_menu(connection):
    """Display the Scratches Stats submenu and execute related queries."""
    while True:
        print("+---------------------------------------+")
        print("| Scratches Stats Queries               |")
        print("+---------------------------------------+")
        print("| 1. Total Scratches by Team            |")
        print("| 2. Most Scratched Players             |")
        print("| 3. Games with the Highest Scratches   |")
        print("| 4. Scratches by Position              |")
        print("| 5. Back to Main Menu                  |")
        print("+---------------------------------------+")
        
        choice = input("Enter your choice: ")

        if choice == '5':
            print("Returning to Main Menu...")
            break

        # Corrected queries
        queries = [
            # 1. Total Scratches by Team
            """
            SELECT 
                ti.teamName AS team_name, 
                COUNT(gs.player_id) AS total_scratches
            FROM 
                game_scratches gs
            JOIN 
                team_info ti ON gs.team_id = ti.team_id
            GROUP BY 
                ti.teamName
            ORDER BY 
                total_scratches DESC;
            """,
            # 2. Most Scratched Players
            """
            SELECT TOP 10
                pi.firstName AS first_name, 
                pi.lastName AS last_name, 
                COUNT(gs.game_id) AS times_scratched
            FROM 
                game_scratches gs
            JOIN 
                player_info pi ON gs.player_id = pi.player_id
            GROUP BY 
                pi.player_id, pi.firstName, pi.lastName
            ORDER BY 
                times_scratched DESC;
            """,
            # 3. Games with the Highest Scratches
            """
            SELECT TOP 10
                g.game_id, 
                g.date_time_GMT AS game_date, 
                COUNT(gs.player_id) AS total_scratches
            FROM 
                game_scratches gs
            JOIN 
                game g ON gs.game_id = g.game_id
            GROUP BY 
                g.game_id, g.date_time_GMT
            ORDER BY 
                total_scratches DESC;
            """,
            # 4. Scratches by Position
            """
            SELECT 
                pi.primaryPosition AS position, 
                COUNT(gs.player_id) AS total_scratches
            FROM 
                game_scratches gs
            JOIN 
                player_info pi ON gs.player_id = pi.player_id
            GROUP BY 
                pi.primaryPosition
            ORDER BY 
                total_scratches DESC;
            """
        ]

        # Execute the selected query
        if choice.isdigit() and 1 <= int(choice) <= 4:
            query = queries[int(choice) - 1]
            execute_query(connection, query)
        else:
            print("Invalid choice. Please select a valid option.")


def advanced_queries_menu(connection):
    """Display the Advanced Queries submenu and execute related queries."""
    while True:
        print("+-----------------------------------------+")
        print("| Advanced Analytics Queries              |")
        print("+-----------------------------------------+")
        print("| 1. Most Penalized Teams and Loss Rate   |")
        print("| 2. Clutch Goals in Final 5 Minutes      |")
        print("| 3. Top Assists between Player Pairs     |")
        print("| 4. Most Aggressive Teams                |")
        print("| 5. Back to Main Menu                    |")
        print("+-----------------------------------------+")
        
        choice = input("Enter your choice: ")

        if choice == '5':
            print("Returning to Main Menu...")
            break

        # Queries corresponding to each option
        queries = [
    # 1. Most Penalized Teams and Loss Rate
    """
    SELECT 
        t.teamName,
        AVG(gts.pim) AS avg_penalty_minutes,
        SUM(CASE WHEN gts.won = 1 THEN 0 ELSE 1 END) * 100.0 / COUNT(*) AS loss_percentage
    FROM 
        game_teams_stats gts
    JOIN 
        team_info t ON gts.team_id = t.team_id
    GROUP BY 
        t.teamName
    ORDER BY 
        loss_percentage DESC;
    """,
    
    # 2. Clutch Goals in Final 5 Minutes
    """
    WITH RankedGoals AS (
        SELECT 
            p.firstName,
            p.lastName,
            COUNT(*) AS clutch_goals,
            ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS row_num
        FROM 
            game_goals gg
        JOIN 
            Event e ON gg.play_id = e.play_id
        JOIN 
            Performs pf ON e.play_id = pf.play_id
        JOIN 
            player_info p ON pf.player_id = p.player_id
        WHERE 
            e.period = (SELECT MAX(period) FROM Event WHERE Event.game_id = e.game_id)
            AND e.periodTime >= (20 * 60 - 5 * 60)  -- Last 5 minutes of the period
        GROUP BY 
            p.firstName, p.lastName
    )
    SELECT TOP 10 * FROM RankedGoals;
    """,

    # 3. Top Assists Between Player Pairs
    """
    SELECT TOP 10
        a.firstName AS assister_firstName,
        a.lastName AS assister_lastName,
        b.firstName AS scorer_firstName,
        b.lastName AS scorer_lastName,
        COUNT(*) AS total_assists
    FROM 
        Performs pa
    JOIN 
        Performs pb ON pa.play_id = pb.play_id AND pa.player_id != pb.player_id
    JOIN 
        player_info a ON pa.player_id = a.player_id
    JOIN 
        player_info b ON pb.player_id = b.player_id
    WHERE 
        pa.playerType = 'Assist' AND pb.playerType = 'Scorer'
    GROUP BY 
        a.firstName, a.lastName, b.firstName, b.lastName
    ORDER BY 
        total_assists DESC;
    """,

    # 4. Most Aggressive Teams
    """
    SELECT TOP 10
        t.teamName,
        AVG(gts.hits) AS avg_hits,
        AVG(gts.pim) AS avg_penalty_minutes,
        (AVG(gts.hits) + AVG(gts.pim)) AS aggression_score
    FROM 
        game_teams_stats gts
    JOIN 
        team_info t ON gts.team_id = t.team_id
    GROUP BY 
        t.teamName
    ORDER BY 
        aggression_score DESC;
    """
]


        # Execute the selected query
        if choice.isdigit() and 1 <= int(choice) <= 4:
            query = queries[int(choice) - 1]
            execute_query(connection, query)
        else:
            print("Invalid choice. Please select a valid option.")







def main():
    """Main function to handle the interface."""
    # Connect to the database
    connection = connect_to_database()
    if not connection:
        print("Failed to connect to the database. Exiting.")
        return  # Exit if connection fails

    while True:
        # Display the main menu
        choice = main_menu()
        if choice == '1':  # Player Performance Queries
            player_performance_menu(connection)
        elif choice == '2':  # Team Performance Queries
            team_performance_menu(connection)
        elif choice == '3':  # Game Statistics Queries
            game_statistics_menu(connection)
        elif choice == '4':  # Event Statistics Queries
            event_statistics_menu(connection)
        elif choice == '5':  # List All Teams
            query = "SELECT team_id, teamName FROM team_info ORDER BY teamName ASC;"
            execute_query(connection, query)
        elif choice == '6':  # Season Rankings
            season_rankings(connection)
        elif choice == '7':  # Scratches Data
            scratches_stats_menu(connection)
        elif choice == '8':  # Advanced Analytics Queries
           advanced_queries_menu(connection)
        elif choice == '9':  # Exit
            print("Exiting the program. Goodbye!")
            break
    

        else:
            print("Invalid choice. Please select a valid option.")

    # Close the database connection
    connection.close()

if __name__ == "__main__":
    main()
