from jumbled_word_project.game import *  # import all game attributes

""""
@function main: Combines the  Menu  and Game classes  to play game.
@class Menu: Sets the menu for the game.
"""


# Create game navigation
class Menu(ScoreBoard):
    """"
    Sets the main menu for the game.

    :param name<str>: Player's name.

    @method main_menu: Displays the  Game's main menu.
    @method game_mode: Displays the GameMode menu.
    @method show_high_score: Displays high score menu.
    """

    # Instantiate player name and score
    def __init__(self, name):
        """"
        Constructor for Menu class.

        :param name<str>: Player's name.

        Instantiates player's name and score.
        Extends the Scoreboard class' constructor.
        """
        super().__init__(name)
        self.option = None

    # Display the Game's main menu
    def main_menu(self):
        """
        Displays the menu to play GameMode.

        Asks the user to enter a valid option if an invalid option is chosen.

        :return option<str>: Returns player's choice
        """
        options = ["1", "2", "3", "4"]
        while self.option not in options:
            print("""
             Game Options 
              Enter: 
              1  Play Game
              2  High Score
              3  About
              4  Exit Game  
                     """)

            self.option = (input("Enter an option here: "))
            if self.option not in options:
                print("Invalid choice, enter any of numbers 1, 2, 3 or 4")
        return self.option

    # Display GameMode's menu.
    def game_mode_menu(self):
        """
           Displays GameMode's menu .

           Asks the user to enter a valid option if an invalid option is chosen.

           :return game_mode<str>: Returns the chosen GameMode
           """
        self.option = None
        game_mode = None
        options = ["1", "2", "3"]
        while self.option not in options:
            print("""
                         Game Options 
                          Enter: 
                          1  Classic
                          2  Survival
                          3  Arcade
                                 """)

            self.option = (input("Enter Game option: "))
            if self.option not in options:
                print("Invalid choice, enter any of numbers 1, 2 or 3")

        if self.option in ["1", "2"]:
            game_modes = {"1": "classic", "2": "survival"}
            game_mode = game_modes[self.option]
        elif self.option == "3":
            self.option = ""
            while self.option not in options:
                game_modes = {"1": "arcade_1", "2": "arcade_2", "3": "arcade_3"}
                print("""
                                         Arcade Game Options 
                                          Enter: 
                                          1  Arcade Type 1
                                          2  Arcade Type 2
                                          3  Arcade Type 3

                                                 """)
                self.option = input("Enter Arcade Game option: ")
                if self.option in options:
                    game_mode = game_modes[self.option]
                else:
                    print("Incorrect choice, enter any of numbers 1, 2, or 3")
        print("You have chosen the {} Game mode".format(game_mode))
        return game_mode

    # Display HighScore's menu.
    def show_high_score(self):
        """
        Displays  HighScore's menu.

        Asks the user to enter a valid option if an invalid option is chosen.

        :return game_mode<str>: Returns the chosen GameMode
        """
        self.option = None
        while self.option not in ["1", "2", "3", "4", "5"]:
            print("""
             Game Options 
              Enter: 
              1  Classic  High score
              2  Survival High Score
              3  Arcade_1 High Score
              4  Arcade_2 High Score
              5  Arcade_3 High Score
                     """)
            self.option = (input("Enter an option  here: "))
            if self.option not in ["1", "2", "3", "4", "5"]:
                print("Invalid choice, enter any of numbers 1, 2, 3, 4 or 5")
        game_modes = {"1": "classic", "2": "survival", "3": "arcade_1", "4": "arcade_2", "5": "arcade_3"}
        game_mode = game_modes[self.option]
        return game_mode


# play game with menu
def main():

    """ Plays game with with navigation from Menu class"""
    play_again = None
    name = None
    while play_again != "n":
        if name:
            option = input("Do you want to change Player name? (y/n): ".lower())
            if option == "y":
                name = input("Enter Player's  name: ")
            else:
                pass
        else:
            name = input("Enter Player's  name: ")
        menu = Menu(name)
        option = menu.main_menu()
        if option == "1":
            game_mode = menu.game_mode_menu()
            user = Game(name, game_mode)
            user.play()
        elif option == "2":
            game_mode = menu.show_high_score()
            menu.high_scores(game_mode)
        elif option == "3":
            abt = AboutGame()
            print(abt)
        else:
            print("Exiting Game.....")
            time.sleep(1)
            break
        play_again = input("Do you want to play again? (y/n): ").lower()


main()
input("\n\n Press the enter key to exit")
