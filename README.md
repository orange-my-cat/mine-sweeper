# CITS3403 Project Word Sweeper : A combination of minesweeper and wordle

#### This game is designed for each user to have one puzzle per day and the puzzle is updated daily at 12.00 am Perth Time.

# By Zong Ken Chai 22991721

# Wee Vern Peh 23241696

# Jonathan Hartono 22976067

# Chukwuebuka Anwasi 22990144

&nbsp;
&nbsp;

## Getting Started

1. Setting up virtual environment
   ```
   python -m pip install virtualenv
   virtualenv env
   source mypython/bin/activate
   python -m pip install -r requirements.txt
   ```
   ```
   # to exit virtual environment
   deactivate
   ```
2. Download [sqlite3](https://www.sqlitetutorial.net/download-install-sqlite/)
   &nbsp;
   &nbsp;

## Running the application

    ```
    # Updating the statistic table
    python add_statistics.py
    # Choosing the word and seed for the game
    python choose_word.py
    # Running the flask app
    flask run
    # ctrl+c to stop the flask application
    ```

&nbsp;
&nbsp;

## Admin Page

1. There is an admin page where admin can modify the tables in the database.
   Username : admin , Password: root1234
2. By logging in, you will have access to the admin page.
3. You can add new word and modify the word choosen for that day.

### All of these can be done using python script too.

&nbsp;
a) Choosing the word and seed randomly (Run this before running "flask run")

```
python choose_word.py
```

b) Delete the word for today

```
python delete_word.py
```

c) Add word into the word list table (You can add multiple word in one line but make sure every word has 5 letters)

```
python add_word.py [word] [word] [word]
```

d) Updating the score table (to visualise statistics given as there aren't any user playing the game)

```
python add_statistics.py
```

&nbsp;
&nbsp;

## Running Unit and System Test

1. System Test

```
flask run
#open another terminal
python ./Testing/system_test.py
```

2. Unit Test

```
python ./Testing/unit_test.py
```
