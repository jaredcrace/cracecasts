import requests
import dotenv
import os
from icecream import ic

from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

dotenv.load_dotenv()

def engage_ai(review_data):
    user_message = f"""
    Which of the mechanics has the best reviews and why do you think that? You must make a choice
    and choose one mechanic and provide reasoning behind it. 
    """

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    qa_chain = load_qa_chain(llm, chain_type="map_reduce")
    qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)
    ans = qa_document_chain.run(
        input_document=review_data, 
        question=user_message)
    return ans

def search_places(google_api_key, location, radius, keyword):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&keyword={keyword}&key={google_api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return "Error in fetching places"
    return response.json()

def get_place_details(place_id, google_api_key):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,rating,review&key={google_api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return "Error in fetching place details"
    return response.json()


if __name__ == "__main__":
    google_api_key = os.environ.get("GOOGLE_API_KEY") 

    # Houston TX
    location = '29.841264, -95.473202'

    # about 5 miles
    radius = 8000 
    keyword = 'car mechanic'

    # Search for car mechanics
    places_result = search_places(google_api_key, location, radius, keyword)

    # Iterate over places and fetch reviews
    place_ids = []
    all_text = []
    all_places = places_result.get("results")

    # read 10 different car mechanics 
    for index in range(10):
        place_id = all_places[index]["place_id"]
        details = get_place_details(place_id, google_api_key)
        busienss_name = details["result"]["name"]

        # make sure this has reviews
        if 'reviews' not in details['result'].keys():
            continue

        review_count = len(details['result']['reviews'])
        if review_count < 5:
            continue

        for review in details['result']['reviews']:
            review_text = review["text"]
            name_and_review = f"Mechanic Name: {busienss_name}\n Review: \n{review_text}\n"
            all_text.append(name_and_review)
        place_ids.append(place_id)

    all_reviews = ' '.join(all_text)

    ic(place_ids)
    ic(all_reviews)


    ans = engage_ai(all_reviews)
    ic(ans)

