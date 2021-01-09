import json
import zipfile as zp
import re
import pandas as pd

archive = zp.ZipFile('data/data.zip', 'r')


def municipality_cumulative_cases_data():

    # Open det test csv for municipalities to create a dictionary for the municipalities and their codes.
    muni_test_pos = 'Municipality_test_pos.csv'

    muni_test_data = archive.open(muni_test_pos)
    muni_test_df = pd.read_csv(muni_test_data, sep=';')
    muni_test_df['Kommune_(id)'] = muni_test_df['Kommune_(id)'].astype(str)  # to str so we avoid floats
    muni_code_dict = pd.Series(muni_test_df['Kommune_(id)'].values, index=muni_test_df['Kommune_(navn)']).to_dict()

    # add code for Copenhagen manually, as it is called København in the other files
    muni_code_dict['Copenhagen'] = '101'

    # Open the time series of cases for the municipalities
    municipality_cases = 'Municipality_cases_time_series.csv'

    cases_data = archive.open(municipality_cases)
    cases_df = pd.read_csv(cases_data, sep=';')

    # Melt the dataframe to get three columns, one for date, municipality, and cases.
    melt_cases = pd.melt(cases_df,
                         id_vars=['date_sample'],
                         value_vars=cases_df.columns[1:],
                         var_name=['municipality'],
                         value_name='infected')

    # Group the melted dataframe by the municipality and sum the cases.
    # Create a new column called 'code' by mapping the municipalities with their codes, using muni_code_dict.
    cases_sum_df = melt_cases.groupby('municipality').sum().reset_index()  # Not drop=True as it removes muni
    cases_sum_df['code'] = cases_sum_df['municipality'].map(muni_code_dict)

    # zfill the municipality codes to get the same numbers as in the geojson
    cases_sum_df['code'] = cases_sum_df['code'].apply(lambda x: str(x).zfill(4))

    return cases_sum_df


def cases_by_sex_data():
    # Open data in archive and load to dataframe
    # use decimal=',' to avoid (european) thousand separator confusion
    cases_by_sex = archive.open('Cases_by_sex.csv')
    cases_by_sex_df = pd.read_csv(cases_by_sex, sep=';', decimal=',')

    # Strip whitespace around strings and change columns names
    cases_by_sex_df.columns = ['age_group', 'women', 'men', 'total']
    cases_by_sex_df['total'] = cases_by_sex_df['total'].str.strip().str.replace('.', '').astype(int)
    cases_by_sex_df['women'] = cases_by_sex_df['women'].str.strip().str.replace('.', '')
    cases_by_sex_df['men'] = cases_by_sex_df['men'].str.strip().str.replace('.', '')

    # Create two new columns from percent data in women and men columns
    cases_by_sex_df['women_percent'] = cases_by_sex_df \
        .apply(lambda x: re.sub('[()]', '', x['women'].split(' ')[1]) + '%', axis=1)
    cases_by_sex_df['men_percent'] = cases_by_sex_df \
        .apply(lambda x: re.sub('[()]', '', x['men'].split(' ')[1]) + '%', axis=1)

    # Remove the percent parentheses in women and men columns
    cases_by_sex_df['women'] = cases_by_sex_df.apply(lambda x: x['women'].split(' ')[0], axis=1).astype(int)
    cases_by_sex_df['men'] = cases_by_sex_df.apply(lambda x: x['men'].split(' ')[0], axis=1).astype(int)

    return cases_by_sex_df


def daily_infected_data():
    # Open the time series of cases for the municipalities
    municipality_cases = 'Municipality_cases_time_series.csv'

    cases_data = archive.open(municipality_cases)
    cases_df = pd.read_csv(cases_data, sep=';')

    total_daily = cases_df.groupby('date_sample').sum().sum(axis=1).values
    cases_df['total_daily'] = total_daily

    return cases_df


def daily_tests_data():
    # Open the time series of tests over time
    municipality_tests = 'Test_pos_over_time.csv'

    tests_data = archive.open(municipality_tests)
    tests_df = pd.read_csv(tests_data, sep=';')
    tests_df = tests_df.iloc[:-2, :]

    tests_df['Tested'] = tests_df['Tested'].str.strip().str.replace('.', '').astype(int)

    return tests_df


def daily_tests_accumulated():
    # Open the time series of tests over time
    municipality_tests = 'Test_pos_over_time.csv'

    tests_data = archive.open(municipality_tests)
    tests_df = pd.read_csv(tests_data, sep=';', decimal=',')
    tests_df['NotPrevPos'] = tests_df['NotPrevPos'].str.strip().str.replace('.', '').astype(int)
    tests_df['NewPositive'] = tests_df['NewPositive'].str.strip().str.replace('.', '').astype(int)
    tests_df['Tested'] = tests_df['Tested'].str.strip().str.replace('.', '').astype(int)

    total = tests_df.iloc[-1, :]

    return total['Tested'], total['NotPrevPos'], total['NewPositive']


def daily_infected_percent_data():
    municipality_tested = 'Municipality_tested_persons_time_series.csv'

    municipality_tested_data = archive.open(municipality_tested)
    municipality_tested_df = pd.read_csv(municipality_tested_data, sep=';')

    total_daily = municipality_tested_df.groupby('PrDate_adjusted').sum().sum(axis=1).values
    municipality_tested_df['total_daily'] = total_daily
    municipality_tested_df = municipality_tested_df.iloc[:, [0, -1]]
    municipality_tested_df = municipality_tested_df.iloc[21:, :].reset_index(drop=True)  # Start from march 1st

    cases_df = daily_infected_data()  # Get cases from other function
    cases_df = cases_df.iloc[3:, [0, -1]]  # Start from march 1st

    percent_df = pd.DataFrame()
    percent_df['date_sample'] = cases_df['date_sample']
    percent_df['percent_positive'] = cases_df['total_daily'].values/municipality_tested_df['total_daily'].values * 100

    # Last value is not correct as all data is not up to date yet
    percent_df = percent_df.iloc[:-1, :]

    return percent_df


def municipality_infected_data():
    # Open the time series of cases for the municipalities
    municipality_cases = 'Municipality_cases_time_series.csv'

    cases_data = archive.open(municipality_cases)
    cases_df = pd.read_csv(cases_data, sep=';')

    # Melt the dataframe to get three columns, one for date, municipality, and cases.
    melt_cases = pd.melt(cases_df,
                         id_vars=['date_sample'],
                         value_vars=cases_df.columns[1:],
                         var_name=['municipality'],
                         value_name='infected')

    mask = melt_cases['municipality'].isin(['NA'])
    melt_cases = melt_cases.loc[~mask, :]  # Makes sure that NA is not included as a municipality
    muni_infected = melt_cases.groupby('municipality').sum().sort_values('infected', ascending=False)

    return muni_infected


def admitted_over_time_data():
    admitted_over_time = 'Newly_admitted_over_time.csv'
    admitted_data = archive.open(admitted_over_time)
    admitted_df = pd.read_csv(admitted_data, sep=';')
    admitted_df = admitted_df.iloc[:, [0, -1]]

    return admitted_df


def deaths_over_time_data():
    deaths_over_time = 'Deaths_over_time.csv'
    deaths_data = archive.open(deaths_over_time)
    deaths_df = pd.read_csv(deaths_data, sep=';')
    deaths_df.columns = ['date', 'deaths']
    deaths_df = deaths_df.iloc[:-1, :]  # Remove the 'total' row

    return deaths_df


def deaths_cumulative_data():
    deaths_over_time = 'Deaths_over_time.csv'
    deaths_data = archive.open(deaths_over_time)
    deaths_df = pd.read_csv(deaths_data, sep=';')
    deaths_df.columns = ['date', 'deaths']
    deaths_df = deaths_df.iloc[:-1, :]  # Remove the 'total' row

    deaths_df = deaths_df.set_index('date')
    deaths_df = deaths_df.cumsum()

    return deaths_df


