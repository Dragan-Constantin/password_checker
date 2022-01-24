import string, os, requests, platform
from os import getcwd


def clear():
    os.system(('cls' if platform.system()=='Windows' else 'clear'))

def score(pswd:str):
    length, score = len(pswd), 0

    # WE CHECK THE PASSWORD CHARACTER TYPES
    upper_case = any([1 if c in string.ascii_uppercase else 0 for c in pswd])
    lower_case = any([1 if c in string.ascii_lowercase else 0 for c in pswd])
    special = any([1 if c in string.punctuation else 0 for c in pswd])
    digits = any([1 if c in string.digits else 0 for c in pswd])

    characters = [upper_case, lower_case, special, digits]
    if sum(characters) == 1: score += 1
    elif sum(characters) == 2: score +=2
    elif sum(characters) == 3: score += 3
    elif sum(characters) <= 4: score += 4

    # WE CHECK THE PASSWORD LENGTH
    if length < 4: score+=0.25
    elif length > 4 and length < 8: score+=0.5
    elif length > 8: score += 1
    elif length > 12: score += 2
    elif length > 16: score += 3
    elif length > 20: score += 4
    
    return score


def get_db(url:str):
    r = requests.get(url)
    return r.text.splitlines()


def online_check(pswd):
    try:
        online_found = 0

        # WE CHECK IF THE PASSWORD IS IN ONE OF OUR PASSWORD DATABASES
        with open('BRUTEFORCE_URL.txt', 'r') as f: db_lists_url = f.read().splitlines()
        for url in db_lists_url:
            online_db = get_db(url)  # is my with open(online)
            if pswd in online_db: online_found+=1

        if online_found > 0:
            print(f"Password was found in {online_found}/15 of our common list. Score: 0/8")
            return True
        else:
            print("\nPassword was not found in our online database.")
            return False

    except Exception as e:
        # print(e)
        print("An error occured: coudn't check online database.")
        return None


def offline_check(pswd):
    try:
        offline_found, db_lists = 0, []

        # WE CHECK IF THE PASSWORD IS IN ONE OF OUR PASSWORD DATABASES
        directory = getcwd()
        db_folder = os.path.join(directory, 'database')

        for filename in os.listdir(db_folder):
            if filename.endswith(".txt") or filename.endswith(".lst"): db_lists.append(filename)

        for i in db_lists:
            db_file = os.path.join(db_folder, i)
            with open(db_file, encoding="cp437", mode='r') as f: db = f.read().splitlines()
            if pswd in db: offline_found+=1

        if offline_found > 0:
            print(f"Password was found in {offline_found}/15 of our common lists. Score: 0/8")
            return True
        else:
            print("\nPassword was not found in your database.")
            return False

    except Exception as e:
        # print(e)
        print("\nAn error occured: coudn't check downloaded database.")
        return None


def checker(online=None, offline=None):
    try:
        pswd = input("Enter your password: ")
        if offline==None:
            choice = input("Do you wish to check your password against your current database? (Y/n) ")
            offline = (True if (choice.lower() == "y" or choice.lower() == "yes") else False)

        if online==None:
            choice = input("\nDo you wish to check your password against our online database?\nIt will take longer to check, but will be more thorough. (Y/n) ")
            online = (True if (choice.lower() == "y" or choice.lower() == "yes") else False)

        result = score(pswd)
        db_off, db_on = None, None
        if offline == True:
            db_off=offline_check(pswd)
        if online == True:
            db_on=online_check(pswd)
        
        if db_off == True or db_on == True:
            input("\nPress \"enter\" to restart\nPress \"ctrl+c\" to exit")
            checker(online, offline)

        # WE GIVE THE FINAL RESULT
        if result < 4: print("\nThe password is quite weak!", end=" ")
        elif result == 4:print("\nThe password is ok!", end=" ")
        elif result > 4: print("\nThe password is pretty good!", end=" ")
        elif result > 6: print("\nThe password is strong!", end=" ")
        percentage = result * 100 / 8
        if len(pswd) <= 4:
            percentage /= 5
        print(f"Score: {str(result)}/8  ({round(percentage, 2)}% of security) ")
        if len(pswd) <= 4:
            print("Your password is way to short.\nA password should be at least 8 characters long.")

        input("\nPress \"enter\" to restart\nPress \"ctrl+c\" to exit")
        clear()
        checker(online, offline)
    except KeyboardInterrupt:
        exit()

if __name__=="__main__":
    print("Press ctrl+c to exit the app\n")
    checker()