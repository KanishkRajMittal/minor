import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from bs4 import BeautifulSoup
import requests
import codeforces_api

cred = credentials.Certificate("/home/kanishk/Desktop/Python/firebase/credentials.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

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
    anonim_cf_api = codeforces_api.CodeforcesApi ()
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
    d["Number_Of_Friends"]:No_of_friends
    d["Current_Rank"]=Rank
    d["Max_Rating"]=max_rating
    d["Max_Rank"]=max_rank
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
    d={}
    d["Handle"]=handle
    # d["Rank"]=rank
    d["POTD_Streak"]=POTD_streak
    d["Institute"]=Institute
    d["Coding_Score"]=Coding_score
    d["Problem_Solved"]=problem_solved
    d["Monthly_Coding_Score"]=monthly_coding_score
    return d

gmail="kanishkrajmittal@gmail.com"
l_handle="KanishkMittal"
c_handle="KanishkMittal"
gfg_handle="kanishkra56bh"

# gmail="harshsharma@gmail.com"
# l_handle="XoXoHarsh"
# c_handle="XOXOHarsh"
# gfg_handle="harshsharma20503"
dic={"codeforces":codeforces(c_handle),"leetcode":leetcode(l_handle),"gfg":gfg(gfg_handle)}

# prof=db.collection("users").document(gmail).get().to_dict()
# dic={}
# if "leetcode" in prof:
#     l_handle=prof['leetcode']["Handle"]
#     dic["leetcode"]=leetcode(l_handle)
# if "codeforces" in prof:
#     c_handle=prof['codeforces']["Handle"]
#     dic["codeforces"]=codeforces(c_handle)
# if "gfg" in prof:
#     print("rgswa")
#     gfg_handle=prof['gfg']["Handle"]
#     dic["gfg"]=gfg(gfg_handle)


#leetcode
db.collection("users").document(gmail).set(dic)

