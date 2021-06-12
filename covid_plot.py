import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import mplcursors
from TwitterBot import*

def covidcasesplot(result,d):
    res=result.lower()
    page=requests.get("https://www.worldometers.info/coronavirus/country/"+res+"/#graph-cases-daily")
    soup=BeautifulSoup(page.content, 'html.parser')
    a=soup.find(id="news_block")
    b=a.find_all(class_="newsdate_div")
    c=a.find_all(class_="date-btn")
    ydata=[]
    xdata=[]
    ydeath=[]

    for cases in b:
        sentence=list(cases.text.split(" "))
        final=sentence[0].replace('Updates\n\n', '')
        nums=int(final.replace(',', ''))
        deathfinal=int(sentence[4].replace(',', ''))
        ydata.append(nums)
        ydeath.append(deathfinal)
    ydata.reverse()
    ydeath.reverse()
    if d=="cases":
        print(ydata)
    else:
        print(ydeath)

    for dates in c:
        # print(dates)
        date=dates.text.strip()
        # print(date)
        xdata.append(date)
    xdata.reverse()
    print(xdata)

    fig, ax = plt.subplots()
    if d=='deaths':
        plt.plot(xdata,ydeath,marker = 'o')
    else:
        plt.plot(xdata, ydata, marker='o')
    plt.xlabel('Dates')
    plt.ylabel('Total no of '+ d)
    plt.tight_layout()
    ax.set_title("Covid new " + d + " in "+ res + " for last 6 days")
    mplcursors.cursor(hover=True)
    plt.savefig('images/'+res+'.jpg')
    upload_twitter = upload_media('images/' + res + '.jpg',"Covid new " + d + " in "+ res + " for last 6 days" )
    plt.show()
    return "0"






