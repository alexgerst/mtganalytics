import json
import urllib2
import re

# Threshold below which we ignore ratings
threshold = 10

# Hard-coded strings for reference
base_url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid='
rating_regex = re.compile('class="textRatingValue">(\d+(\.\d*)?|\.\d+)</span>')
votes_regex = re.compile('class="totalVotesValue">(\d+)</span>')

# Dictionary to be populated from Gatherer
rating_dict = {
    'Artifact': {},
    'Creature': {},
    'Enchantment': {},
    'Instant': {},
    'Land': {},
    'Planeswalker': {},
    'Sorcery': {}
}

# Load card data from JSON file
print('Loading card data...')
with open('AllSetsArray-x.json') as data_file:
    card_set_list = json.load(data_file)
print('Card data loaded.')

# Iterate through all cards and fetch their ratings
for card_set in card_set_list:
    for card in card_set['cards']:
        print('Parsing ' + card['name'])
        if 'multiverseid' in card.keys() and 'types' in card.keys():
            url = base_url + str(card['multiverseid'])
            response = urllib2.urlopen(url)
            response_data = response.read()
            rating = float(rating_regex.search(response_data).group(1))
            votes = int(votes_regex.search(response_data).group(1))
            if votes >= threshold:
                for card_type in card['types']:
                    if card_type in rating_dict.keys():
                        if card['name'] not in rating_dict[card_type].keys():
                            rating_dict[card_type][card['name']] = []
                        rating_dict[card_type][card['name']].append(rating)
                        print(card_type + ' - ' + str(rating))

# Analyze the data and find average ratings
for card_type in rating_dict.keys():
    total_type_rating = 0.0
    num_type_ratings = 0
    for card_name in rating_dict[card_type].keys():
        total_card_rating = 0.0
        num_card_ratings = 0
        for card_rating in rating_dict[card_type][card_name]:
            total_card_rating += card_rating
            num_card_ratings++
        total_type_rating += total_card_rating / num_card_ratings
        num_type_ratings++
    print(card_type + ' Average Rating: ' + str(total_type_rating / num_type_ratings))

