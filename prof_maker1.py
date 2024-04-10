import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from bs4 import BeautifulSoup
import requests
import sys

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

def keep_numeric_digits(input_string):
    return ''.join(char for char in input_string if char.isdigit())



def leetcode(handle):
    d={}
    d["Handle"]=handle
    url = "https://leetcode-stats-api.herokuapp.com/"+handle+"/"
    response=requests.get(url)

    if response.status_code != 200:
        raise print('User not Found')

    profile=response.json()

    # community stats
    views=0
    solution=0
    Discuss=0
    Reputation=profile["reputation"]
    d["Community_Stats"]={"Views":views,"Solution":solution,"Discuss":Discuss,"Reputation":Reputation}


    #Ratings and stuff
    rating = 1579
    global_rank_contest_attempted = 2
    # rating_percentile = soup.find('div', {'class': 'text-label-1 dark:text-dark-label-1 text-2xl'}).text
    no_ques_solve = profile["totalSolved"]
    no_of_badges=2

    no_easy_ques_solve=profile["easySolved"]
    no_med_ques_solve=profile["mediumSolved"]
    no_diff_ques_solve=profile["hardSolved"]

    global_rank_contest = "127,814/518,551"
    contest_attempted = 2

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

# gmail="kanishkrajmittal@gmail.com"
# l_handle="KanishkMittal"
# c_handle="KanishkMittal"
# gfg_handle="kanishkra56bh"

# gmail="harshsharma@gmail.com"
# l_handle="XoXoHarsh"
# c_handle="XOXOHarsh"
# gfg_handle="harshsharma20503"
# dic={"codeforces":codeforces(c_handle),"leetcode":leetcode(l_handle),"gfg":gfg(gfg_handle)}

gmail = sys.argv[1]
prof=db.collection("users").document(gmail).get().to_dict()
dic={}
if "leetcode" in prof:
    l_handle=prof['leetcode']["Handle"]
    dic["leetcode"]=leetcode(l_handle)
if "codeforces" in prof:
    c_handle=prof['codeforces']["Handle"]
    dic["codeforces"]=codeforces(c_handle)
if "gfg" in prof:
    print("rgswa")
    gfg_handle=prof['gfg']["Handle"]
    dic["gfg"]=gfg(gfg_handle)


#leetcode
db.collection("users").document(gmail).set(dic)
