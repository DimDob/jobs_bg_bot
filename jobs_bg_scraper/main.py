import logging
import time
from bs4 import BeautifulSoup
import requests

from jobs_bg_scraper.save_as_xlsx import execute

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

start_time = time.time()


def returnKey(val):
    key_list = list(resultDict.keys())
    val_list = list(resultDict.values())

    position = val_list.index(val)
    return key_list[position]


URL = 'https://www.jobs.bg/front_job_search.php?subm=1&categories%5B%5D=56&techs%5B%5D=Python'

response = requests.get(URL
                        )  # here i get the response from the URI
soup = BeautifulSoup(response.text, 'lxml')  # creating a soup object
jobs = []
companies = []

for x in range(20):  # appending jobs
    a = soup.find_all('a', class_='black-link-b')
    title = a[x]['title']
    jobs.append(title)

for c in range(20):  # appending companies
    companiesArr = soup.find_all('div', class_='secondary-text')
    currentCompany = companiesArr[c].text
    companies.append(currentCompany)

resultDict = dict(zip(companies, jobs))  # name:position dict - zipping two lists

pr = ''

for kvpt in resultDict.items():  # string formatting for output
    pr += f"{kvpt[0]} searches for {kvpt[1]}" + '\n'

companiesData = {'Jr': [], 'Mid': [], 'Senior': []}  # level:companies names dict

jobsData = {'Junior': 0, 'Middle': 0, 'Senior': 0}  # level:jobs dict

for job in resultDict.values():  # filling the objects
    if 'Junior' in job:

        key = returnKey(job)
        jobsData['Junior'] += 1
        companiesData['Jr'].append(key)

    elif 'Middle' in job:
        key = returnKey(job)
        jobsData['Middle'] += 1
        companiesData['Mid'].append(key)

    elif 'Senior' in job:
        key = returnKey(job)
        jobsData['Senior'] += 1
        companiesData['Senior'].append(key)

outputData = {}  # output dict companyName:job type offers

jobsDataVals = list(jobsData.values())
companiesDataVals = list(companiesData.values())

for x in range(3):
    outputData[tuple(companiesDataVals[x])] = jobsDataVals[x]

output = ''

strings = ['Juniors', 'Middles', 'Seniors']
i = 0
for kvpt in outputData.items():  # string formatting for output
    if kvpt[1] == 0:
        output += 'There are currently no middle developers searched.' + '\n'
        continue
    output += f"There are {kvpt[1]} {strings[i]} searched right now by {len(kvpt[0])} companies - {', '.join(map(str, kvpt[0]))}" + '\n'
    i += 1

logging.info(pr)
logging.info(output)


def main():  # downloading src links

    resultLink = soup.find_all('a', class_='black-link-b')

    for x in range(len(jobs)):
        link = resultLink[x]['href']
        title = resultLink[x]['title']
        with open('output/offers.txt', 'a') as f:
            f.writelines(f'{title} -> {link}\n')

    execute()
    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
