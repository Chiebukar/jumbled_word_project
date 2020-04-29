from random import *
import shelve
from func_timeout import *
import time
import copy
from pathlib import Path
from tabulate import tabulate

"""
@class User: Keeps the player's info.
@class Question: Gets word and hint from file and jumbles the word.
@class GameMode: Extends the behaviour of the Question class according to specific game mode.
@class Answer: Extends the GameMode class to check player's response and show the correct answer.
@class Scoreboard: Extends the User class to store score and high scores.
@class Game: Combines all objects to play game.
@class AboutGame: Shows the game guidelines.
@exception FunctionTimedOut: Exception raised when Question times out.
 """


# Store player's name and score
# Return object as string
class User:
    """
    A class that gets player's name and initializes score .

    :param name <str>: The player's name.
    """

    # Get the player's name from user and initialize score
    def __init__(self, name):
        """
        The constructor of the User class
        
        Initializes and keeps user info of name and score.
        
        :param name <str>: The player's name
        """""
        self.name = name
        self.score = 0

    # show object as a string of player's name and score
    def __str__(self):

        """ :returns rep <str>: Returns a string of player's name and score """

        rep = self.name + " : " + str(self.score)
        return rep


# Make jumbled word and hint from file
class Question:
    """
    A class that gets word and hint from the file and jumbles the the word.

    :param file <str>: The filename of the text file of words to be jumbled.
                      Words in the text file should be in the  format(word//hint).

    @staticmethod make_dict: Forms a dictionary of WORDS and hints.
    @method  get_question: Jumbles word gotten from make_dict.
    @method get_hint: Gets the hint for jumbled word.
    """

    def __init__(self, file):
        """ Constructor for Question class.

        Instantiates make_dict.

       :param file <str>: The filename of the text file of words to be jumbled.
                         Words in the text file should be in the  format(word//hint).
        """

        self.WORDS = self.make_dict(file)  # Instantiate  make_dict
        self.original_word = None
        self.response = None
        self.ques = None
        self.used_words_list = []
        self.hint = False

    # Make a dictionary of words as keys and hints as values
    @staticmethod
    def make_dict(file):
        """
         Forms a dictionary of words and hints and shuffles the contents of file.

        :param file: <str>: The filename of the text file of words to be jumbled.
                         Words in the text file should be in the  format(word//hint).

        :return WORDS: <dict> A dictionary containing word and hint pairs.
        """
        words = {}
        text_file = open(file, "r")
        for line in text_file:
            key, value = line.split("//")
            words[key] = value
        sample(list(words), len(words))
        text_file.close()
        return words

    # Jumble the word
    def get_question(self):
        """
        Gets word from WORDS<dict> and jumbles word.

        Gets answer to jumbled word as original_word.

        :return sel_question:<str>: Returns the jumbled word.
        """
        keys = [key for key in self.WORDS]
        self.original_word = choice(keys)
        jumble_word = sample(self.original_word, len(self.original_word))
        sel_question = "".join(jumble_word)
        return sel_question

    # Get the hint for word
    def get_hint(self):
        """
        # Gets the hint of the word from WORDS<dict>

        :return hint<str>: Returns the hint to answer each word
        """
        hint = self.WORDS[self.original_word]
        hint = hint.replace("\n", ".")
        return hint


# Change the behaviour of Question class
class GameMode(Question):
    """
     Extends the behaviour of Question for game modes.

    @method arcade_mode: Extends get_question  for the arcade game modes.
    @method arcade_quest: Asks questions and gets response as input.
    @method retry_arcade_quest: Asks the player same question again after  wrong response.
    @method arcade_mode_1: Method for Arcade 1 GameMode.
    @method arcade_mode_2: Method for Arcade 2 GameMode.
    @method arcade_mode_3: Method for Arcade 3 GameMode.
    @method classic: Method for classic GameMode.
    @method survival: Method for survival GameMode.

    """
    # Make question for Arcade Modes
    def arcade_mode(self, quest_len):
        """
        Extends get_question  for the arcade game modes according to required question length.

        :param quest_len:<str>: The desired  length for Arcade mode questions.
        :return quest<str> :  Returns question for Arcade modes.
        """
        quest = ""
        while len(quest) != quest_len or self.original_word in self.used_words_list:
            quest = self.get_question()
        return quest

    # Ask question for Arcade GameModes
    def arcade_quest(self, quest_len):
        """
        Asks question and gets response as input.

        :param quest_len:<str>: The desired  length for Arcade mode questions.
        :return ask<str>: Returns questions and gets response as input.
        """

        quest = self.arcade_mode(quest_len)
        self.ques = copy.deepcopy(quest)
        if self.response == "None" or self.response == "1":
            ask = input("""Your jumbled word is: {}
                        Press the enter key to  enter your response below: """.format(quest))
        else:
            ask = input("""Your jumbled word is: {}
               Press 1 for hint
                  Enter your response here: """.format(quest))
        return ask

    # Ask question again
    def retry_arcade_quest(self):
        """
        Asks the player same question again after  wrong response.

        provides hint if  requested by the player.

        :return: ask<str>: Asks question and takes response as input
        """
        quest = self.ques
        if self.response == "1":
            hint = self.get_hint()
            self.hint = True
            ask = input("""Your jumbled word is: {}
          Hint: {}
                      Enter your response here: """.format(quest, hint))
            return ask

        elif self.response is None:
            ask = input("""Your jumbled word is: {}
             Press the enter key to  enter your response below: """.format(quest))

        elif self.response != self.original_word:
            ask = input("""Your jumbled word is: {}
               Enter your response here: """.format(quest))
        else:
            ask = None
        return ask

    # Display question and take response for Arcade 1 GameMode
    def arcade_mode_1(self, quest_len, quest_time):

        """
        Method to display questions for Arcade 1 GameMode

        Asks player question and gives the player time-limit within a time length to answer the question.
        Retries the question with hint if requested by player with the remaining time as the new time limit.
        Raises the FunctionTimedOut exception if time length elapses and stops asking for player's response.
        Adds the already asked words to used words<list>.
        returns the player's response or None if the question is unanswered.


        :param quest_len:<int>: The length of the jumbled word
        :param quest_time:<int/float> The time limit to answer question
        :raise FunctionTimedOut: Raised when time limit elapses
        :return:response<str>: Returns the player's response
        """
        try:
            start_time = time.time()
            self.response = func_timeout(quest_time, self.arcade_quest, args=[quest_len]).lower()
            end_time = time.time()
            if self.response == "1":
                try:
                    used_time = end_time - start_time
                    rem_time = int(quest_time - used_time)
                    print(" \n\n remaining time: {} secs".format(rem_time))
                    self.response = func_timeout(rem_time, self.retry_arcade_quest).lower()
                except FunctionTimedOut:
                    raise FunctionTimedOut
        except FunctionTimedOut:
            print("Your time has elapsed")
            self.response = "None"
        self.used_words_list.append(self.original_word)
        return self.response

    # Display question and take response for Arcade 2 GameMode
    def arcade_mode_2(self, quest_len, quest_time, tries):
        """
        Method to display questions for Arcade 2 GameMode

        Asks player question and gives the player  a number of  tries with the same
         time-limit for  each try.
        Another attempt  is given within the tries limit if the previous answer is wrong or the time elapses.
        The question is asked again with hint if requested by the player with the remaining time as the new time limit.
        Raises the FunctionTimedOut exception if time length elapses for each try.
        Adds the already asked word to used words<list>.
        returns the player's response and None if the question is unanswered.


        :param quest_len:<int>: The length of the jumbled word
        :param quest_time:<int/float>: The time limit to answer question
        :param tries:<int>: The number of tries given  to give correct response
        :raise FunctionTimedOut: Raised when time limit elapses
        :return:response:<str>: Returns the player's response
        """
        try:
            print("\n\n  remaining tries: {}".format(tries))
            tries -= 1
            start_time = time.time()
            self.response = func_timeout(quest_time, self.arcade_quest, args=[quest_len]).lower()
            end_time = time.time()
            if self.response == "1":
                try:
                    used_time = end_time - start_time
                    rem_time = int(quest_time - used_time)
                    self.response = func_timeout(rem_time, self.retry_arcade_quest).lower()
                except FunctionTimedOut:
                    raise FunctionTimedOut
            if self.response != self.original_word:
                raise FunctionTimedOut
        except FunctionTimedOut:
            while tries:
                try:
                    print(" \n\n remaining tries: {}".format(tries))
                    tries -= 1
                    start_time = time.time()
                    self.response = func_timeout(quest_time, self.retry_arcade_quest).lower()
                    end_time = time.time()
                    if self.response == "1":
                        try:
                            used_time = end_time - start_time
                            rem_time = int(quest_time - used_time)
                            self.response = func_timeout(rem_time, self.retry_arcade_quest).lower()
                        except FunctionTimedOut:
                            raise FunctionTimedOut
                    if self.response != self.original_word:
                        raise FunctionTimedOut
                    else:
                        break
                except FunctionTimedOut:
                    if self.response is None:
                        self.response = "None"
        self.used_words_list.append(self.original_word)
        return self.response

    # Display question and take response for Arcade 3 GameMode
    def arcade_mode_3(self, quest_len, quest_time, tries):
        """
                Method to display question for Arcade 3 GameMode

                Gives the player 3 attempts within the same time limit to give correct response.
                Another attempt is given if the player's previous answer is wrong  and time has not elapsed.
                The question is asked again with hint if requested by the player with
                the remaining time as the new time limit.
                Raises the FunctionTimedOut exception if time length elapses for each try.
                Adds the already asked word to used words<list>.
                returns the player's response and None if the question is unanswered.


                :param quest_len:<int>: The length of the jumbled word.
                :param quest_time:<int>: The time limit to answer question.
                :param tries:<int>: The number of tries given to give correct response.
                :raise FunctionTimedOut: Raised when time limit elapses.
                :return:response:<str>: Returns the player's response.
                """

        try:
            tries -= 1
            start_time = time.time()
            self.response = func_timeout(quest_time, self.arcade_quest, args=[quest_len]).lower()
            end_time = time.time()
            if self.response != self.original_word:
                used_time = int(end_time - start_time)
                rem_time = quest_time - used_time
                quest_time = rem_time
                while tries and self.response != self.original_word and rem_time > 0:
                    try:
                        print(" \n\n remaining time: {} secs".format(rem_time))
                        tries -= 1
                        start_time = time.time()
                        self.response = func_timeout(rem_time, self.retry_arcade_quest).lower()
                        end_time = time.time()
                        used_time = int(end_time - start_time)
                        rem_time = quest_time - used_time
                        quest_time = rem_time
                    except FunctionTimedOut:
                        print("\n\nYour time has elapsed")
                        self.response = "None"
                        break
        except FunctionTimedOut:
            print("\n Your time has elapsed")
            self.response = "None"
        self.used_words_list.append(self.original_word)
        return self.response

    # Display question and take response for classic GameMode
    def classic(self):
        """
        Method to display questions for classic GameMode

        Asks player question and with no time-limit to  respond.
        Retries the question with hint if requested by player with.
        Adds the already asked words to used words<list>.
        returns the player's response or None if the question is unanswered.

        :raise FunctionTimedOut: Raised when time limit elapses
        :return:response<str>: Returns the player's response
        """

        quest = self.get_question()
        while self.original_word in self.used_words_list:
            quest = self.get_question()
        self.ques = copy.deepcopy(quest)
        self.response = input("""Your jumbled word is: {}
           Press 1 for Hint
                      Enter your response here: """.format(quest))
        print()
        while self.response == "1":
            self.response = self.retry_arcade_quest()
        self.used_words_list.append(self.original_word)
        return self.response

    # Display question and take response for survival GameMode
    def survival(self, quest_len):
        """
                Method to display questions for survival GameMode

                Asks player question and with no time-limit to respond.
                Retries the question with hint if requested by player.
                Adds the already asked words to used words<list>.
                returns the player's response.

                :raise FunctionTimedOut: Raised when time limit elapses
                :return:response<str>: Returns the player's response
                """
        self.response = self.arcade_quest(quest_len)
        print()
        if self.response == "1":
            self.response = self.retry_arcade_quest()
        self.used_words_list.append(self.original_word)
        return self.response


# Check player response
class Answer(GameMode):
    """
    Extends GameMode to check player's response and show the correct answers.

    @method check_answer: Checks if player's response is correct
    @method show_answer: Shows the correct answer.
    """

    # Check if player's response is correct
    def check_answer(self):
        """ Checks if the player's response is right or wrong.

        :returns:<boolean> Returns True if player is right or False if player is wrong"""
        if self.response == self.original_word:
            return True
        return False

    # Print the correct answer
    def show_answer(self):
        """Shows the correct answer if the player's response is wrong."""

        if not self.check_answer():
            print("The right answer is: {}".format(self.original_word))


# Manage player's score
class ScoreBoard(User):
    """
    Extends the User class to save scores and high scores.

    @method update_score: Increases player's score.
    @staticmethod  file_path: Generates path to the file that stores the high score of GameMode.
    @method upload_score: Uploads score to GameMode's file.
    @staticmethod high_scores: Prints the top 5 high score values in the GameMode's file.
    @method show_score: Shows the player's current score.
    @method final_high_score: Extends high_score to Show the player's final score and high score.
    """

    # Increase player's score for correct response
    def update_score(self, hint):
        """
        Increases player's score

        Increases the player's score by 3 points if they answer the question correctly without hint.
        Increases the player's score by 1 point if they answer the question correctly with hint.

        :param hint:<boolean>: Results to True if player uses hint to answer questions and False if not.
        """
        if hint:
            self.score += 1
        else:
            self.score += 3

    # Generate GameMode score file path
    @staticmethod
    def file_path(game_mode):
        """
        Generates path to the file that stores the high score of GameMode.

        creates new GameMode folder and file for scores if non exists.

        :param game_mode:<str>: File name for GameMode
        :return: file<str>: Returns the file path as file in str format
        """
        data_folder = Path("high_score_DB")
        data_folder.mkdir(parents=True, exist_ok=True)
        file = str(data_folder) + "/" + game_mode
        return file

    # Add player's score to GameMode file
    def upload_score(self, game_mode):
        """
         Uploads player's score to GameMode scoreboard.

        :param game_mode:<str>: file name for GameMode
        """

        file = ScoreBoard.file_path(game_mode)
        scoreboard = shelve.open(file)
        scoreboard[self.name] = self.score
        print("Score uploaded!")

    # Print the top 5 high scores
    @staticmethod
    def high_scores(game_mode):
        """
        Prints the top 5 high score values in GameMode file.

        prints the high scores in tabular form
        :param game_mode:<str>: file name for GameMode.
        :return: high_score_values<list> : Returns a list of the 5 highest score values.
        """
        file = ScoreBoard.file_path(game_mode)
        scoreboard = shelve.open(file)
        high_scores = sorted(scoreboard.items(), reverse=True, key=lambda x: x[1])[:5]
        high_score_values = []
        print(tabulate(high_scores, headers=['Name', 'Score'], tablefmt='orgtbl'))
        for e_score in high_scores:
            high_score_values.append(e_score[1])
        scoreboard.close()
        return high_score_values

    # Show the player's score
    def show_score(self):
        """
        Shows the player's current score.

        :return score:<int>: Returns player's scores
        """
        print("{}: current score:{}".format(self.name, self.score))
        return self.score

    # Print the high score
    # Print the player's high score position if score is in high score
    def final_high_score(self, game_mode):
        """"
         Prints the top 5 high score of the GameMode's file.

         Prints the player's high score position if score is in top 5 scores.
         Congratulates the player if they make the high score.
         Shows the player how many points they were off an high score position if they don't make high score.

         :param game_mode:<str>: file name for GameMode.
        """

        print("\n Game Completed \n Your Final Score is: {}".format(self.score))
        high_scores_values = ScoreBoard.high_scores(game_mode)
        high_score_position = ["1st", "2nd", "3rd", "4th", "5th"]
        if self.score in high_scores_values:
            high_score_index = high_scores_values.index(self.score)
            print("""Congratulations! {}  
You are {} in High scores""".format(self.name, high_score_position[high_score_index]))

        else:
            difference = high_scores_values[-1] - self.score
            print("Jumble Completed \n Your Final Score is: {}".format(self.score))
            print("You are {} points short of an High score position".format(difference))


# Play game
class Game(object):
    """
    Combines all objects to play game.

    :param: name<str>: Player's name.
    :param game_mode:<str>: file name of GameMode.

    @method - Method to play Game.
    """

    # Instantiate classes to play game
    def __init__(self, name, game_mode):
        """
        Constructor for Game class.

        Instantiates Answer(GameMode) and ScoreBoard(User) classes

        :param name<str>: Player's name
        :param game_mode:<str>: file name for GameMode
        """

        self.game_mode = game_mode
        self.answer = Answer("word")
        self.scoreboard = ScoreBoard(name)

    # Play game
    def play(self):

        """Method that combines objects to play game.

           Extends the objects to play jumble word game.
        """
        game_mode = self.game_mode

        # Play game for classic GameMode
        if game_mode == "classic":
            counter = 0
            while counter < 5:
                self.scoreboard.show_score()
                response = self.answer.classic()
                if self.answer.check_answer():
                    print("correct")
                    hint = self.answer.hint
                    self.scoreboard.update_score(hint)
                else:
                    print("\n your response is: ", response)
                    self.answer.show_answer()
                self.answer.hint = False
                counter += 1

        # Play game for survival GameMode
        elif game_mode == "survival":
            quest_len = 5
            cut_off_mark = 10
            stage = 1
            while quest_len < 10:
                print("Welcome to stage: ", stage)
                print("cut off mark for next stage is: {} points".format(cut_off_mark))
                time.sleep(2)
                counter = 0
                while counter < 5:
                    self.scoreboard.show_score()
                    response = self.answer.survival(quest_len)
                    if self.answer.check_answer():
                        print("correct")
                        hint = self.answer.hint
                        self.scoreboard.update_score(hint)
                    else:
                        print("\n your response is: ", response)
                        self.answer.show_answer()
                    self.answer.hint = False
                    counter += 1
                score = self.scoreboard.show_score()
                if score < cut_off_mark:
                    rem = cut_off_mark - score
                    print("Your score is {} points below the cut off mark for the next stage".format(rem))
                    break
                input("\n\n Press the enter key to move to the next stage")
                stage += 1
                cut_off_mark += 10
                quest_len += 1
        # Play game for Arcade GameMode
        else:
            quest_len = 5
            quest_time = 60
            stage = 1
            while quest_len < 10:
                print("Welcome to stage: ", stage)
                print("Your have {} secs to answer each question".format(quest_time))
                time.sleep(3)
                counter = 0
                while counter < 5:
                    self.scoreboard.show_score()
                    if game_mode == "arcade_1":  # Arcade 1 GameMode
                        response = self.answer.arcade_mode_1(quest_len, quest_time)
                    elif game_mode == "arcade_2":  # Arcade 2 GameMode
                        response = self.answer.arcade_mode_2(quest_len, quest_time, 2)

                    else:   # Arcade 3 GameMode
                        response = self.answer.arcade_mode_3(quest_len, quest_time, 3)
                    if self.answer.check_answer():
                        print("correct")
                        hint = self.answer.hint
                        self.scoreboard.update_score(hint)
                    else:
                        print("\n your response is: ", response)
                        self.answer.show_answer()
                    self.answer.hint = False
                    counter += 1
                stage += 1
                quest_time += 30
                quest_len += 1
        time.sleep(2)
        self.scoreboard.upload_score(game_mode)
        self.scoreboard.final_high_score(game_mode)


# Print game guidelines
class AboutGame:
    def __str__(self):
        """
        A class that shows the player  the game guidelines.

        :return about<str>:  Returns a string of the game guidelines
        """

        about = ("""        This is a Jumble word game,it displays word in jumbled form and allows 
        the user to enter the word in correct form.
        The game has 2 main game modes, the classic and arcade modes.

        In the classic mode the player is allowed a chance to correctly answer questions with no time limit.
        10 questions  are chosen at random from 5 to 9 lettered words.
        Players scores 3 points for  correct answer and no points for wrong answer.
        The player is allowed to request for meaning of WORDS as hints and gets 1 point when a question
        is answered correctly using hint.
        
        In the survival mode the  player is allowed a chance to answer 5 questions each from 
        5 to 9 lettered words with no time limit, where each lettered word is a stage leading up 5 stages.
        Player is to reach a specified cut off mark to qualify for the next stage.
        Player scores 3 points for correct answer and no points for wrong answer.
        The player is allowed to request for the meaning of words as hints and gets 1 point when a question
        is answered correctly using hint.

        In the Arcade mode the player is given a certain time limit to answer 5 questions each from 
        5 to 9 lettered words with each lettered word a stage leading up 5 stages 
        (with 5,6,7,8 and 9 words respectively).
        The player gets 3 points for question answered correctly and 1 point for
        correct answers using hint. No points are awarded for a final wrong answer. 
        The arcade mode has 3 sub modes (arcade 1, 2 and 3) which uses the same stage levels 
        and scoring metrics.

        Arcade 1 sub mode gives the player a certain time limit per stage to enter answers, a question 
        is deemed to be answered wrongly if the answer is incorrect or the given time elapses.

        Arcade 2  sub mode gives the player 2 attempts to correctly answer a question, a second attempt is given 
        if the first attempt is wrong or the given time elapses.
        The player is given the same time for both attempts.

        Arcade 3 sub mode gives the player 3 attempts within a certain time limit to enter correct answers.
        Attempts are only given if the previous attempt is wrong, there are no renewed time with only 3 attempts
        allowed within a given time frame.The player is shown the amount of time left after each attempt.

       After the each completed game mode, the player is shown the final score and congratulated if they make 
       the high score or shown how far off they were if they don't.
    """)
        return about


