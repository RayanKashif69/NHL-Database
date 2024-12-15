import re

# Correct order of table inserts
table_order = [
    "TimeZone",
    "Venue",
    "TeamName",
    "player_info",
    "OfficialInfo",
    "team_info",
    "game",
    "event",
    "Officiates",
    "game_skater_stats",
    "game_goalie_stats",
    "game_scratches",
    "game_teams_stats",
    "game_goals",
    "game_penalties",
    "Performs"
]

# Function to parse INSERT statements by table name
def parse_insert_statements(file_path):
    insert_statements = {table: [] for table in table_order}
    pattern = re.compile(r"INSERT INTO (\w+)\s+VALUES", re.IGNORECASE)
    
    current_table = None
    current_statement = []
    
    with open(file_path, "r") as file:
        for line in file:
            # Check if the line starts a new INSERT statement
            match = pattern.match(line)
            if match:
                # Save the current statement to the corresponding table
                if current_table and current_statement:
                    insert_statements[current_table].append("".join(current_statement))
                
                # Start a new statement
                current_table = match.group(1)
                current_statement = [line]
            elif current_table:
                # Continue building the current statement
                current_statement.append(line)
        
        # Save the last statement
        if current_table and current_statement:
            insert_statements[current_table].append("".join(current_statement))
    
    return insert_statements

# Function to write the sorted INSERT statements to a file
def write_sorted_inserts(insert_statements, output_file):
    with open(output_file, "w") as f:
        for table in table_order:
            if insert_statements[table]:
                f.write(f"-- Inserts for {table} --\n")
                for statement in insert_statements[table]:
                    f.write(statement + "\n")
                f.write("\n")

# Main logic
def rearrange_insert_statements(input_file, output_file):
    insert_statements = parse_insert_statements(input_file)
    write_sorted_inserts(insert_statements, output_file)

# Input and output files
input_sql_file = "dump.sql"
output_sql_file = "sorted_nhl2.sql"

# Run the script
rearrange_insert_statements(input_sql_file, output_sql_file)
print(f"Sorted INSERT statements have been written to {output_sql_file}")
