from .template_func import fit_content
from .task_instructions import TASK_INSTRUCTIONS, DATASET_NAMES
from .template_criterion import CRITERION
from .template_examples import EXAMPLES

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

# template_openai_eval_5_11_11 = '''{task_instruction}
#
# You will be given a question, a reference answer, and a student's answer. Please evaluate the student's answer based on the reference answer, and provide a score from 0-5 to the student's answer. Assess for both factual accuracy and relevance to the question. Following are the scoring criterion:
#
# {criterion}
#
# Question: "{question}"
#
# Reference answer: "{reference_answer}"
#
# Student's answer: "{answer}"
#
# Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation.
# '''

# template_openai_eval_5_examples_11_4 = '''{task_instruction}
#
# You will be given a question, a reference answer, and a student's answer. Please evaluate the student's answer based on the reference answer, and provide a score from 0-5 to the student's answer. Assess for both factual accuracy and relevance to the question. Following is the scoring criteria:
#
# 5 - Completely Correct and Highly Relevant: The answer fully addresses the question, resolves the ambiguity, and provides a well-rounded resolution. All facts presented in the answer are accurate and relevant.
# 4 - Mostly Correct and Relevant: The answer is very relevant and addresses the ambiguity well, but might have a minor oversight or inaccuracy. Almost all the facts presented are accurate, with only minor errors.
# 3 - Partially Correct and Relevant: The answer is generally on topic and attempts to address the ambiguity, but there might be minor inaccuracies or omissions. The majority of the facts are correct, with only a few minor errors.
# 2 - Somewhat Relevant but Flawed: The answer somewhat addresses the topic but does not fully explore the question's ambiguity or does not provide a complete resolution. The facts presented are a mix of correct and incorrect information, with about half being accurate.
# 1 - Mostly Irrelevant or Incorrect: The answer slightly touches upon the topic but misses the main point. The majority of the facts presented are incorrect, with only a small portion being accurate.
# 0 - Completely Irrelevant or Incorrect: The student's answer is completely off-topic, not related to the question at all, or contains only incorrect information.
#
# Here are some examples.
#
# {examples}
#
# Now it's your turn.
#
# Question: "{question}"
#
# Reference answer: "{reference_answer}"
#
# Student's answer: "{answer}"
#
# Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation.
# '''

# template_openai_eval_5_examples_11_11 = '''{task_instruction}
#
# You will be given a question, a reference answer, and a student's answer. Please evaluate the student's answer based on the reference answer, and provide a score from 0-5 to the student's answer. Assess for both factual accuracy and relevance to the question. Following are the scoring criterion:
#
# {criterion}
#
# Here are some examples.
#
# {examples}
#
# Now it's your turn.
#
# Question: "{question}"
#
# Reference answer: "{reference_answer}"
#
# Student's answer: "{answer}"
#
# Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation.
# '''
# template_openai_eval_5 = '''{task_instruction}
#
# You will be given a question, a reference answer, and a student's answer. Please evaluate the student's answer based on both your knowledge and the reference answer, and provide a score from 0-5 to the student's answer. Keep in mind that the reference answer is not the sole correct response. Assess for both factual accuracy and relevance to the question. Following are the scoring criterion:
#
# {criterion}
#
# Question: "{question}"
#
# Reference answer: "{reference_answer}"
#
# Student's answer: "{answer}"
#
# Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation.
# '''
#
# template_openai_eval_5_examples = '''{task_instruction}
#
# You will be given a question, a reference answer, and a student's answer. Please evaluate the student's answer based on both your knowledge and the reference answer, and provide a score from 0-5 to the student's answer. Keep in mind that the reference answer is not the sole correct response. Assess for both factual accuracy and relevance to the question. Following are the scoring criterion:
#
# {criterion}
#
# Here are some examples.
#
# {examples}
#
# Now it's your turn.
#
# Question: "{question}"
#
# Reference answer: "{reference_answer}"
#
# Student's answer: "{answer}"
#
# Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation.
# '''

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

Verify if the response contains a statement resembling the target sentence. Answer yes or no.
'''

TEMPLATES_OPENAI = {
    "eval": template_openai_eval,
    # "eval_5": template_openai_eval_5,
    # "eval_5_with_examples": template_openai_eval_5_examples,
    "eval_with_examples": template_openai_eval_examples,
    "fact_eval": template_openai_fact_eval,
    "repetition": template_openai_repetition,
    "repetition_split": template_openai_repetition_split,
    "compare_questions": template_openai_compare_questions
}
for dataset_name in DATASET_NAMES:
    TEMPLATES_OPENAI[f"eval_categorical_{dataset_name}"] = fit_content(template_eval_categorical,
                                                                       task_instruction=TASK_INSTRUCTIONS[f"{dataset_name}_eval"],
                                                                       criterion=CRITERION[dataset_name])
    TEMPLATES_OPENAI[f"eval_categorical_examples_{dataset_name}"] = fit_content(template_eval_categorical_examples,
                                                                                task_instruction=TASK_INSTRUCTIONS[f"{dataset_name}_eval"],
                                                                                criterion=CRITERION[dataset_name],
                                                                                examples=EXAMPLES[f"{dataset_name}_eval_categorical"])