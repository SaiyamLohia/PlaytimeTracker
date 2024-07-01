import csv
import psutil
import threading
import time


games = []
running_game = None
game_path = None

start_time = None


def update_games():
    global games
    with open('data.csv', mode='r') as file:
        reader = csv.reader(file)
        csv_data = list(reader)

    for game in csv_data:
        games.append(game[0])


def update_runtime_csv():
    with open('data.csv', mode='r') as file:
        reader = csv.reader(file)
        csv_data = list(reader)

    for r in range(len(csv_data)):
        if csv_data[r-1][0] == game_path:
            csv_data[r-1][2] = str(round(float(csv_data[r-1][2]) + ((time.time() - start_time) / 60), 2))

    with open('data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)


def look_for_game():
    processes = psutil.process_iter()
    for process in processes:
        try:
            if process.is_running():
                if process.cmdline()[0] in games:
                    global running_game
                    global game_path
                    running_game = process
                    game_path = process.cmdline()[0]
        except (IndexError, psutil.AccessDenied):
            pass


def main_loop():

    global start_time, running_game, game_path

    while True:
        if running_game:
            if running_game.is_running():
                if start_time is None:
                    start_time = running_game.create_time()
            else:
                update_runtime_csv()
                running_game = None
                game_path = None

        else:
            start_time = None
            look_for_game()
        time.sleep(10)


def commands(user_input):
    with open('data.csv', mode='r') as file:
        reader = csv.reader(file)
        csv_data = list(reader)

    if user_input.lower() == '/add':
        path = input('Enter the path for the executable file of the application: ')
        name = input('Enter the name of the application: ')

        csv_data.append([path, name, "0"])

        print("New Application Added!")

    elif user_input.lower() == '/view':
        for game in csv_data:
            hours_played = round(float(game[2]) / 60, 2)
            print(game[1] + ': ' + str(hours_played) + ' hours')

    elif user_input.lower() == '/rem':
        i = 1
        for game in csv_data:
            print(str(i) + '. ' + game[1])
            i += 1
        remove_index = int(input("Index of App to be removed: "))
        csv_data.pop(remove_index-1)
        print("Application removed!")

    with open('data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    update_games()


update_games()
threading.Thread(target=main_loop, daemon='True').start()
while True:
    commands(input(''))
