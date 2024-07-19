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

def add_player_names_in_team(team_name, how_many_players):
    team_players = []
    print()
    for i in range(how_many_players):
        player = input(f"Enter the {i + 1} player of {team_name}: ")
        team_players.append(player)
    return team_players

def add_player_names_in_file(team_name, team_players, file):
    file.write(f"Team Name: {team_name}\n")
    for i, player in enumerate(team_players):
        file.write(f"{i + 1}: {player}\n")

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

def get_runs():
    while True:
        try:
            runs = int(input("How many runs did the batsman score?\n"))
            return runs
        except ValueError:
            print(ENTER_NUMBER_ONLY_MSG)

def display_over_summary(current_over, score, wickets, runs_this_over):
    print(f"\n\033[1mEnd of Over {current_over}\033[0m")
    print(f"Score: {score}/{wickets}")
    print(f"Runs this over: {runs_this_over}")
    return f"{current_over:2d} | {score:3d}/{wickets:<2d} | {runs_this_over:2d}\n"

def play_innings(team_name, file, overs, players, target=None):
    score = 0
    wickets = 0
    extras = 0
    current_ball = 1
    current_over = 1
    total_balls = overs * 6
    runs_this_over = 0
    over_summaries = [f"{'Over':^4}|{'Score':^7}|{'Runs':^5}\n{'-'*18}\n"]

    print(f"\n\033[1mInnings of {team_name} has started\033[0m")
    if target:
        print(f"\033[1mTarget: {target}\033[0m")

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

        previous_score = score
        score, wickets, extras, current_ball, all_out = handle_ball_outcome(
            choice, score, current_ball, wickets, extras, players
        )
        runs_this_over += score - previous_score

        if all_out:
            break

        if target and score >= target:
            print(f"\n\033[1m{team_name} has reached the target!\033[0m")
            break

        if current_ball % 6 == 0:
            over_summary = display_over_summary(current_over, score, wickets, runs_this_over)
            over_summaries.append(over_summary)
            current_over += 1
            runs_this_over = 0

    innings_summary = f"""\n\033[1mTotal Score of {team_name}\033[0m
\033[1mRuns: {score}\033[0m
\033[1mWickets: {wickets}\033[0m
\033[1mExtras: {extras}\033[0m
\033[1mOvers: {(current_ball-1) // 6}.{(current_ball-1) % 6}\033[0m
\033[1mRun Rate: {score / ((current_ball-1) / 6):.2f}\033[0m\n"""

    print(innings_summary)
    file.write(innings_summary)
    
    print("\n\033[1mOver-by-over summary:\033[0m")
    print(''.join(over_summaries))
    file.write("\nOver-by-over summary:\n")
    file.write(''.join(over_summaries))
    
    return score, wickets

def team1_bat_first(team1_name, team2_name, file, overs, players):
    team1_score, team1_wickets = play_innings(team1_name, file, overs, players)
    print("\033[1mInnings 1 finished\033[0m")
    team2_score, team2_wickets = play_innings(team2_name, file, overs, players, target=team1_score+1)
    return team1_score, team1_wickets, team2_score, team2_wickets

def team2_bat_first(team1_name, team2_name, file, overs, players):
    team2_score, team2_wickets = play_innings(team2_name, file, overs, players)
    print("\033[1mInnings 1 finished\033[0m")
    team1_score, team1_wickets = play_innings(team1_name, file, overs, players, target=team2_score+1)
    return team1_score, team1_wickets, team2_score, team2_wickets

def determine_winner(team1_name, team1_score, team2_name, team2_score):
    if team1_score > team2_score:
        return f"{team1_name} won by {team1_score - team2_score} runs"
    elif team2_score > team1_score:
        return f"{team2_name} won by {10 - team2_wickets} wickets"
    else:
        return "The match ended in a tie"

def display_final_scores(team1_name, team1_score, team1_wickets, team2_name, team2_score, team2_wickets, file):
    final_scores = f"""
\033[1mFinal Scores:\033[0m
╔{'═'*15}╦{'═'*10}╗
║{'Team':^15}║{'Score':^10}║
╠{'═'*15}╬{'═'*10}╣
║{team1_name:^15}║{f'{team1_score}/{team1_wickets}':^10}║
║{team2_name:^15}║{f'{team2_score}/{team2_wickets}':^10}║
╚{'═'*15}╩{'═'*10}╝
"""
    print(final_scores)
    file.write(final_scores)

def start_match(bat_or_bowl, team1_name, team2_name, who_won_the_toss, file, overs, players):
    if who_won_the_toss == team1_name:
        if bat_or_bowl == "bat":
            team1_score, team1_wickets, team2_score, team2_wickets = team1_bat_first(team1_name, team2_name, file, overs, players)
        else:
            team2_score, team2_wickets, team1_score, team1_wickets = team2_bat_first(team1_name, team2_name, file, overs, players)
    elif who_won_the_toss == team2_name:
        if bat_or_bowl == "bat":
            team2_score, team2_wickets, team1_score, team1_wickets = team2_bat_first(team1_name, team2_name, file, overs, players)
        else:
            team1_score, team1_wickets, team2_score, team2_wickets = team1_bat_first(team1_name, team2_name, file, overs, players)

    display_final_scores(team1_name, team1_score, team1_wickets, team2_name, team2_score, team2_wickets, file)

    result = determine_winner(team1_name, team1_score, team2_name, team2_score)
    print(f"\n\033[1m{result}\033[0m")
    file.write(f"\n{result}\n")

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

def remove_previous_score():
    try:
        os.remove("cricket.txt")
        print("\033[1mPrevious Scores Removed\033[0m")
    except FileNotFoundError:
        print("\n\033[1mNo score exists\033[0m")
        print("______________")

# Main program
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

        while True:
            try:
                how_many_players = int(input("How many players are playing (from one team) in the match\n"))
                break
            except ValueError:
                print(ENTER_NUMBER_ONLY_MSG)

        team1_players = add_player_names_in_team(team1_name, how_many_players)
        team2_players = add_player_names_in_team(team2_name, how_many_players)

        file = open("cricket.txt", "a")
        add_player_names_in_file(team1_name, team1_players, file)
        add_player_names_in_file(team2_name, team2_players, file)

        print("__________________________________\n")
        while True:
            try:
                overs = int(input("Enter how many overs this match is\n"))
                break
            except ValueError:
                print(ENTER_NUMBER_ONLY_MSG)

        file.write(f"\nMatch overs: {overs}\n")

        print("\nNow do the toss")
        time.sleep(2)
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

        while True:
            bat_or_bowl = input(f"\nEnter what {who_won_the_toss} want to do (bat/bowl): ").lower()
            if bat_or_bowl not in ["bat", "bowl"]:
                print("Enter a valid value")
            else:
                break

        file.write(f"{who_won_the_toss} won the toss and chose to {bat_or_bowl}\n")
        print("\033[1mToss finished\033[0m\n")

        start_match(bat_or_bowl, team1_name, team2_name, who_won_the_toss, file, overs, how_many_players)
        file.close()

    elif choice == 3:
        remove_previous_score()

    elif choice == 4:
        break

    else:
        print("\n\033[1mEnter a valid number\033[0m")