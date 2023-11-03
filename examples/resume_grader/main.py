import openai
import os
from icecream import ic
import dotenv
import argparse

'''
roles: system, user, assistant
system - sets the behavior of the assistant
user - provides requests or comments for hte assistant to respond to
assistant - stores previous assistant responses
pip install openai, python-dotenv, icecream
'''

dotenv.load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

def engage_ai(job_data, resume_data):
    system_message = f"""
    You are an expert in analyzing resumes against job postings. You are able to explain why
    a candidate's resume does or does not meet expections for a job. 
    """

    user_message = f"""
    Given a candidate's resume and a new job posting. Would you hire the candidate for the job? 
    Please give the candidate a rating of 1 (highest) out of 10 (lowest) based on resume and job
    description match.  

    Candidate Resume:
    {resume_data}

    Job Posting:
    {job_data}
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

    ic(ans["choices"][0]["message"]["content"])

if __name__ == '__main__':

    description_text = '''
    This script accepts a resume and job description and will determine if 
    the resume is a good fit for the job. It will provide a grade from 1-10. 
    '''

    example_text = '''
    Examples:
    $ python main.py job_description.txt resume.txt   
    '''

    parser = argparse.ArgumentParser(description=description_text,
                                     epilog=example_text,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('job_description_file',
                        help='a file that contains the job description',
                        action='store',
                        default=None)

    parser.add_argument('resume_file',
                        help='a file that contains the resume of the candidate',
                        action='store',
                        default=None)

    args = parser.parse_args()
    ic(args)

    # load the resume
    with open(args.resume_file) as file:
        resume_data = file.read()
    
    # load the job description
    with open(args.job_description_file) as file:
        job_data = file.read()
 
    engage_ai(job_data, resume_data)