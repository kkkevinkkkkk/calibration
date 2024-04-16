template_eval_categorical = '''{task_instruction}

You will be given a question, a reference answer, and a student's answer. Please evaluate the student's answer based on both your knowledge and the reference answer, and provide a score from 0-5 to the student's answer. Keep in mind that the reference answer is not the sole correct response. Assess for both factual accuracy and relevance to the question. Following are the scoring criterion:

{criterion}

Question: "{question}"

Reference answer: "{reference_answer}"

Student's answer: "{answer}"

Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation.
'''

template_eval_categorical_examples = '''{task_instruction}

You will be given a question, a reference answer, and a student's answer. Please evaluate the student's answer based on both your knowledge and the reference answer, and provide a score from 0-5 to the student's answer. Keep in mind that the reference answer is not the sole correct response. Assess for both factual accuracy and relevance to the question. Following are the scoring criterion:

{criterion}

Here are some examples.

{examples}

Now it's your turn.

Question: "{question}"

Reference answer: "{reference_answer}"

Student's answer: "{answer}"

Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation.
'''


template_compare_questions = '''Determine if the following two questions have the same meaning.
Question 1: "{question1}"
Question 2: "{question2}"
Think about it carefully. Answer yes or no and then justify your answer
'''


template_repetition = '''You will be presented with a question followed by two answers. Evaluate how similar these answers are, considering their amount of information provided, factual content, effectiveness in addressing the question, format and organization. Conclude by providing an integer similarity score between 0 and 5.

Question: {question}

Answer 1: "{answer1}"

Answer 2: "{answer2}"

Now please give your similarity score in the format of "Similarity score: <Your score>/5" and give your explanation. Make your answer short and concise.
'''

template_repetition_split = '''You will receive a sentence and a response; please ascertain if a similar statement is present in the response.

Sentence: "{sentence}"

Response: "{response}"

Verify if the response contains a statement resembling the target sentence. Answer yes or no.
'''


template_self_eval_categorical_examples = '''{task_instruction}

You will be given a question, and a student's answer. Please evaluate the student's answer, and provide a score from 0-5 to the student's answer based on the following scoring criterion:

{criterion}

Here are some examples.

{examples}

Now it's your turn.

Question: {question}

Answer: {answer}

Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation. Assess for both factual accuracy and relevance to the question.
'''

template_self_eval_categorical_examples_vicuna = '''{task_instruction}

You will be given a question, and a student's answer. Please evaluate the student's answer, and provide a score from 0-5 to the student's answer based on the following scoring criterion:

{criterion}

Here are some examples.

{examples}

Question: {question}

Answer: {answer}

Comment:'''

template_self_eval_categorical_examples_doc = '''{task_instruction}

You will be given a question, relevant documents for reference, and a student's answer. Please evaluate the student's answer, and provide a score from 0-5 to the student's answer based on the following scoring criterion:

{criterion}

Here are some examples.

{examples}

Now it's your turn.

Question: {question}

Documents: {documents}

Answer: {answer}

Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation. Assess for both factual accuracy and relevance to the question.
'''

template_self_eval_categorical = '''{task_instruction}

You will be given a question, and a student's answer. Please evaluate the student's answer, and provide a score from 0-5 to the student's answer based on the following scoring criterion:

{criterion}

Question: {question}

Answer: {answer}

Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation. Assess for both factual accuracy and relevance to the question.
'''


template_self_eval_range = '''Please evaluate the student's answer to the question, and provide a score from 0-5 to the student's answer. Assess for both factual accuracy and relevance to the question. Following are the scoring criterion:

{criterion}

Here are some examples.

{examples}

Now it's your turn.

Question: {question}

Answer: {answer}

Now please provide your score range about this answer in the format of “Score: <score lower bound>-<score upper bound>/5” and give your explanation. Assess for both factual accuracy and relevance to the question.
'''


template_question_rephrase = '''You will be given a question. Please rephrase the question to {rephrase_num} same questions and provide your rephrased questions in the format of
"Question 1: <Your rephrased question 1>
Question 2: <Your rephrased question 2>
Question 3: <Your rephrased question 3>
..."

Now given the original question, Please provide your rephrased questions.
Question: {question}'''


template_choose_entities = '''To validate the answer to "{question}", which {entity_num} named entities should you primarily check? Choose from options below.
1) Number: This category includes all entities that represent numerical information, such as cardinal numbers, ordinal numbers, percentages, and monetary values.
2) Date_and_times: This category includes all entities that are time-related, such as dates and times.
3) Location: This category includes all entities that are location-related, such as countries, cities, buildings and other geographical locations. 
4) Person: This category includes all entities that are person-related, such as names of people.
5) Organization: This category includes all entities that are organization-related, such as names of organizations, affiliations.
6) Event: This category includes all entities that are event-related.
7) Language: This category includes all entities that are language-related.
8) Law: This category includes all entities that are law-related.
9) Product: This category includes all entities that are product-related.
10) Work_of_art: This category includes all entities that are work of art-related. 
Choose the top 5 important entities from the options above. 
If you think Number is the most important, Location is the second important, Organization is the third, Event is the fourth, and Date_and_times is the last, then your answer should be "Number, Location, Organization, Event, Date_and_times"'''

template_self_eval_summ = '''You will be given one summary written for a news article.

Your task is to rate the overall quality of the summary with a score from 0 to 5, where 0 is the lowest and 5 is the highest.

Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.

Evaluation Steps:
1. Read the news article carefully and identify the main topic and key points.
2. Read the summary and compare it to the news article. Check if the summary covers the main topic and key points of the news article, and if it presents them in a clear and logical order.
3. Assign a score for the summary quality on a scale of 0 to 5, where 0 is the lowest and 5 is the highest.

Here are some examples.

{examples}

Now it's your turn.

Task Input:
Article:
{article}

Summary:
{summary}

Now please provide your score of the summary in the format of "Score: <Your score>/5" and give your explanation.
'''  # following the template in G-Eval (https://arxiv.org/pdf/2303.16634.pdf)
template_self_eval_summ_vicuna = '''You will be given one summary written for a news article.

Your task is to rate the overall quality of the summary with a score from 0 to 5, where 0 is the lowest and 5 is the highest.

Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.

Evaluation Steps:
1. Read the news article carefully and identify the main topic and key points.
2. Read the summary and compare it to the news article. Check if the summary covers the main topic and key points of the news article, and if it presents them in a clear and logical order.
3. Assign a score for the summary quality on a scale of 0 to 5, where 0 is the lowest and 5 is the highest.

Here are some examples.

{examples}


Article:
{article}

Summary:
{summary}

Comment:'''  # following the template in G-Eval (https://arxiv.org/pdf/2303.16634.pdf)

template_eval_summ = '''You will be given one summary written for a news article.

Your task is to rate the overall quality of the summary with a score from 0 to 5, where 0 is the lowest and 5 is the highest.

Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.

Evaluation Steps:
1. Read the news article carefully and identify the main topic and key points.
2. Read the summary and compare it to the news article. Check if the summary covers the main topic and key points of the news article, and if it presents them in a clear and logical order.
3. Assign a score for the summary quality on a scale of 0 to 5, where 0 is the lowest and 5 is the highest.

Task Input:
Article:
{article}

Summary:
{summary}

Now please provide your score of the summary in the format of "Score: <Your score>/5" and give your explanation.
'''  # following the template in G-Eval (https://arxiv.org/pdf/2303.16634.pdf)
template_self_verification = ''''You will be given a question and your own answer to the question. Please verify if the answer is correct or not.

Question: {question}

Answer: {answer}

Now please determine whether the answer is true or false. Return "True" if the answer is correct, and "False" if the answer is incorrect.'''

template_self_verification_examples = '''You will be given a question and your own answer to the question. Please verify if the answer is correct or not.

Here are some examples.

{examples}

Now please determine whether the answer is true or false. Return "True" if the answer is correct, and "False" if the answer is incorrect.


Question: {question}

Answer: {answer}

Correctness:'''

template_self_verification_summ = ''''You will be given a document and your own summary. Please verify if the summary is correct or not.

Document: {doc}

Summary: {summary}

Now please determine whether the summary is true or false. Return "True" if the summary is correct, and "False" if the summary is incorrect.'''


template_self_verification_examples_summ = '''You will be given a document and your own summary. Please verify if the summary is correct or not.

Here are some examples.

{examples}

Now please determine whether the summary is true or false. Return "True" if the summary is correct, and "False" if the summary is incorrect.

Document: {doc}

Summary: {summary}

Correctness:'''


TEMPLATE_LLAMA2_CHAT = '''<s>[INST] {task_instruction} [/INST]'''
TEMPLATES = {
    "eval_categorical": template_eval_categorical,
    "eval_categorical_examples": template_eval_categorical_examples,
    "compare_questions": template_compare_questions,
    "question_rephrase": template_question_rephrase,
    "repetition": template_repetition,
    "repetition_split": template_repetition_split,
    "self_eval_categorical_examples": template_self_eval_categorical_examples,
    "self_eval_categorical_examples_vicuna": template_self_eval_categorical_examples_vicuna,
    "self_eval_categorical_examples_doc": template_self_eval_categorical_examples_doc,
    "self_eval_categorical": template_self_eval_categorical,
    "self_eval_range": template_self_eval_range,
    "choose_entities": template_choose_entities,
    "llama2_chat": TEMPLATE_LLAMA2_CHAT,
    "eval_summ": template_eval_summ,
    "self_eval_summ_vicuna": template_self_eval_summ_vicuna,
    "self_eval_summ": template_self_eval_summ,
    "self_verification": template_self_verification,
    "self_verification_examples": template_self_verification_examples,
    "self_verification_summ": template_self_verification_summ,
    "self_verification_examples_summ": template_self_verification_examples_summ,
}
