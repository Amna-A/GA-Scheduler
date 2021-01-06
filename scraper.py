import requests
from bs4 import BeautifulSoup

def extract_value(text, prefix, suffix):
    prefix_index = text.find(prefix)
    text = text[prefix_index + len(prefix)::]
    suffix_index = text.find(suffix)
    value = text[0:suffix_index]
    clean_index = value.find('>')
    value = value[clean_index+1:]
    return value

def extract_data(dept):

    for result in response.json()['results']:
        course_name = result['title']
        course_uri = result['uri']
        response2 = requests.get(course_uri, verify=False)

        instructor_name = extract_value(
            response2.text, '<a href="/catalogue/instructor/', '</a>')
   
        if "<" in instructor_name:
            instructor_name = "TBD"

        course_dictionary = {
            "course name": "-".join(course_name.split("-", 2)[:2]),
            "instructor_name": instructor_name,
            #'course_uri': result['uri']
        }
        dataset[dept].append(course_dictionary)


'''- Scrapping each depatement data form the UofA website (graduate) into a csv fine to create the dataset.
------------------------------------------------------------------------------------------------
    * From each department in the faculty of engineering, will scrape:
        a- department name
        b- course name
        c- course instructor

    * Departments in the Faculty of Engineering at the UofA:
        1- Chemical and Materials Engineering (CME)
        2- Civil Engineering (CIV E)
        3- Electrical and Computer Engineering (ECE)
        4- Mechanical Engineering (MEC E)
        5- Biomedical Engineering (BME)
        6- Environmental Engineering (ENV E)
'''

# API to get search results
url = 'https://platform.cloud.coveo.com/rest/search/v2?organizationId=universityofalbertaproductionk9rdz87w'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    'Host': 'platform.cloud.coveo.com',
    'Authorization': 'Bearer xx23b52d3f-ba50-41b9-85dc-579dfbdd11a7',
    'Content-Type': 'application/x-www-form-urlencoded; charset="UTF-8"',
    'Origin': 'https://www.ualberta.ca',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.ualberta.ca/',
}
'''
* From each department in the faculty of engineering, will scrape:
    a- department name
    b- course name
    c- course instructor
'''
# list of titles
dataset = {
    "CME": [],
    "CIV E": [],
    "ECE": [],
    "MEC E": [],
}
titles = []
uris = []
# Make a GET request to fetch the raw HTML content
payload = r'''actionsHistory=%5B%7B%22name%22%3A%22Query%22%2C%22value%22%3A%22ECE%20course%22%2C%22time%22%3A%22%5C%222020-11-07T22%3A57%3A37.540Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22value%22%3A%22ECE%20course%22%2C%22time%22%3A%22%5C%222020-11-07T22%3A47%3A50.126Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22value%22%3A%22ECE%20course%22%2C%22time%22%3A%22%5C%222020-11-07T22%3A35%3A10.786Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22value%22%3A%22ECE%20course%22%2C%22time%22%3A%22%5C%222020-11-07T22%3A28%3A56.038Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22value%22%3A%22ECE%20course%22%2C%22time%22%3A%22%5C%222020-11-07T22%3A27%3A51.967Z%5C%22%22%7D%5D&referrer=&visitorId=7cafce27-97ab-459a-b812-dd5bfb7e07aa&isGuestUser=false&q=ECE%20course&aq=(%40ua__faculty%3D%3DEngineering)%20(%40ua__term%3D%3D%22Fall%202020%22)%20(%40ua__type%3D%3DGraduate)&searchHub=search&tab=Courses&locale=en&pipeline=ualberta-courses&firstResult=0&numberOfResults=1000&excerptLength=200&enableDidYouMean=true&sortCriteria=relevancy&queryFunctions=%5B%5D&rankingFunctions=%5B%5D&groupBy=%5B%7B%22field%22%3A%22%40ua__faculty%22%2C%22maximumNumberOfValues%22%3A11%2C%22sortCriteria%22%3A%22alphaascending%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%22Engineering%22%5D%2C%22queryOverride%22%3A%22ECE%20course%22%2C%22advancedQueryOverride%22%3A%22(%40ua__term%3D%3D%5C%22Fall%202020%5C%22)%20(%40ua__type%3D%3DGraduate)%22%7D%2C%7B%22field%22%3A%22%40ua__term%22%2C%22maximumNumberOfValues%22%3A13%2C%22sortCriteria%22%3A%22nosort%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%22Fall%202020%22%2C%22Winter%202020%22%2C%22Spring%202020%22%2C%22Summer%202020%22%2C%22Continuing%20Ed%20Winter%202020%22%2C%22Continuing%20Ed%20Fall%202020%22%2C%22Fall%202019%22%2C%22Winter%20%202019%22%2C%22Spring%202019%22%2C%22Summer%202019%22%2C%22Continuing%20Ed%20Winter%202019%22%2C%22Continuing%20Ed%20Fall%202019%22%5D%2C%22queryOverride%22%3A%22ECE%20course%22%2C%22advancedQueryOverride%22%3A%22(%40ua__faculty%3D%3DEngineering)%20(%40ua__type%3D%3DGraduate)%22%7D%2C%7B%22field%22%3A%22%40ua__credits%22%2C%22maximumNumberOfValues%22%3A6%2C%22sortCriteria%22%3A%22occurences%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%2C%7B%22field%22%3A%22%40ua__type%22%2C%22maximumNumberOfValues%22%3A11%2C%22sortCriteria%22%3A%22occurrences%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%22Graduate%22%5D%2C%22queryOverride%22%3A%22ECE%20course%22%2C%22advancedQueryOverride%22%3A%22(%40ua__faculty%3D%3DEngineering)%20(%40ua__term%3D%3D%5C%22Fall%202020%5C%22)%22%7D%2C%7B%22field%22%3A%22%40ua__campus%22%2C%22maximumNumberOfValues%22%3A11%2C%22sortCriteria%22%3A%22alphaascending%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%2C%7B%22field%22%3A%22%40ua__cat_subject_shortname%22%2C%22maximumNumberOfValues%22%3A6%2C%22sortCriteria%22%3A%22occurrences%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%5D&categoryFacets=%5B%5D&retrieveFirstSentences=true&timezone=Africa%2FCairo&enableQuerySyntax=true&enableDuplicateFiltering=true&enableCollaborativeRating=false&debug=false&allowQueriesWithoutKeywords=true'''
payload = payload
response = requests.post(url, headers=headers, data=payload, verify=False)
# titles.append(response.json()["results"][0]['title'])
extract_data("ECE")
#print(dataset['ECE'])

payload = payload.replace('ECE%20course', 'MEC%20E')
response = requests.post(url, headers=headers, data=payload)
#titles.append(response.json()["results"][0]['title'])
extract_data("MEC E")

# payload = payload.replace('MEC%20E', 'ENV%20E')
# response = requests.post(url, headers=headers, data=payload)
# extract_data("ENV E")

payload = payload.replace('MEC%20E', 'CIV%20E')
response = requests.post(url, headers=headers, data=payload)
extract_data("CIV E")

# payload = payload.replace('CIV%20E', 'BME')
# response = requests.post(url, headers=headers, data=payload)
# extract_data("BME")

payload = payload.replace('CIV%20E', 'CME')
response = requests.post(url, headers=headers, data=payload)
extract_data("CME")

import json
print(json.dumps(dataset))





