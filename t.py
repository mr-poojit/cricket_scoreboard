# Importing external modules
import os
import time

# Constants
WELCOME_MSG = """\n\033[1mEnter which choice you want to use\033[0m
1. Read previous score
2. Add a new game
3. Remove previous saved score
4. Quit
"""
ENTER_NUMBER_ONLY_MSG = "Enter a number only"
CHOICE_PROMPT = "Enter the choice here: "

# Functions

# Function for adding team players in list
def add_player_names_in_team(team_name, how_many_players):
    team_players = []
    print()
    for i in range(how_many_players):
        player = input(f"Enter the {i + 1} player of {team_name}: ")
        team_players.append(player)
    return team_players

# Adding players name in file
def add_player_names_in_file(team_name, team_players, file):
    file.write(f"Team Name: {team_name}\n")
    for i, player in enumerate(team_players):
        file.write(f"{i + 1}: {player}\n")

# Handling each ball outcome
def handle_ball_outcome(choice, score, current_ball, wickets, extras, players):
    if choice == 1:
        runs = get_runs()
        score += runs
        current_ball += 1
    elif choice == 2:
        current_ball += 1
    elif choice == 3:
        current_ball += 1
        wickets += 1
        if wickets == players - 1:
            print("Sorry, but you are all out")
            return score, wickets, extras, current_ball, True
    elif choice == 4:
        extras += 1
        score += 1
    elif choice == 5:
        quit()
    else:
        print("Enter a valid value")
    return score, wickets, extras, current_ball, False

# Getting runs from the user
def get_runs():
    while True:
        try:
            runs = int(input("How many runs did the batsman score?\n"))
            return runs
        except ValueError:
            print(ENTER_NUMBER_ONLY_MSG)

# This function will execute every inning
def play_innings(team_name, file, overs, players):
    score = 0
    wickets = 0
    extras = 0
    current_ball = 1
    current_over = 1
    total_balls = overs * 6

    print(f"\n\033[1mInnings of {team_name} has started\033[0m")

    fall_of_wickets = []

    while current_ball <= total_balls:
        print("\n_______________________________")
        print(f"\033[1m\nStatus of ball {current_ball} (enter a number)\033[0m")
        print("""1. Runs
2. Dot ball
3. Wicket
4. Wide Ball/No Ball
5. Force Quit
""")
        while True:
            try:
                choice = int(input(CHOICE_PROMPT))
                break
            except ValueError:
                print(ENTER_NUMBER_ONLY_MSG)

        score, wickets, extras, current_ball, all_out = handle_ball_outcome(
            choice, score, current_ball, wickets, extras, players
        )

        if all_out:
            break

        if current_ball % 6 == 0:
            print(f"\n{current_over} over finished")
            current_over += 1

        if wickets > 0:
            fall_of_wickets.append((wickets, score))

    print(f"""\n\033[1mTotal Score of {team_name}\033[0m
\033[1mRuns: {score}\033[0m
\033[1mWickets: {wickets}\033[0m
\033[1mExtras: {extras}\033[0m
\033[1mRun Rate: {score / overs}\033[0m\n""")

    print("\033[1mFall of Wickets:\033[0m")
    for wicket, run in fall_of_wickets:
        print(f"{wicket} - {run}")

    file.write(f"""\nTotal Score of {team_name}\n
Runs: {score}\n
Wickets: {wickets}\n
Extras: {extras}\n
Run Rate: {score / overs}\n""")

    file.write("Fall of Wickets:\n")
    for wicket, run in fall_of_wickets:
        file.write(f"{wicket} - {run}\n")

    return score

# If team 1 is batting first
def team1_bat_first(team1_name, team2_name, file, overs, players):
    team1_score = play_innings(team1_name, file, overs,players)
    print("\033[1mInnings 1 finished\033[0m")
    required_runs = team1_score + 1
    print(f"\033[1m{team2_name} needs {required_runs} runs to win\033[0m")
    team2_score = play_innings(team2_name, file, overs, players)
    if team2_score >= required_runs:
        print(f"\033[1m{team2_name} wins\033[0m")
    else:
        print(f"\033[1m{team1_name} wins\033[0m")

# If team 2 is batting first
def team2_bat_first(team1_name, team2_name, file, overs, players):
    team2_score = play_innings(team2_name, file, overs, players)
    print("\033[1mInnings 1 finished\033[0m")
    required_runs = team2_score + 1
    print(f"\033[1m{team1_name} needs {required_runs} runs to win\033[0m")
    team1_score = play_innings(team1_name, file, overs, players)
    if team1_score >= required_runs:
        print(f"\033[1m{team1_name} wins\033[0m")
    else:
        print(f"\033[1m{team2_name} wins\033[0m")

# Function which will start the match
def start_match(bat_or_bowl, team1_name, team2_name, who_won_the_toss, file, overs, players):
    if who_won_the_toss == team1_name:
        if bat_or_bowl == "bat":
            team1_bat_first(team1_name, team2_name, file, overs, players)
        else:
            team2_bat_first(team1_name, team2_name, file, overs, players)
    elif who_won_the_toss == team2_name:
        if bat_or_bowl == "bat":
            team2_bat_first(team1_name, team2_name, file, overs, players)
        else:
            team1_bat_first(team1_name, team2_name, file, overs, players)

# For reading the previous score
def read_previous_score():
    try:
        with open('cricket.txt') as file:
            print("\n\033[1mScore\033[0m\n")
            all_content = file.read()
            print(all_content)
            print("______________________________________\n")
    except FileNotFoundError:
        print("\n\033[1mNo score exists\033[0m")
        print("_______________")

# For removing the previous score
def remove_previous_score():
    try:
        os.remove("cricket.txt")
        print("\033[1mPrevious Scores Removed\033[0m")
    except FileNotFoundError:
        print("\n\033[1mNo score exists\033[0m")
        print("______________")

# Starting of program
while True:
    print("\033[1m\nWelcome to our Cricket Scoreboard software\033[0m")
    print(WELCOME_MSG)

    while True:
        try:
            choice = int(input("Add the number: "))
            break
        except ValueError:
            print(ENTER_NUMBER_ONLY_MSG)
            print(WELCOME_MSG)

    if choice == 1:
        read_previous_score()

    elif choice == 2:
        team1_name = input("Enter team 1 name: ")
        team2_name = input("Enter team 2 name: ")

        toss_teams = [team1_name, team2_name]

        print()

        # How many players are playing
        while True:
            try:
                how_many_players = int(input("How many players are playing (from one team) in the match\n"))
                break
            except ValueError:
                print(ENTER_NUMBER_ONLY_MSG)

        # Team 1 player
        team1_players = add_player_names_in_team(team1_name, how_many_players)

        # Team 2 players
        team2_players = add_player_names_in_team(team2_name, how_many_players)

        # Putting team 1 player name in file
        file = open("cricket.txt", "a")
        add_player_names_in_file(team1_name, team1_players, file)

        # Putting team 2 player name in file
        add_player_names_in_file(team2_name, team2_players, file)

        # Asking how many over the match is
        print("__________________________________\n")
        while True:
            try:
                overs = int(input("Enter how many overs this match is\n"))
                break
            except ValueError:
                print(ENTER_NUMBER_ONLY_MSG)

        # Putting how many over match in file
        file.write(f"\nMatch overs: {overs}\n")

        # Doing the toss
        print("\nNow do the toss")
        time.sleep(5)
        for i, team in enumerate(toss_teams, start=1):
            print(f"{i}: {team}")

        while True:
            try:
                toss_winner = int(input("Who won the toss (Enter number)? "))
                if toss_winner not in [1, 2]:
                    print("Enter a valid number")
                else:
                    who_won_the_toss = toss_teams[toss_winner - 1]
                    break
            except ValueError:
                print(ENTER_NUMBER_ONLY_MSG)

        # Asking for the decision (bat or bowl)
        while True:
            bat_or_bowl = input(f"\nEnter what {who_won_the_toss} want to do (bat/bowl): ").lower()
            if bat_or_bowl not in ["bat", "bowl"]:
                print("Enter a valid value")
            else:
                break

        file.write(f"{who_won_the_toss} won the toss and chose to {bat_or_bowl}\n")
        print("\033[1mToss finished\033[0m\n")

        # Starting the match
        start_match(bat_or_bowl, team1_name, team2_name, who_won_the_toss, file, overs, how_many_players)
        file.close()

    elif choice == 3:
        remove_previous_score()

    elif choice == 4:
        break

    else:
        print("\n\033[1mEnter a valid number\033[0m")