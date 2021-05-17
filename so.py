import argparse
import requests
import html

parser = argparse.ArgumentParser()
parser.add_argument('question_number', type=int)
parser.add_argument('label', type=str)
args = parser.parse_args()

session = requests.Session()

URL = 'https://api.stackexchange.com/2.2/questions'


class QuotaOverflow(Exception):
    pass	
    
    
def get_pagesizes_range(number):
    result = []
    for _ in range(number // 100):
        result.append(100)
    if number % 100 != 0:
        result.append(number % 100)
    return result
    
    
def top_questions(number, label):
    pagesizes = get_pagesizes_range(number)
    try:
        top_ques = []
        for page, pagesize in enumerate(pagesizes, 1):
    	    params = {"page": page, "pagesize": pagesize,
    	              "order": "desc", "sort": "votes",
    	              "tagged": label, "site": "stackoverflow"}
    	    resp = session.get(URL, params=params).json()["items"]
    	    for item in resp:
    	    	title = html.unescape(item["title"])
    	    	question_id = item['question_id']
    	    	top_ques.append((title, question_id))
        return top_ques
    except Exception:
    	raise QuotaOverflow("only make 300 requests per day")
    	
    	
def top_answer(question_id):
    link = f'{URL}/{question_id}/answers'
    params = {"pagesize": 1, "order": "desc",	
              "sort": "votes", "site": "stackoverflow"}
    try:
    	resp = session.get(link, params=params).json()["items"]
    	answer = resp[0]['answer_id']
    	return answer
    except Exception:
    	raise QuotaOverflow("only make 300 requests per day")
    	
    	
def main():
    label = args.label
    question_number = args.question_number
    print(f'Top {question_number} questions with tag {label}')
    
    if question_number >= 300:
    	print("only make 300 requests per day")
    	return
    	
    questions = top_questions(question_number, label)
    for title, question_id in questions:
    	answer_id = top_answer(question_id)
    	link_to_answer = f'https://stackoverflow.com/a/{answer_id}'
    	print(title, ",answer:", link_to_answer)
    	
if __name__ == "__main__":
    main()	
   	
