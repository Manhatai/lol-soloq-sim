import tkinter # For some commands not available in customtkinter
import customtkinter # Main app frame
import random as rd # Lp calculations
from pyprobs import Probability as pr # Lp calculations
from PIL import Image # For rank image
import requests # For getting summoners info from riots api
from dotenv import load_dotenv # For env file usage
import os # Same as above
import urllib.parse # For encoding summoner name into the URL

# App frame
root = customtkinter.CTk()
root.geometry("720x780")
root.title("SoloQ Simulator")
root.after(201, lambda :root.iconbitmap('images\\favicon.ico'))

# System settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Lists used in the program
rank_types = {"iron iv": 0, "iron iii": 100, "iron ii": 200, "iron i": 300, "bronze iv": 400, "bronze iii": 500,
              "bronze ii": 600, "bronze i": 700, "silver iv": 800, "silver iii": 900, "silver ii": 1000,
              "silver i": 1100, "gold iv": 1200, "gold iii": 1300, "gold ii": 1400, "gold i": 1500,
              "platinum iv": 1600, "platinum iii": 1700, "platinum ii": 1800, "platinum i": 1900,
              "emerald iv": 2000, "emerald iii": 2100, "emerald ii": 2200, "emerald i": 2300, "diamond iv": 2400,
              "diamond iii": 2500, "diamond ii": 2600, "diamond i": 2700}
game_count_prob = []
lp_total = []


# Class doing all the work
class Calculations():
    def __init__(self):
        self.user_rank = None
        self.user_lp = None
        self.wr = None
        self.games_expected = None
        self.lp = None
        self.result_whole = None
        self.result_final = None

    # Rank input (class)
    def rank_current(self):
        user_rank = rankInput.get().lower()
        if (user_rank not in rank_types) or (isinstance(user_rank, str) == False):
            print("Rank not found")
            foundLabel.configure(text="Rank/Username not found (example: gold IV)", text_color="red")
            rankInput.configure(border_width=2, border_color="red")
        else:
            print("Rank found!!!")
            rankInput.configure(border_width=1, border_color="white")
            foundLabel.configure(text="Rank found!", text_color="green")
            print(f"Users rank: {user_rank}")
            self.user_rank = user_rank

    # Lp count input (class)
    def lp_count(self):
        try:
            user_lp = leaguePoints.get()
            user_lp = int(user_lp)
            if (user_lp > 99) or (user_lp < 0):
                print("Lp count invalid")
                foundLabel2.configure(text="Lp count invalid (should be 0 - 99)", text_color="red")
                leaguePoints.configure(border_width=2, border_color="red")
            else:
                print("Lp count is valid!")
                leaguePoints.configure(border_width=1, border_color="white")
                foundLabel2.configure(text="Lp count is valid!", text_color="green")
                print(f"Users lp count: {user_lp}")
                self.user_lp = user_lp
        except (ValueError, KeyError):
            print("Lp count invalid")
            foundLabel2.configure(text="Lp count invalid (should be 0 - 99)", text_color="red")
            leaguePoints.configure(border_width=2, border_color="red")

    # Winrate input (class)
    def winrate(self):
        try:
            wr = winrateInput.get()
            wr = int(wr)
            wr = (wr / 100)
            if (wr > 1) or (wr < 0):
                print("Invalid winrate value (should be 1 - 100)")
                foundLabel3.configure(text="Invalid winrate value (should be 1 - 100)", text_color="red")
                winrateInput.configure(border_width=2, border_color="red")
            else:
                print("Winrate value is valid!")
                winrateInput.configure(border_width=1, border_color="white")
                foundLabel3.configure(text="Winrate value is valid!", text_color="green")
                print(f"Users winrate: {wr}")
                self.wr = wr
        except (ValueError, KeyError):
            print("Invalid winrate value (should be 1 - 100)")
            foundLabel3.configure(text="Invalid winrate value (should be 1 - 100)", text_color="red")
            winrateInput.configure(border_width=2, border_color="red")

    # Input games expected (class)
    def set_games_expected(self):
        try:
            games_expected = gamesExpected.get()
            games_expected = int(games_expected)
            foundLabel4.configure(root, text="Games expected value is valid!", text_color="green")
            gamesExpected.configure(border_width=1, border_color="white")
            print(f"Number of games user expects to play: {games_expected}")
            self.games_expected = games_expected
            if check_var.get() == "on":
                gamesExpected.configure(border_width=1, border_color="white")
        except (ValueError, KeyError):
            foundLabel4.configure(root, text="Games expected value is invalid", text_color="red")
            gamesExpected.configure(border_width=2, border_color="red")

    # Loop calculating the lp value (class)
    def ranked_games(self):
        games = []
        lp = 0
        game_count = 0
        while True:
            result = pr.prob(self.wr)  # returns True or False based on "wr" value
            if result:
                lp += rd.randint(20, 25)  # +20lp / +25lp
            else:
                lp += rd.randint(-22, -18)  # -18lp / -22lp

            if check_var.get() == "on":
                self.games_expected = 10000
                if lp + rank_types[self.user_rank] >= rank_types[rankNewInput.get().lower()]:
                    game_count_prob.append(game_count)
                    break

            if game_count == self.games_expected:
                break

            games.append(lp)
            game_count += 1
        self.lp = lp

    # Function calculating your final rank, passing it to rank_gained (class)
    def ranked_calculations(self):
        for i in range(1000):  # 1000 * "games_expected" samples
            self.ranked_games()
            lp_total.append(self.lp)

        result = sum(lp_total) / 1000
        result_whole = round(result)
        result_whole += self.user_lp + rank_types.get(self.user_rank)
        self.result_whole = result_whole

    # Function outputting your rank and rank image on the screen (class)
    def rank_gained(self):
        rank_ranges = {(0, 99): "iron IV", (100, 199): "iron III", (200, 299): "iron II", (300, 399): "iron I",
                       (400, 499): "bronze IV", (500, 599): "bronze III", (600, 699): "bronze II",
                       (700, 799): "bronze I", (800, 899): "silver IV", (900, 999): "silver III",
                       (1000, 1099): "silver II", (1100, 1199): "silver I", (1200, 1299): "gold IV",
                       (1300, 1399): "gold III", (1400, 1499): "gold II", (1500, 1599): "gold I",
                       (1600, 1699): "platinum IV", (1700, 1799): "platinum III",
                       (1800, 1899): "platinum II", (1900, 1999): "platinum I", (2000, 2099): "emerald IV",
                       (2100, 2199): "emerald III", (2200, 2299): "emerald II", (2300, 2399): "emerald I",
                       (2400, 2499): "diamond IV", (2500, 2599): "diamond III",
                       (2600, 2699): "diamond II", (2700, 2799): "diamond I"}

        for (start, end), rank in rank_ranges.items():
            proper_lp_count = round(self.result_whole / 100)
            if start <= self.result_whole <= end:
                result_final = f"Your rank should be: {rank} {proper_lp_count}LP"
                print(result_final)
                self.result_final = result_final
                print(proper_lp_count)
                if self.result_whole in range(0, 399):
                    image_path.configure(dark_image=iron, size=(200, 200))
                    image_label.pack()

                if self.result_whole in range(400, 799):
                    image_path.configure(dark_image=bronze, size=(200, 200))
                    image_label.pack()

                if self.result_whole in range(800, 1199):
                    image_path.configure(dark_image=silver, size=(200, 200))
                    image_label.pack()

                if self.result_whole in range(1200, 1599):
                    image_path.configure(dark_image=gold, size=(200, 200))
                    image_label.pack()

                if self.result_whole in range(1600, 1999):
                    image_path.configure(dark_image=platinum, size=(200, 200))
                    image_label.pack()

                if self.result_whole in range(2000, 2399):
                    image_path.configure(dark_image=emerald, size=(200, 200))
                    image_label.pack()

                if self.result_whole in range(2400, 2799):
                    image_path.configure(dark_image=diamond, size=(200, 200))
                    image_label.pack()

            if self.result_whole >= 2800:
                result_final = f"Your rank should be: master+"
                print(result_final)
                self.result_final = result_final
                image_path.configure(dark_image=master, size=(200, 200))
                image_label.pack()

    # Clears all lists everytime the class instance is called (class)
    def clear(self):
        game_count_prob.clear()
        lp_total.clear()


calculations = Calculations()


# "Enter desired rank" checkbox
def checkbox():
    if check_var.get() == "on":
        image_label.forget()
        gamesExpected.configure(border_width=0)
        gamesExpected.delete(0, tkinter.END)
        gamesExpected.configure(state="disabled")
        foundLabel4.configure(text="")
        title5.forget()
        title6.pack()
        checkboxLabel.configure(
            text="Calculations lesser than one rank up from your current rank might not be as accurate.",
            text_color="white", font=("Roboto", 14))
        rankNewInput.pack()
        image_path.configure(dark_image=default_image, size=(200, 200))
    else:
        gamesExpected.configure(border_color="white")
        gamesExpected.configure(border_width=1)
        gamesExpected.configure(state="normal")
        foundLabel4.configure(text="")
        title5.pack()
        image_label.pack()
        title6.forget()
        checkboxLabel.configure(text="")
        rankNewInput.delete(0, 'end')
        rankNewInput.pack_forget()


# Calculations in "Enter desired rank" textbox
def rankProb():
    if check_var.get() == "on":
        rank1 = rankInput.get().lower()
        rank2 = rankNewInput.get().lower()
        diff1 = rank_types.get(rank1)
        diff2 = rank_types.get(rank2)
        if diff2 < (diff1 + 399):
            checkboxLabel.configure(
                text="Calculations less than one rank up from your current rank might not be as accurate!",
                text_color="red")
        else:
            checkboxLabel.configure(text="Able to calculate!", text_color="green")


# Getting Users account info based off RiotID
def username_check():
    # Getting users RiotID
    load_dotenv()

    api_key = os.getenv("API_KEY")

    if not api_key:
        print("API key is missing. Make sure to set it in your environment variables.")
        pass

    # Summoners username and the region they play in
    summoner_name = f"{rankInput.get()}"  # rankInput.get()
    region = "eun1"  # Replace with the appropriate region for your username

    print(f"Summoners name: {summoner_name}")

    # Encode summoner name into the URL
    encoded_summoner_name = urllib.parse.quote_plus(summoner_name.replace("#", "%23"))

    # Getting Users rank and lp
    base_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{encoded_summoner_name}"
    headers = {"X-Riot-Token": api_key}

    # Fetch summoners data from URL
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        summoner_data = response.json()
        summoner_id = summoner_data['id']


        # Getting the summoners rank info
        rank_url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
        rank_response = requests.get(rank_url, headers=headers)
        if rank_response.status_code == 200:
            ranks = rank_response.json()

            # Extract rank info
            rank_data = [  # a list of dictionaries (!)
                {"Queue": rank["queueType"], "Rank": rank.get("tier", "Unranked"), "Division": rank.get("rank", ""), "LP": rank.get("leaguePoints", 0)}
                for rank in ranks
            ]

            print(rank_data)

            # If bool is true (list isn't empty) do this:
            if bool(rank_data):
                print("Username checks out!")
                users_soloq_rank = next(item for item in rank_data if item["Queue"] == "RANKED_SOLO_5x5") #
                users_rank = users_soloq_rank["Rank"]
                users_div = users_soloq_rank["Division"]
                users_lp = users_soloq_rank["LP"]
                rankInput.delete(0, tkinter.END)
                rankInput.insert(0, str(users_rank + ' ' + users_div))
                leaguePoints.delete(0, tkinter.END)
                leaguePoints.insert(0, str(users_lp))
                root.update()

            else:
                print("Invalid Username or User hasn't played any solo ranked games!")
                pass
        else:
            print(f"Error getting rank information: {rank_response.status_code}")
            pass
    else:
        print(f"Error getting summoner information: {response.status_code}")
        pass

# Gives "Calculate rank" button the data it needs
def calculate_and_update():
    checkbox()
    username_check()
    calculations.rank_current()
    calculations.lp_count()
    calculations.winrate()
    calculations.set_games_expected()
    calculations.ranked_games()
    calculations.ranked_calculations()
    calculations.rank_gained()
    rankProb()
    result_final = calculations.result_final
    title5.configure(text=f"{result_final}", font=("Roboto", 20), text_color="#0DFF00")
    if check_var.get() == "on":
        checkbox()
        foundLabel4.configure(root, text="")
        title5.configure(text="")
        title6.configure(
            text=f"Games needed to reach the desired rank (average): {round((sum(game_count_prob)) / len(game_count_prob))}",
            font=("Roboto", 20),
            text_color="#0DFF00",
            padx=10,
            pady=10,
        )
    else:
        title6.configure(text="")
    calculations.clear()

# Rank input (app)
title = customtkinter.CTkLabel(root, text="Enter your username or rank:", font=("Roboto", 16))
title.pack(pady=5)
rank_var = tkinter.StringVar()
rankInput = customtkinter.CTkEntry(root, width=150, height=25, textvariable=rank_var, border_width=1,
                                   border_color="white", )
rankInput.pack()
foundLabel = customtkinter.CTkLabel(root, text="")
foundLabel.pack()

# Lp count (app)
title2 = customtkinter.CTkLabel(root, text="Enter your lp count (0 - 99):", font=("Roboto", 16))
title2.pack(pady=5)
lp_var = tkinter.StringVar()
leaguePoints = customtkinter.CTkEntry(root, width=150, height=25, textvariable=lp_var, border_width=1,
                                      border_color="white", )
leaguePoints.pack()
foundLabel2 = customtkinter.CTkLabel(root, text="")
foundLabel2.pack()

# Winrate input (app)
title3 = customtkinter.CTkLabel(root, text="Enter your winrate (1 - 100):", font=("Roboto", 16))
title3.pack(pady=5)
wr_var = tkinter.StringVar()
winrateInput = customtkinter.CTkEntry(root, width=150, height=25, textvariable=wr_var, border_width=1,
                                      border_color="white", )
winrateInput.pack()
foundLabel3 = customtkinter.CTkLabel(root, text="")
foundLabel3.pack()

# Expected games input (app)

title4 = customtkinter.CTkLabel(root, text="Enter how many games you want to play:", font=("Roboto", 16))
title4.pack(pady=5)
games_var = tkinter.StringVar()
gamesExpected = customtkinter.CTkEntry(root, width=150, height=25, textvariable=games_var, border_width=1,
                                       border_color="white", )
gamesExpected.pack()
foundLabel4 = customtkinter.CTkLabel(root, text="")
foundLabel4.pack()

# Yes/No checkbox (app)
check_var = customtkinter.StringVar(value="off")
my_check = customtkinter.CTkCheckBox(
    root,
    text="Would you like to calculate how many games it would take to get to a certain rank?",
    variable=check_var,
    onvalue="on",
    offvalue="off",
    command=checkbox,
    font=("Roboto", 16),
    corner_radius=36,
    border_width=2,
    border_color="white",
)

my_check.pack()
checkboxLabel = customtkinter.CTkLabel(root, text="")
checkboxLabel.pack()
rankNew_var = tkinter.StringVar()
rankNewInput = customtkinter.CTkEntry(root, width=150, height=25, textvariable=rankNew_var, border_width=1,
                                      border_color="white", )

# Rank result output (app)
title5 = customtkinter.CTkLabel(root, text="")
title5.pack(padx=10, pady=10)

# Average games to achieve x rank output (app)
title6 = customtkinter.CTkLabel(root, text="")

# Adding image to users window (app)
default_image = Image.open('images/default.png')
iron = Image.open('images/iron.png')
bronze = Image.open('images/bronze.png')
silver = Image.open('images/silver.png')
gold = Image.open('images/gold.png')
platinum = Image.open('images/platinum.png')
emerald = Image.open('images/emerald.png')
diamond = Image.open('images/diamond.png')
master = Image.open('images/master.png')
image_path = customtkinter.CTkImage(dark_image=default_image, size=(200, 200))
image_label = customtkinter.CTkLabel(root, image=image_path, text="", width=150, height=150)

# Calculate button (app)
calculate = customtkinter.CTkButton(root, width=300, height=50, text="Calculate rank", font=("Roboto", 30),
                                    command=calculate_and_update, hover_color="green", border_width=2,
                                    border_color="white",
                                    )
calculate.pack(side="bottom", padx=100, pady=10)

# Run app
root.mainloop()
