"""Main application"""

import re

import requests
from bs4 import BeautifulSoup
from dateutil import parser

from app import BASE_URL, HEADERS, LOGGER, RESOURCE_IDS, RESOURCE_NAMES 


def download_deep_explorations(region_id):
    """Download the deep explorations list"""
    # return read_deep_explorations()
    response = requests.get(
        '{}listed/upgrades/{}'.format(BASE_URL, region_id),
        headers=HEADERS
    )
    return parse_deep_explorations(response.text)

def read_deep_explorations():
    """Read deep_exploration file"""
    with open('deep_explorations.html') as file:
        return parse_deep_explorations(file)

def parse_deep_explorations(html):
    """Read the deep_explorations left"""
    soup = BeautifulSoup(html, 'html.parser')
    deep_explorations_tree = soup.find_all(class_='list_link')

    deep_explorations = {}
    for deep_exploration_tree in deep_explorations_tree:
        deep_exploration_id = int(deep_exploration_tree['user'])
        columns = deep_exploration_tree.find_all('td')
        deep_explorations[deep_exploration_id] = {
            'resource_type': RESOURCE_NAMES[columns[1].text.replace(' resources', '').lower()],
            'until_date_time': parser.parse(columns[2].string),
        }
    return deep_explorations

def deep_explorate(state_id, capital_id, resource_type, amount, alt):
    """Main function"""
    response = requests.get(
        '{}main/content'.format(BASE_URL),
        headers=HEADERS
    )
    soup = BeautifulSoup(response.text, 'html.parser')
    state_div = soup.find_all('div', {'class': 'index_case_50'})[1]
    action = state_div.findChild()['action']
    current_state_id = int(re.sub('.*/', '', action))
    LOGGER.info('Current state %s', current_state_id)
    params = {}
    if current_state_id != state_id:
        LOGGER.info(
            'Not in the correct state, %s instead of %s', 
            current_state_id, state_id
        )
    else:
        params = {}
        # if current_state_id != state_id:
        #     params['alt'] = True
        if alt:
            params['alt'] = True

        json_data = {
            'tmp_gov': '{}_{}'.format(resource_type, amount)
        }

        requests.post(
            '{}parliament/donew/34/{}_{}/{}'.format(
                BASE_URL, resource_type, amount, capital_id
            ),
            headers=HEADERS,
            params=params,
            json=json_data
        )

    response = requests.get(
        '{}parliament/index/{}'.format(BASE_URL, capital_id),
        headers=HEADERS
    )
    soup = BeautifulSoup(response.text, 'html.parser')
    active_laws = soup.find('div', {'id': 'parliament_active_laws'})
    deep_exploration_name = RESOURCE_IDS[resource_type]
    exploration_laws = active_laws.findAll(text='Deep exploration,')
    LOGGER.info('Resources exploration: state, %s deep_explorations', deep_exploration_name)
    for exploration_law in exploration_laws:
        action = exploration_law.parent.parent['action']
        action = action.replace('law', 'votelaw')
        result = requests.post(
            '{}{}/pro'.format(BASE_URL, action),
            params=params,
            headers=HEADERS
        )
        LOGGER.info('Response: %s', result.text)
