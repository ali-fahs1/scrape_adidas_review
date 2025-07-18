from camoufox.sync_api import Camoufox
import json
import time
import asyncio
from rnet import Impersonate,Client,Proxy,Response
import pandas as pd

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
def create_client() -> Client:
    return Client(impersonate=Impersonate.Firefox136)

async def get_reviews(client,url):
    
    return await client.get(url)


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

    # Save to CSV
    df.to_csv('output.csv', index=True)









async def main() ->None:
    
    results=[]
    client=create_client()
    initial_page=await client.get(f'https://www.adidas.com/api/models/{model_number}/reviews?bazaarVoiceLocale=en_US&feature&includeLocales=en%2A&limit=5&offset=22&sort=newest')
    review_nb=json.loads(await initial_page.text())['totalResults']
    for i in range(0,review_nb,10):
        url=f'https://www.adidas.com/api/models/{model_number}/reviews?bazaarVoiceLocale=en_US&feature&includeLocales=en%2A&limit=10&offset={i}&sort=newest'
        reviews_resp=await get_reviews(client,url)
        reviews_data=json.loads(await reviews_resp.text())['reviews']
        for x in reviews_data:           
            userNickname.append(x['userNickname'])
            title.append(x['title'])
            formattedDate.append(x['formattedDate'])
            text.append(x['text'])
            isRecommended.append(x['isRecommended'])
            rating.append(x['rating'])
            badges.append(x['badges'])
            positiveFeedbackCount.append(x['positiveFeedbackCount'])
            negativeFeedbackCount.append(x['negativeFeedbackCount'])
    save_data_into_csv(userNickname,title,formattedDate,text,isRecommended,rating,badges,positiveFeedbackCount,negativeFeedbackCount)

        
if __name__=="__main__":
    with Camoufox() as browser:
        page = browser.new_page()
        page.goto("https://www.adidas.com/us/samba-og-shoes/JR8829.html")
        
        model_number=json.loads(page.locator('div#consent_blackbar+script+script').inner_text().replace("window.REACT_QUERY_DATA = ",''))['queries'][0]['state']['data']['model_number']
    print(f'done with camoufox with model_number{model_number}')

    asyncio.run(main())



end = time.perf_counter()
print(f"Script finished in {end - start:.2f} seconds")