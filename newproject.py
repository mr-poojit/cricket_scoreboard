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

def add_player_names_in_team(team_name, how_many_players):
    team_players = []
    print()
    for i in range(how_many_players):
        player = input(f"Enter the {i + 1} player of {team_name}: ")
        team_players.append(player)
    return team_players

def add_player_names_in_file(team_name, team_players, file):
    file.write(f"Team Name: {team_name}\n")
    for i, player in enumerate(team_players, 1):
        file.write(f"{i}: {player}\n")

def get_runs():
    while True:
        try:
            runs = int(input("How many runs did the batsman score? "))
            if runs < 0:
                print("Runs cannot be negative. Please enter a valid number.")
            else:
                return runs
        except ValueError:
            print(ENTER_NUMBER_ONLY_MSG)

def handle_ball_outcome(choice, score, current_ball, wickets, extras, players):
    all_out = False
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
            print("All out!")
            all_out = True
    elif choice == 4:
        extras += 1
        score += 1
    else:
        print("Enter a valid value")
        return score, wickets, extras, current_ball, False
    return score, wickets, extras, current_ball, all_out

def display_over_summary(current_over, score, wickets, runs_this_over):
    print(f"\n\033[1mEnd of Over {current_over}\033[0m")
    print(f"Score: {score}/{wickets}")
    print(f"Runs this over: {runs_this_over}")

def display_over_wise_scores(team_name, over_scores, file):
    print(f"\n\033[1mOver-wise Scores for {team_name}:\033[0m")
    file.write(f"\nOver-wise Scores for {team_name}:\n")
    
    max_digits = max(len(str(score)) for score in over_scores)
    
    header = "Over | Score"
    print(header)
    print("-" * len(header))
    file.write(f"{header}\n{'-' * len(header)}\n")
    
    for i, score in enumerate(over_scores, 1):
        print(f"{i:4d} | {score:{max_digits}d}")
        file.write(f"{i:4d} | {score:{max_digits}d}\n")
    print()
    file.write("\n")

def play_innings(team_name, file, overs, players, target=None):
    score = 0
    wickets = 0
    extras = 0
    current_ball = 0
    total_balls = overs * 6
    runs_this_over = 0
    over_scores = []

    print(f"\n\033[1mInnings of {team_name} has started\033[0m")

    while current_ball < total_balls:
        current_over = current_ball // 6 + 1
        if current_ball % 6 == 0 and current_ball > 0:
            display_over_summary(current_over - 1, score, wickets, runs_this_over)
            over_scores.append(runs_this_over)
            runs_this_over = 0

        print("\n_______________________________")
        print(f"\033[1m\nStatus of ball {current_ball % 6 + 1} of over {current_over} (enter a number)\033[0m")
        print("""1. Runs
2. Dot ball
3. Wicket
4. Wide Ball/No Ball
5. Force Quit
""")
        while True:
            try:
                choice = int(input(CHOICE_PROMPT))
                if choice == 5:
                    return score, wickets, current_ball
                if 1 <= choice <= 4:
                    break
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print(ENTER_NUMBER_ONLY_MSG)

        previous_score = score
        score, wickets, extras, current_ball, all_out = handle_ball_outcome(
            choice, score, current_ball, wickets, extras, players
        )
        runs_this_over += score - previous_score

        if all_out:
            over_scores.append(runs_this_over)
            break

        if target and score >= target:
            over_scores.append(runs_this_over)
            current_ball += 1  # Increment to count the winning ball
            break

    if runs_this_over > 0:
        over_scores.append(runs_this_over)

    innings_summary = f"""\n\033[1mTotal Score of {team_name}\033[0m
\033[1mRuns: {score}\033[0m
\033[1mWickets: {wickets}\033[0m
\033[1mExtras: {extras}\033[0m
\033[1mOvers: {current_ball // 6}.{current_ball % 6}\033[0m
\033[1mRun Rate: {score / (current_ball / 6):.2f}\n"""

    print(innings_summary)
    file.write(innings_summary)

    display_over_wise_scores(team_name, over_scores, file)

    return score, wickets, current_ball

def determine_winner(team1_name, team1_score, team2_name, team2_score, team2_wickets, balls_left):
    if team1_score > team2_score:
        return f"{team1_name} won by {team1_score - team2_score} runs"
    elif team2_score > team1_score:
        wickets_left = 10 - team2_wickets - 1
        overs_left = balls_left // 6
        balls_remaining = balls_left % 6
        if overs_left > 0 and balls_remaining > 0:
            return f"{team2_name} won by {wickets_left} wickets with {overs_left} overs and {balls_remaining} balls remaining"
        elif overs_left > 0:
            return f"{team2_name} won by {wickets_left} wickets with {overs_left} overs remaining"
        else:
            return f"{team2_name} won by {wickets_left} wickets with {balls_remaining} balls remaining"
    else:
        return "The match ended in a tie"

def start_match(bat_or_bowl, team1_name, team2_name, who_won_the_toss, file, overs, players):
    total_balls = overs * 6
    
    if who_won_the_toss == team1_name:
        if bat_or_bowl == "bat":
            team1_score, team1_wickets, _ = play_innings(team1_name, file, overs, players)
            print("\033[1mInnings 1 finished\033[0m")
            team2_score, team2_wickets, balls_played = play_innings(team2_name, file, overs, players, target=team1_score+1)
        else:
            team2_score, team2_wickets, _ = play_innings(team2_name, file, overs, players)
            print("\033[1mInnings 1 finished\033[0m")
            team1_score, team1_wickets, balls_played = play_innings(team1_name, file, overs, players, target=team2_score+1)
    else:
        if bat_or_bowl == "bat":
            team2_score, team2_wickets, _ = play_innings(team2_name, file, overs, players)
            print("\033[1mInnings 1 finished\033[0m")
            team1_score, team1_wickets, balls_played = play_innings(team1_name, file, overs, players, target=team2_score+1)
        else:
            team1_score, team1_wickets, _ = play_innings(team1_name, file, overs, players)
            print("\033[1mInnings 1 finished\033[0m")
            team2_score, team2_wickets, balls_played = play_innings(team2_name, file, overs, players, target=team1_score+1)

    balls_left = total_balls - balls_played
    result = determine_winner(team1_name, team1_score, team2_name, team2_score, team2_wickets, balls_left)
    print(f"\n\033[1m{result}\033[0m")
    file.write(f"\n{result}\n")

def read_previous_score():
    try:
        with open('cricket.txt', 'r') as file:
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
            if 1 <= choice <= 4:
                break
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print(ENTER_NUMBER_ONLY_MSG)

    if choice == 1:
        read_previous_score()

    elif choice == 2:
        team1_name = input("Enter team 1 name: ")
        team2_name = input("Enter team 2 name: ")

        toss_teams = [team1_name, team2_name]

        print()

        while True:
            try:
                how_many_players = int(input("How many players are playing (from one team) in the match? "))
                if how_many_players > 0:
                    break
                else:
                    print("Please enter a positive number of players.")
            except ValueError:
                print(ENTER_NUMBER_ONLY_MSG)

        team1_players = add_player_names_in_team(team1_name, how_many_players)
        team2_players = add_player_names_in_team(team2_name, how_many_players)

        with open("cricket.txt", "w") as file:
            add_player_names_in_file(team1_name, team1_players, file)
            add_player_names_in_file(team2_name, team2_players, file)

            print("__________________________________\n")
            while True:
                try:
                    overs = int(input("Enter how many overs this match is: "))
                    if overs > 0:
                        break
                    else:
                        print("Please enter a positive number of overs.")
                except ValueError:
                    print(ENTER_NUMBER_ONLY_MSG)

            file.write(f"\nMatch overs: {overs}\n")

            print("\nNow do the toss")
            time.sleep(2)
            for i, team in enumerate(toss_teams, 1):
                print(f"{i}: {team}")

            while True:
                try:
                    toss_winner = int(input("Who won the toss (Enter number)? "))
                    if toss_winner in [1, 2]:
                        who_won_the_toss = toss_teams[toss_winner - 1]
                        break
                    else:
                        print("Enter a valid number (1 or 2)")
                except ValueError:
                    print(ENTER_NUMBER_ONLY_MSG)

            while True:
                bat_or_bowl = input(f"\nEnter what {who_won_the_toss} want to do (bat/bowl): ").lower()
                if bat_or_bowl in ["bat", "bowl"]:
                    break
                else:
                    print("Enter a valid choice (bat or bowl)")

            file.write(f"{who_won_the_toss} won the toss and chose to {bat_or_bowl}\n")
            print("\033[1mToss finished\033[0m\n")

            start_match(bat_or_bowl, team1_name, team2_name, who_won_the_toss, file, overs, how_many_players)

    elif choice == 3:
        remove_previous_score()

    elif choice == 4:
        print("Thank you for using the Cricket Scoreboard software. Goodbye!")
        break

    else:
        print("\nEnter a valid number")
