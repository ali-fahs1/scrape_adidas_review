import json
import time
import asyncio
from rnet import Impersonate,BlockingClient
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

userNickname=[]
title=[]
formattedDate=[]
text=[]
isRecommended=[]
rating=[]
badges=[]
positiveFeedbackCount=[]
negativeFeedbackCount=[]

start =time.perf_counter()
def create_client():
    return BlockingClient(impersonate=Impersonate.Firefox136)

def get_reviews(client,url):
    
    return  client.get(url)


def save_data_into_csv(userNickname,title,formattedDate,text,isRecommended,rating,badges,positiveFeedbackCount,negativeFeedbackCount):


    # Create DataFrame from dict where keys become column names
    df = pd.DataFrame({
        'userNickname': userNickname,
        'title': title,
        'formattedDate': formattedDate,
        'text': text,
        'isRecommended': isRecommended,
        'rating': rating,
        'badges': badges,
        'positiveFeedbackCount': positiveFeedbackCount,
        'negativeFeedbackCount':negativeFeedbackCount,

    })


    # Setup Google Sheets credentials
    # scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    # client = gspread.authorize(creds)

    # sheet = client.open("adidas_review").sheet1  # or .worksheet("Sheet1")

    # # Write DataFrame to sheet
    # sheet.clear()  # optional: clear existing data
    # set_with_dataframe(sheet, df)


    # Save to CSV

    df.to_csv('output.csv', index=True)
    return 'done !!'

def main():
    model_number='NKI96'
    
    results=[]
    client=create_client()
    initial_page= client.get(f'https://www.adidas.com/api/models/{model_number}/reviews?bazaarVoiceLocale=en_US&feature&includeLocales=en%2A&limit=5&offset=22&sort=newest')
    review_nb=json.loads( initial_page.text())['totalResults']
    for i in range(0,review_nb,10):
        print(i)
        url=f'https://www.adidas.com/api/models/{model_number}/reviews?bazaarVoiceLocale=en_US&feature&includeLocales=en%2A&limit=10&offset={i}&sort=newest'
        reviews_resp= get_reviews(client,url)
        reviews_data=json.loads( reviews_resp.text())['reviews']
        for x in reviews_data:   
            userNickname.append(str(x['userNickname']).strip().replace('\n', ' ').replace('\r', ' '))
            title.append(str(x['title']).strip().replace('\n', ' ').replace('\r', ' '))
            formattedDate.append(str(x['formattedDate']).strip().replace('\n', ' ').replace('\r', ' '))
            text.append(str(x['text']).strip().replace('\n', ' ').replace('\r', ' '))
            isRecommended.append(str(x['isRecommended']).strip().replace('\n', ' ').replace('\r', ' '))
            rating.append(str(x['rating']).strip().replace('\n', ' ').replace('\r', ' '))
            badges.append(str(x['badges']).strip().replace('\n', ' ').replace('\r', ' '))
            positiveFeedbackCount.append(str(x['positiveFeedbackCount']).strip().replace('\n', ' ').replace('\r', ' '))
            negativeFeedbackCount.append(str(x['negativeFeedbackCount']).strip().replace('\n', ' ').replace('\r', ' '))
    save_data_into_csv(userNickname,title,formattedDate,text,isRecommended,rating,badges,positiveFeedbackCount,negativeFeedbackCount)

main()

end = time.perf_counter()
print(f"Script finished in {end - start:.2f} seconds")


# https://adidas-review-872349921472.africa-south1.run.app