import praw
import os
import dotenv
import openai
import time
from icecream import ic

dotenv.load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

def reddit_search(praw_obj, subreddits):
    all_text = []
    for subreddit in subreddits:
        time.sleep(1)
        ic(subreddit)

        # top post for the week limited to just 1
        for post in praw_obj.subreddit(subreddit).top(limit=1, time_filter='week'):
            title = post.title
            all_text.append(title)
    
            # controls the "Morecomments" object to load more comments than was done by default
            # this parameter can be None to load all comments 
            post.comments.replace_more(limit=3)
            comments_array = post.comments[:2]
            for comment in comments_array:
                body = comment.body
                ic(subreddit, title)
                ic(body)
                all_text.append(body)

    return ' '.join(all_text)

def engage_ai(reddit_data):
    system_message = f"""
    You are an expert at reading reddit posts and understanding crypto currency trends and topics. 
    """

    user_message = f"""
    Analyze the following Reddit threads and identify which cryptocurrencies are mentioned the most 
    frequently. Provide a summary of the top cryptocurrencies discussed, along with the context or 
    sentiment of the discussion where possible. 

    Here are the threads:
    {reddit_data}
    """

    messages=[
        {"role": "system", "content": f"{system_message}"},
        {"role": "user", "content": f"{user_message}"},
        ]

    ic(f"calling openai with prompt: {user_message}")
    ans = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=2048,
        messages=messages,
    )

    res = ans["choices"][0]["message"]["content"]
    ic(res)

    return res

if __name__ == "__main__":
    # Set up your credentials
    client_id = os.environ.get("CLIENT_ID") 
    client_secret = os.environ.get("CLIENT_SECRET") 
    user_agent = os.environ.get("APP_NAME") 

    # Initialize praw instance
    praw_obj = praw.Reddit(
        client_id=client_id, 
        client_secret=client_secret, 
        user_agent=user_agent
        )

    # Define subreddits
    subreddits = [
        'CryptoCurrency',
        'Bitcoin',
        'ethereum',
        'CryptoMarkets',
        'CryptoMoonShots'
        ]

    ic(f"searching {subreddits}")

    # get data from reddit
    response = reddit_search(praw_obj, subreddits)
    ic(len(response))
    
    # send to the AI
    chatgpt_res = engage_ai(response)
    ic(chatgpt_res)
