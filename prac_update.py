import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from bs4 import BeautifulSoup
import requests
import datetime
import pytz
from time import sleep
# from selenium import webdriver
# from selenium.webdriver import Chrome
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import FCMManager as fcm
from datetime import date

tokens = ["eb-GTGGgRUOzuiFlPC1EXL:APA91bG6RnoxXJjnr0HrVEMJ4MZQVBI-O51JhClhjRqyYyH9L2ilXVrdprPUR0nkKaXoIpvAd3dQ-9eKQwD1CZX_2u-XYIgQkyJHuFdfQq2KpdmHwpW7flX2Qv_g2tBvA6wE28aph80O"]
# fcm.sendPush(title,description,tokens)
fcm.sendPush("Reminder", "Have you solved today's problem?", tokens)

count=1

def keep_numeric_digits(input_string):
    return ''.join(char for char in input_string if char.isdigit())


def is_within_two_days(given_date):
    # Parse the given date string to a datetime object
    given_date_obj = datetime.datetime.strptime(given_date, '%Y-%m-%d')

    # Get the current date
    current_date = datetime.datetime.now()

    # Calculate the difference between the given date and the current date
    date_difference = given_date_obj - current_date

    # Check if the absolute difference is less than or equal to 2 days
    return abs(date_difference.days) <= 1

def get_current_day():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    current_day_index = datetime.datetime.today().weekday()
    current_day = days[current_day_index]
    return str(current_day)

def get_current_time():
    ist = pytz.timezone('Asia/Kolkata')  # Set the time zone to IST
    current_time_ist = datetime.datetime.now(ist).time()
    formatted_time = current_time_ist.strftime('%H:%M:%S')
    return str(formatted_time)

def get_upcoming_day_date(day_name,time):
    if(get_current_day()==day_name and get_current_time()<time):
        return datetime.date.today()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # Get the current date
    current_date = datetime.date.today()
    # Calculate the days until the next occurrence of the specified day
    days_until_next_day = (current_date.weekday() - days.index(day_name)) % 7
    # Calculate the date of the upcoming day
    upcoming_date = current_date + datetime.timedelta(days=(7 - days_until_next_day))
    return upcoming_date



def leetcode(handle):
    d={}
    d["Handle"]=handle
    url = "https://leetcode.com/"+handle+"/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # community stats
    community_stats=soup.find_all(class_='flex items-center space-x-2 text-[14px]')
    views=community_stats[0].text
    for i in range(len(views)):
        if views[i].isdigit():
            break;
    views=views[i:]
    solution=community_stats[1].text
    for i in range(len(solution)):
        if solution[i].isdigit():
            break;
    solution=solution[i:]
    Discuss=community_stats[2].text
    for i in range(len(Discuss)):
        if Discuss[i].isdigit():
            break;
    Discuss=Discuss[i:]
    Reputation=community_stats[3].text
    for i in range(len(Reputation)):
        if Reputation[i].isdigit():
            break;
    Reputation=Reputation[i:]
    d["Community_Stats"]={"Views":views,"Solution":solution,"Discuss":Discuss,"Reputation":Reputation}

    #Ratings and stuff
    rating = soup.find(class_='text-label-1 dark:text-dark-label-1 flex items-center text-2xl').text
    global_rank_contest_attempted = soup.find_all(class_='text-label-1 dark:text-dark-label-1 font-medium leading-[22px]')
    # rating_percentile = soup.find('div', {'class': 'text-label-1 dark:text-dark-label-1 text-2xl'}).text
    no_ques_solve = soup.find(class_='text-[24px] font-medium text-label-1 dark:text-dark-label-1').text
    type_ques_solve=soup.find_all(class_='mr-[5px] text-base font-medium leading-[20px] text-label-1 dark:text-dark-label-1')
    no_of_badges=soup.find(class_='text-label-1 dark:text-dark-label-1 mt-1.5 text-2xl leading-[18px]').text

    no_easy_ques_solve=int(type_ques_solve[0].text)
    no_med_ques_solve=int(type_ques_solve[1].text)
    no_diff_ques_solve=int(type_ques_solve[2].text)

    global_rank_contest = global_rank_contest_attempted[0].text
    contest_attempted = int(global_rank_contest_attempted[1].text)

    d["Current_Rating"]=rating
    d["Global_Rank_In_Contest"] = global_rank_contest
    d["Contest_Attempted"] =contest_attempted
    # print("Rating Precentile = ",rating_percentile)
    d["Number_Of_Ques_solved"] = no_ques_solve
    d["Easy_Ques_Solved"]=no_easy_ques_solve
    d["Medium_Ques_Solved"]= no_med_ques_solve
    d["Difficult_Ques_Solved"] = no_diff_ques_solve
    d["Number_Of_Badges"]= no_of_badges
    return d

def codeforces(handle):
    d={}
    d["Handle"]=handle
    url='https://codeforces.com/api/user.info?handles='+handle
    response=requests.get(url)

    if response.status_code != 200:
        raise print('User not Found')

    profile=response.json()["result"][0]
    contributions=profile["contribution"]
    rating=profile["rating"]
    No_of_friends=profile["friendOfCount"]
    Rank=profile["rank"]
    max_rating=profile["maxRating"]
    max_rank=profile["maxRank"]

    d["Number_Of_Contributions"]=contributions
    d["Current_Rating"]=rating
    d["Number_Of_Friends"]=No_of_friends
    d["Current_Rank"]=Rank
    d["Max_Rating"]=max_rating
    d["Max_Rank"]=max_rank

    url="https://codeforces.com/profile/"+handle
    response=requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    problem_solved=soup.find_all(class_='_UserActivityFrame_counterValue')
    No_of_ques_solve=problem_solved[0].text
    max_streak=problem_solved[3].text
    d["Number_Of_Ques_solved"] = keep_numeric_digits(No_of_ques_solve)
    d["Max_Streak"]=max_streak
    return d


def gfg(handle):
    url = "https://auth.geeksforgeeks.org/user/"+handle+"/?utm_source=geeksforgeeks&utm_medium=my_profile&utm_campaign=auth_user"
    response=requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # rank=soup.find(class_='rankNum').text
    POTD_streak=soup.find(class_='streakCnt tooltipped').text
    Institute=soup.find(class_='basic_details_data').text
    score_card=soup.find_all(class_='score_card_value')
    Coding_score=score_card[0].text
    problem_solved=score_card[1].text
    monthly_coding_score=score_card[2].text

    # Find the tabs containing the number of questions for each difficulty
    tabs = soup.find_all('li', class_='tab')
    # Create a dictionary to store the count for each difficulty
    difficulty_count = {'easy': 0, 'medium': 0, 'hard': 0}
    for tab in tabs:
        # Extract the difficulty level and count from the 'href' attribute
        difficulty = tab.find('a')['href'].replace('#', '')
        count = int(tab.find('a').text.split('(')[1].split(')')[0])
        # Update the dictionary with the count for the corresponding difficulty
        difficulty_count[difficulty] = count
    
    d={}
    d["Handle"]=handle
    # d["Rank"]=rank
    d["POTD_Streak"]=POTD_streak
    d["Institute"]=Institute
    d["Coding_Score"]=Coding_score
    d["Problem_Solved"]=problem_solved
    d["Monthly_Coding_Score"]=monthly_coding_score
    d["Easy_Ques_Solved"]=difficulty_count["easy"]
    d["Medium_Ques_Solved"]= difficulty_count['medium']
    d["Hard_Ques_Solved"] = difficulty_count['hard']

    return d



    


def extract_info(problem_description):
    # Find the indices of key phrases
    problem_statement_index = problem_description.find("Problem Statement")
    examples_index = problem_description.find("Example")
    constraints_index = problem_description.find("Constraints")
    your_task_index = problem_description.find("Your Task")

    # Extract the corresponding sections using string slicing
    problem_statement = problem_description[problem_statement_index + len("Problem Statement"):examples_index].strip()
    examples_section = problem_description[examples_index + len("Examples"):constraints_index].strip()
    your_task = problem_description[your_task_index + len("Your Task"):constraints_index].strip()
    constraints = problem_description[constraints_index + len("Constraints"):].strip()

    # Convert examples_section to a dictionary
    # examples_dict = {}
    # examples_list = examples_section.split("\n")
    # current_example = ""
    # for line in examples_list:
    #     line = line.strip()
    #     if line.startswith("Example"):
    #         current_example = line
    #         examples_dict[current_example] = {"Input": {}, "Output": "", "Explanation": ""}
    #     elif line.startswith("Input:"):
    #         examples_dict[current_example]["Input"] = eval(line[len("Input:"):].strip())
    #     elif line.startswith("Output:"):
    #         examples_dict[current_example]["Output"] = eval(line[len("Output:"):].strip())
    #     elif line.startswith("Explanation:"):
    #         examples_dict[current_example]["Explanation"] = line[len("Explanation:"):].strip()

    # Create the final dictionary

    problem_statement=problem_statement.replace("\n","@!")
    examples_section=examples_section.replace("\n","@!")
    constraints=constraints.replace("\n","@!")
    your_task=your_task.replace("\n","@!")
    problem_dict = {
        "Problem Statement": problem_statement,
        "Examples": examples_section,
        "Constraints": constraints+"@! Your Task: "+your_task
        # "Your Task": your_task
    }
    return problem_dict



# def leetcode_potd():
#     driver = webdriver.Chrome()
#     driver.get("https://leetcode.com/problemset/all/")
#     sleep(3)

#     # Click on the "Solve problem" button
#     daily_ques = driver.find_element(By.XPATH, '(//div[@class="truncate"])[1]')
#     daily_ques.click()

#     sleep(2)
#     driver.switch_to.window(driver.window_handles[0])
#     # print(driver.current_url)

#     title = driver.find_element(By.XPATH, "//div[@class='flex h-full items-center']").text
#     ques = driver.find_element(By.XPATH, '(//p)[1]').text+driver.find_element(By.XPATH, '(//p)[2]').text
#     ex1 = driver.find_element(By.XPATH, '(//pre)[1]').text
#     ex2 = driver.find_element(By.XPATH, '(//pre)[2]').text
#     constraints = driver.find_element(By.XPATH, '(//ul)[2]').text

#     title=title.replace("\n","@!")
#     ques=ques.replace("\n","@!")
#     constraints= constraints.replace("\n","@!")
#     ex1=ex1.replace("\n","@!")
#     ex2=ex2.replace("\n","@!")

#     data = {"LeetCode": {"title":title,"Problem Statement": ques, "Examples": ex1+"@!"+ex2,
#                     "Constraints": constraints}}
#     # print(data["LeetCode"]["Examples"])
#     return data


# def gfg_potd():
#     # Create a webdriver instance
#     # Create a webdriver instance
#     driver = Chrome()

#     # Navigate to the link
#     driver.get("https://www.geeksforgeeks.org/problem-of-the-day")
#     sleep(5)

#     # Click on the "Solve problem" button using JavaScript
#     solve_button = driver.find_element(
#         By.XPATH, '//button[@class="ui button problemOfTheDay_POTDCntBtn__SSQfX"]')
#     driver.execute_script("arguments[0].click();", solve_button)
#     sleep(1)
#     driver.switch_to.window(driver.window_handles[1])
#     s = driver.current_url


#     attributes = driver.find_element(
#         By.XPATH, '(//div)[@class="problems_problem_content__Xm_eO"]').text
#     # print(attributes)

#     # Close the browser
#     driver.quit()
#     # Extract information and print the dictionary
#     attributes="Problem Statement"+attributes
#     result_dict = extract_info(attributes)
#     d={}
#     d["GeeksForGeeks"]=result_dict
#     return d



def codeforces_contest():
    url=" https://codeforces.com/api/contest.list?gym=false"
    response=requests.get(url)

    if response.json()["status"] != "OK":
        raise print('User not Found')
    d={}
    profile=response.json()["result"]
    global count
    for contest in profile[0:5]:
        # d["c_id"]=contest["id"]
        c_name=contest["name"]
        # d["c_duration"]=contest["durationSeconds"]/3600
        timestamp=contest["startTimeSeconds"]
        start_time_utc = datetime.datetime.utcfromtimestamp(timestamp)
        ist = pytz.timezone('Asia/Kolkata')
        start_time_ist = start_time_utc.replace(tzinfo=pytz.utc).astimezone(ist)
        formatted_start_time = start_time_ist.strftime('%Y-%m-%d %H:%M:%S')
        date=str(start_time_ist.date())
        if is_within_two_days(date):
            fcm.sendPush("Reminder", "Upcoming Codeforces Contest On "+date, tokens)

        time=str(start_time_ist.time())
        d[str(count)]={"Name":c_name,"Platform":"Codeforces","Date":date,"Time":time}
        count=count+1
    return d
    # db.collection("contests").document("contests").set(d)

def leetcode_contest():
    url="https://leetcode.com/contest/"
    response=requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    d={}
    global count
    name=soup.find_all(class_='transition-colors group-hover:text-blue-s dark:group-hover:text-dark-blue-s')
    c_name=name[0].text
    c_date=str(get_upcoming_day_date("Sunday","08:00:00"))
    if is_within_two_days(c_date):
        fcm.sendPush("Reminder", "Upcoming Leetcode Contest On "+c_date, tokens)

    c_time="08:00:00"
    d[str(count)]={"Name":c_name,"Platform":"Leetcode","Date":c_date,"Time":c_time}
    count=count+1



    c_name=name[1].text
    c_date=str(get_upcoming_day_date("Saturday","20:00:00"))
    if is_within_two_days(c_date):
        fcm.sendPush("Reminder", "Upcoming Leetcode Contest On "+c_date, tokens)

    c_time="20:00:00"
    d[str(count)]={"Name":c_name,"Platform":"Leetcode","Date":c_date,"Time":c_time}
    count=count+1
    return d
    # db.collection("contests").document("contests").set(d)

def gfg_contest():
    url="https://practice.geeksforgeeks.org/events/rec/gfg-weekly-coding-contest"
    response=requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    d={}
    global count
    c_name=soup.find(class_='sofia-pro events_upcomingEventDescTxt__xgvgK').text
    c_date=str(get_upcoming_day_date("Sunday","19:00:00"))
    if is_within_two_days(c_date):
        fcm.sendPush("Reminder", "Upcoming GFG Contest On "+c_date, tokens)

    c_time="19:00:00"
    d[str(count)]={"Name":c_name,"Platform":"GeeksForGeeks","Date":c_date,"Time":c_time}
    count=count+1
    return d
    # db.collection("contests").document("contests").set(d)
    # d[c_name]={"c_date":c_date,"c_time":c_time}
    # db.collection("contest").document("gfg").set(d)

def contest_update():
    dict1 = leetcode_contest()
    dict2 = codeforces_contest()
    dict3 = gfg_contest()

    # Merge dictionaries using {**d1, **d2, **d3} syntax
    d = {**dict1, **dict2, **dict3}
    db.collection("contests").document("contests").set(d)

def user_update():   
    users = db.collection("users").get()
    for user in users:
        gmail=user.id
        prof=user.to_dict()
        dic={}
        if "leetcode" in prof:
            l_handle=prof['leetcode']["Handle"]
            dic["leetcode"]=leetcode(l_handle)
            old_rating=str(prof["leetcode"]["Current_Rating"])
            new_rating=str(dic["leetcode"]["Current_Rating"])
            if old_rating>new_rating:
                fcm.sendPush("Rating Changed", "Leetcode Rating Decreased To "+new_rating, tokens)
            if old_rating<new_rating:
                fcm.sendPush("Rating Changed", "Leetcode Rating Increased To "+new_rating, tokens)

        if "codeforces" in prof:
            c_handle=prof['codeforces']["Handle"]
            dic["codeforces"]=codeforces(c_handle)
            old_rating=str(prof["codeforces"]["Current_Rating"])
            new_rating=str(dic["codeforces"]["Current_Rating"])
            if old_rating>new_rating:
                fcm.sendPush("Rating Changed", "Codeforces Rating Decreased To "+new_rating, tokens)
            if old_rating<new_rating:
                fcm.sendPush("Rating Changed", "Codeforces Rating Increased To "+new_rating, tokens)
        if "gfg" in prof:
            gfg_handle=prof['gfg']["Handle"]
            dic["gfg"]=gfg(gfg_handle)
        db.collection("users").document(gmail).update(dic)



# def POTD_update():
#     dict1 = leetcode_potd()
    
#     dict3 = gfg_potd()
#     d1={"Problem Statement":"Vasya is a sorcerer that fights monsters. Again. There are n monsters standing in a row, the amount of health points of the i-th monster is ai.@!Vasya is a very powerful sorcerer who knows many overpowered spells. In this fight, he decided to use a chain lightning spell to defeat all the monsters. Let's see how this spell works.@!Firstly, Vasya chooses an index i of some monster (1≤i≤n) and the initial power of the spell x. Then the spell hits monsters exactly n times, one hit per monster. The first target of the spell is always the monster i. For every target except for the first one, the chain lightning will choose a random monster who was not hit by the spell and is adjacent to one of the monsters that already was hit. So, each monster will be hit exactly once. The first monster hit by the spell receives x damage, the second monster receives (x−1) damage, the third receives (x−2) damage, and so on.@!Vasya wants to show how powerful he is, so he wants to kill all the monsters with a single chain lightning spell. The monster is considered dead if the damage he received is not less than the amount of its health points. On the other hand, Vasya wants to show he doesn't care that much, so he wants to choose the minimum initial power of the spell x such that it kills all monsters, no matter which monster (among those who can get hit) gets hit on each step.@!Of course, Vasya is a sorcerer, but the amount of calculations required to determine the optimal spell setup is way above his possibilities, so you have to help him find the minimum spell power required to kill all the monsters.@!Note that Vasya chooses the initial target and the power of the spell, other things should be considered random and Vasya wants to kill all the monsters even in the worst possible scenario.",
#           "Constraints":"time limit per test: 2 seconds@!memory limit per test: 256 megabytes@!input: standard input@!output: standard output@!Input@!The first line of the input contains one integer n(1≤n≤3⋅105) — the number of monsters.@!The second line of the input contains n integers a1,a2,…,an(1≤ai≤109), where ai is the amount of health points of the i-th monster.@!Output@!Print one integer — the minimum spell power required to kill all the monsters if Vasya chooses the first target optimally, and the order of spell hits can be any possible within the given rules.",
#           "Examples":"input@!6@!2 1 5 6 4 3@!output@!8@!input@!5@!4 4 4 4 4@!output@!8@!input@!2@!1 1000000000@!output@!1000000000"}
#     dict2 = {"Codeforces":d1}
#     # Merge dictionaries using {**d1, **d2, **d3} syntax
#     d = {**dict1,**dict2,**dict3}
#     db.collection("questions").document("POTD").set(d)


# cred = credentials.Certificate("/home/kanishk/Desktop/Python/firebase/credentials.json")
# firebase_admin.initialize_app(cred)
db=firestore.client() 
user_update()
contest_update()
# POTD_update()
