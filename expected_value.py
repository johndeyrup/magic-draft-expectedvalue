'''
Created on Nov 23, 2014

@author: John
'''
import urllib.request
from bs4 import BeautifulSoup
response = urllib.request.urlopen('http://www.mtggoldfish.com/prices/online/boosters')
html = response.read()
soup = BeautifulSoup(html)

#Prices for each booster set not sure of a better way to write this beyond doing the tedious sorting of code
def get_prices():
    price_list = []
    for tag in soup.find_all("div", class_='priceList'):
        for subtag in tag.find_all('dd', class_='priceList-prices-price'):
            price_list.append(subtag.contents[0].strip())
    return price_list

#Get names for each booster
def get_names():
    booster_name = []
    for tag in soup.find_all("div", class_='priceList'):
        for subtag in tag.find_all('dt', class_='priceList-prices-card'):
            for link in subtag.find('a'):
                booster_name.append(link)
    return booster_name

#Returns the payout for a given booster
def get_booster_payout(boost_list, booster_name):
    for x in range(len(boost_list)):
        if(booster_name == boost_list[x][0]):
            return float(boost_list[x][1])
            break
      
#Gives the likelihood of each event given a certain probability of win and loss       
def calc_probabilities(prob_win):
    prob_loss = 1 - prob_win
    competition_probabilities = []
    #Competition is single elimination ofr 4-3-2-2 and 8-4
    competition_probabilities.append([[prob_win**3,4],[prob_win**2*prob_loss,3], [prob_win*prob_loss,2], ['4-3-2-2']])
    competition_probabilities.append([[prob_win**3,8],[prob_win**2*prob_loss,4],['8-4']])
    #Probabilities for getting 2 wins in swiss = WWL, WLW, LWW
    #Probabilities for getting 1 win in swiss = LLW, LWL, WLL
    competition_probabilities.append([[prob_win**3,3],[3*prob_win**2*prob_loss,2], [3*prob_win*prob_loss**2,1],["Swiss"]])
    return competition_probabilities
 
def calc_exp_value(match_results, pay_out, booster_type):
    print('Expected value for %s' % booster_type)
    cost = pay_out*3 + 2
    for result in match_results:
        expected_value = 0
        for subresult in result:
            if len(subresult) > 1:
                print("There is a %f likelihood that you will gain tickets %f" % (subresult[0],subresult[1]*pay_out))
                expected_value += subresult[0] * subresult[1] * pay_out
            else:
                print("By playing %s your expected value ignoring cards is %f with expected earnings of %f" % 
                      (subresult[0], expected_value, expected_value-cost))
                print()
    
booster_list = list(zip(get_names(), get_prices()))
booster_name = 'Magic 2015 Booster'
win_results = calc_probabilities(.60)
payout = get_booster_payout(booster_list,booster_name)
calc_exp_value(win_results, payout, booster_name)