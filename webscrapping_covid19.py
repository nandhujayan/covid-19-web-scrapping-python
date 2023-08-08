import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.worldometers.info/coronavirus/"

headers = {
    "User-Agent": "Your User Agent String"
}

max_retries = 5
retry_delay = 5  # seconds

covid_data = []

for retry in range(max_retries):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        break  # Exit the loop if the request is successful
    except requests.RequestException as e:
        print(f"Request error (Retry {retry + 1}/{max_retries}):", e)
        if retry < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Exiting.")
            exit()

soup = BeautifulSoup(response.content, "html.parser")
table = soup.find("table", id="main_table_countries_today")

rows = table.find_all("tr")

for row in rows[1:]:  # Skip the header row
    try:
        columns = row.find_all("td")
        no = columns[0].text.strip()
        country = columns[1].text.strip()
        total_cases = columns[2].text.strip()
        new_cases = columns[3].text.strip()
        total_deaths = columns[4].text.strip()
        new_deaths = columns[5].text.strip()
        total_recovered = columns[6].text.strip()
        new_recovered = columns[7].text.strip()
        active_cases = columns[8].text.strip()
        serious_critical = columns[9].text.strip()
        cases_per_million = columns[10].text.strip()
        deaths_per_million = columns[11].text.strip()
        total_tests = columns[12].text.strip()
        tests_per_million = columns[13].text.strip()
        population = columns[14].text.strip()

        covid_data.append({
            "N0": no,
            "country": country,
            "Total Cases": total_cases,
            "New Cases": new_cases,
            "Total Deaths": total_deaths,
            "New Deaths": new_deaths,
            "Total Recovered": total_recovered,
            "New Recovered": new_recovered,
            "Active Cases": active_cases,
            "Serious Critical": serious_critical,
            "Cases per 1M Population": cases_per_million,
            "Deaths per 1M Population": deaths_per_million,
            "Total Tests": total_tests,
            "Tests per 1M Population": tests_per_million,
            "Population": population
        })
    except Exception as e:
        print("Error in extracting COVID-19 data:", e)

df = pd.DataFrame(covid_data)
df.to_csv("worldometer_covid_stats.csv", index=False)

print("COVID-19 data from Worldometer successfully extracted and CSV saved.")
