import pandas as pd


#visualisation of collected data via xlsx format.
def execute():
    # outputData variable stores each line from Auditor_names.txt file.
    outputData = open('output/offers.txt', 'r+')

    lines = [line.split(' -> ') for line in outputData]
    jobs = [line[0] for line in lines]
    urls = [line[1].strip() for line in lines]
    outputData.truncate(0) #clearing the content of the offers.txt file for the next run.
    # creating DF object and passing a dict containing all params for each cell
    df = pd.DataFrame({'Job Titles': jobs, 'URLs': urls})
    with pd.ExcelWriter(r'output/outputOffers.xlsx') as writer:
        df.to_excel(writer, sheet_name='JobsBG', index=False)
