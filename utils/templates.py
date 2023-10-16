template_chat_asqa = '''<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

You will be given an ambiguous factoid question which have different correct answers depneding on interpretation. Your answer should synthesize factual information from multiple sources into a long-form summary that resolves the ambiguity.
<</SYS>>

Question: {question} [/INST]'''

template_chat_eli5 = '''<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
<</SYS>>

You will be given a question and you need to provide an answer which is comprehensible by five year olds. You will also have some web documents for reference

Documents: {documents}
Question: {question} [/INST]'''

template_chat_self_eval = '''<s>[INST] You will be given a question and your own answer to the question. Please evaluate the your own answer and provide a score from 0-100.

Question: {question}

Your answer: {answer}

Now please provide your score about this answer in the format of "Correctness Score: <Your score>/100" and give your explanation. After that, provide your confidence about your evaluation in the format of "Confidence Score: <Your score>/100" and give your explanation.[/INST]
'''

template_chat_question_rephrase = '''<s>[INST] You will be given a question. Please rephrase the question to {rephrase_num} same questions and provide your rephrased questions in the format of
"Question 1: <Your rephrased question 1>
Question 2: <Your rephrased question 2>
Question 3: <Your rephrased question 3>
..."

Now given the original question, Please provide your rephrased questions.
Question: {question} [/INST]'''


TEMPLATES_CHAT = {
    "asqa": template_chat_asqa,
    "eli5": template_chat_eli5,
    "self_eval": template_chat_self_eval,
    "question_rephrase": template_chat_question_rephrase}


template_openai_eval = '''{task_instruction}

{grader_instruction}

Question: {question}

Gold Answer: {gold_answer}

Student's answer: {answer}

Now please provide your score about this answer in the format of "Score: <Your score>/100" and give your explanation.
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
    "fact_eval": template_openai_fact_eval,
    "repetition": template_openai_repetition,
    "repetition_split": template_openai_repetition_split,
    "compare_questions": template_openai_compare_questions
}

TEMPLATES = {
    "chat": TEMPLATES_CHAT,
    "openai": TEMPLATES_OPENAI
}