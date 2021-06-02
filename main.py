import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import time
import threading
import sys

API_KEY= "tQdfPFM_soCT"
PROJECT_TOKEN= "tpHxwKtKdBaz"
RUN_TOKEN= "tptbVEDn9ozf"

class Data:
    def __init__(self,api_key,project_token,run_token):
        # print(run_token)
        self.api_key=api_key
        self.project_token=project_token
        self.run_token=run_token
        self.params={'api_key': self.api_key}
        self.data=self.get_data()

    def get_data(self):
        # rend_response = requests.get(f'https://parsehub.com/api/v2/runs/{self.run_token}', params=self.params)
        # print(self.run_token)# method,URL,header(authentication to access parsehub)
        # print(json.loads(rend_response.text))
        # sys.exit(1)
        response = requests.get(f'https://parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',
                                params=self.params)  # method,URL,header(authentication to access parsehub)
        data = json.loads(response.text)  # to convert the response data into jason format(key & Value)
        return data


    def total_cases(self):
        for datas in self.data['total']:
            if datas['name'] =='Coronavirus Cases:':
                return datas['value']
        return '0'

    def total_deaths(self):
        for datas in self.data['total']:
            if datas['name'] =='Deaths:':
                return datas['value']
        return '0'

    def total_recovered(self):
        for datas in self.data['total']:
            if datas['name'] =='Recovered:':
                return datas['value']
        return '0'

    def get_country(self,country):
        for datas in self.data['country']:
            if datas['name'].lower()==country.lower():
                print(datas)
                return datas
        return '0'

    def get_countryname(self):
        country_list=[]
        for datas in self.data['country']:
            country_list.append(datas['name'])
        return country_list

    def update_data(self):
        print("updating")
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run',
                                 params=self.params)
        # data = json.loads(response.text)
        # print(data)
        def poll():
            time.sleep(0.1)
            old_data = self.data
            # print(old_data)
            while True:
                new_data = self.get_data()
                # print(new_data)
                if new_data != old_data:
                    self.data = new_data
                    print("Data updated")
                    # main()
                    break
                # else:
                #     main()
                time.sleep(5)
        t = threading.Thread(target=poll)
        t.start()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    print(text)

# speak("how are you")
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:  # use the default microphone as the audio source
        audio = r.listen(source)  # listen for the first phrase and extract it into audio data
        said = ""
    try:
        said = r.recognize_google(audio)

    except LookupError:  # speech is unintelligible
        print("Could not understand audio")
    return said

def main():
    covid_data = Data(API_KEY, PROJECT_TOKEN, RUN_TOKEN)
    countries_list=covid_data.get_countryname()
    result="NONE"
    print("Listening....")
    END_TEXT="stop"
    UPDATE_COMMAND = "update"
    # print(END_TEXT)
    TOTAL_PATTERNS={re.compile("[\w\s]+ total [\w\s]+ cases"):covid_data.total_cases,
                    re.compile("[\w\s]+ total cases"): covid_data.total_cases,
                    re.compile("[\w\s]+ total [\w\s]+ deaths"):covid_data.total_deaths,
                    re.compile("[\w\s]+ total deaths"): covid_data.total_deaths,
                    re.compile("[\w\s]+ total [\w\s]+ recovered"): covid_data.total_recovered,
                    re.compile("[\w\s]+ total recovered"): covid_data.total_recovered
                   }

    COUNTRY_PATTERNS = {re.compile("[\w\s]+ total cases [\w\s]"): lambda country: covid_data.get_country(country)['total_no_of_cases'],
                        re.compile("[\w\s]+ total deaths [\w\s]"):lambda country: covid_data.get_country(country)['total_no_of_deaths'],
                        re.compile("[\w\s]+ total recovered [\w\s]"):lambda country: covid_data.get_country(country)['total_recovered']
                        }
    while True:
        text=get_audio()
        print(text)
        # print(UPDATE_COMMAND)

        for pattern,func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                # return

        for pattern,func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                sentence=list(text.split(" "))
                # print(sentence)
                for country in countries_list:
                    # print(country)
                    if country in sentence:
                        # print(country)
                        result=func(country)
                        print(result)
                        # print(result)
                        # break

        if result != "NONE":
            # print(text)
            speak(result)
            main()
            break

        if text == UPDATE_COMMAND:
            result = "Data is being updated. This may take a moment!"
            print(result)
            speak(result)
            covid_data.update_data()

        if text.find(END_TEXT):
            print("Stopped")
            break

print("Covid-19 recent data")
main()
