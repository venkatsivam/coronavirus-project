import requests
import json
import pyttsx3
import speech_recognition as sr
import re

API_KEY= "tQdfPFM_soCT"
PROJECT_TOKEN= "tpHxwKtKdBaz"
RUN_TOKEN= "tJy-T4JYWDcZ"

class Data:
    def __init__(self,api_key,project_token):
        self.api_key=api_key
        self.project_token=project_token
        self.params={'api_key': self.api_key}
        self.data=self.get_data()

    def get_data(self):
        response = requests.get(f'https://parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',
                                params=self.params)  # method,URL,header(authentication to access parsehub)
        data = json.loads(response.text)  # to convert the response data into jason format(key & Value)
        return data
        # print(data)

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
            if datas['name']==country:
                # print(datas)
                return datas
        return '0'

    def get_countryname(self):
        country_list=[]
        for datas in self.data['country']:
            country_list.append(datas['name'])
        return country_list

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
# print(get_audio())

def main():
    covid_data = Data(API_KEY, PROJECT_TOKEN)
    countryList=covid_data.get_countryname()
    result="NONE"
    print("Listening....")
    END_TEXT="stop"
    # print(END_TEXT)
    TOTAL_PATTERNS={re.compile("[\w\s]+ total [\w\s]+ cases"):covid_data.total_cases,
                    re.compile("[\w\s]+ total cases"): covid_data.total_cases,
                    re.compile("[\w\s]+ total [\w\s]+ deaths"):covid_data.total_deaths,
                    re.compile("[\w\s]+ total deaths"): covid_data.total_deaths,
                    re.compile("[\w\s]+ total [\w\s]+ recovered"): covid_data.total_recovered,
                    re.compile("[\w\s]+ total recovered"): covid_data.total_recovered
                   }

    COUNTRY_PATTERNS = {re.compile("[\w\s]+ cases [\w\s]"): lambda country:covid_data.get_country(country)['total_no_of_cases'],
                        re.compile("[\w\s]+ deaths [\w\s]"):lambda country: covid_data.get_country(country)['total_no_of_deaths'],
                        re.compile("[\w\s]+ recovered [\w\s]"):lambda country: covid_data.get_country(country)['total_recovered']
                        }
    while True:
        text=get_audio()
        # print(text)
        # print(END_TEXT)

        for pattern,func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                # return

        for pattern,func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                sentence=list(text.split(" "))
                # print(sentence)
                for country in countryList:
                    # print(country)
                    if country in sentence:
                        # print(country)
                        result=func(country)
                        # print(result)
                        break

        if result != "NONE":
            print(text)
            speak(result)
            main()
            break

        if text.find(END_TEXT):
            print("Stopped")
            break

print("Covid-19 recent data")
main()
