template_openai_eval = '''{task_instruction}

You will be given a question, a reference answer, and a student's answer. Please evaluate the student's answer based on the reference answer, and provide a score from 0-100 to the student's answer. Assess for both factual accuracy and relevance to the question.

Question: "{question}"

Reference answer: "{reference_answer}"

Student's answer: "{answer}"

Now please provide your score about this answer in the format of "Score: <Your score>/100" and give your explanation.
'''

template_openai_eval_examples = '''{task_instruction}

You will be given a question, a reference answer, and a student's answer. Please evaluate the student's answer based on the reference answer, and provide a score from 0-100 to the student's answer. Assess for both factual accuracy and relevance to the question.

{examples}

Now it's your turn.

Question: "{question}"

Reference answer: "{reference_answer}"

Student's answer: "{answer}"

Please provide your score about this answer in the format of "Score: <Your score>/100" and give your explanation.
'''

template_openai_fact_eval = '''You will be given a student's answer and please evaluate the answer for its factuality.

Student's answer: {answer}

Now please provide your score about this answer in the format of "Score: <Your score>/100" and give your explanation.
'''


template_openai_compare_questions = '''Determine if the following two questions have the same meaning.
Question 1: "{question1}"
Question 2: "{question2}"
Think about it carefully. Answer yes or no and then justify your answer
'''

# template_openai_repetition = '''You will be given a question and two answers to that question. Please evaluate the similarity between the two answers and give a similarity score from 0-5.
#
# Question: {question}
#
# Answer 1: "{answer1}"
#
# Answer 2: "{answer2}"
#
# Now please give your similarity score in the format of "Similarity score: <Your score>/5" and give your explanation. Make your answer short and concise.
# '''

template_openai_repetition = '''You will be presented with a question followed by two answers. Evaluate how similar these answers are, considering their amount of information provided, factual content, effectiveness in addressing the question, format and organization. Conclude by providing a similarity score between 0 and 5.

Question: {question}

Answer 1: "{answer1}"

Answer 2: "{answer2}"

Now please give your similarity score in the format of "Similarity score: <Your score>/5" and give your explanation. Make your answer short and concise.
'''

template_openai_repetition_split = '''You will receive a sentence and a response; please ascertain if a similar statement is present in the response.

Sentence: "{sentence}"

Response: "{response}"

Answer yes or no.
'''

TEMPLATES_OPENAI = {
    "eval": template_openai_eval,
    "eval_with_examples": template_openai_eval_examples,
    "fact_eval": template_openai_fact_eval,
    "repetition": template_openai_repetition,
    "repetition_split": template_openai_repetition_split,
    "compare_questions": template_openai_compare_questions
}