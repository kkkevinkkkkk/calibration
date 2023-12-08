from .template_criterion import CRITERION
from .template_examples import EXAMPLES
from .task_instructions import TASK_INSTRUCTIONS, DATASET_NAMES
from .template_func import fit_content
# template_chat_asqa_0 = '''<s>[INST] <<SYS>>
# You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
#
# You will be given an ambiguous factoid question which have different correct answers depneding on interpretation. Your answer should synthesize factual information from multiple sources into a long-form summary that resolves the ambiguity.
# <</SYS>>
#
# Question: {question} [/INST]'''
#
template_chat_asqa = '''<s>[INST] You will be given an ambiguous factoid question which have different correct answers depneding on interpretation. Your answer should synthesize factual information from multiple sources into a long-form summary that resolves the ambiguity. Provide a clear and concise answer with an unbiased tone.

Question: {question} [/INST]'''

template_task = '''<s>[INST] {task_instruction}

Question: {question} [/INST]'''


# template_chat_eli5 = '''<s>[INST] <<SYS>>
# You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
#
# If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
# <</SYS>>
#
# You will be given a question and you need to provide an answer which is comprehensible by five year olds. You will also have some web documents for reference. Provide a clear, engaging answer with a journalistic tone.
#
# Documents: {documents}
# Question: {question} [/INST]'''

template_chat_eli5_11_11 = '''<s>[INST] You will be given a question and you need to provide an answer which is comprehensible by five year olds. Provide a clear, engaging answer with a journalistic tone.

Question: {question} [/INST]'''
template_chat_eli5 = '''<s>[INST] You will be given a question and you need to provide an answer that's easy to understand. Keep it accurate, comprehensible and concise.

Question: {question} [/INST]'''

# template_chat_self_eval = '''<s>[INST] You will be given a question and your own answer to the question. Please evaluate the your own answer and provide a score from 0-100.
#
# Question: {question}
#
# Your answer: {answer}
#
# Now please provide your score about this answer in the format of "Correctness Score: <Your score>/100" and give your explanation. After that, provide your confidence about your evaluation in the format of "Confidence Score: <Your score>/100" and give your explanation.[/INST]
# '''
template_chat_self_eval = '''<s>[INST] You will be given a question and your own answer to the question. Please evaluate the your own answer and provide a score from 0-100.

Question: {question}

Your answer: {answer}

Now please provide your score about this answer in the format of "Correctness Score: <Your score>/100" and give your explanation. Assess for both factual accuracy and relevance to the question.[/INST]
'''
template_chat_self_verification = '''<s>[INST] You will be given a question and your own answer to the question. Please verify if the answer is correct.

Question: {question}

Your answer: {answer}

Now please determine whether the answer is true or false. Your response format should be "True/False"[/INST]
'''
template_chat_self_eval_examples = '''<s>[INST] You will be given a question and your own answer to the question. Please evaluate the your own answer and provide a score from 0-100.

{examples}

Now it's your turn.

Question: "{question}"

Your answer: "{answer}"

Now please provide your score about this answer in the format of "Correctness Score: <Your score>/100" and give your explanation. Assess for both factual accuracy and relevance to the question.[/INST]
'''
template_self_eval_five_pnt_asqa = '''<s>[INST] Please evaluate the student's answer to the question, and provide a score from 0-5 to the student's answer. Assess for both factual accuracy and relevance to the question. Following are the scoring criterion:

{criterion}

Question: {question}

Answer: {answer}

Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation. Assess for both factual accuracy and relevance to the question.[/INST]
'''

template_self_eval_five_pnt_examples_asqa = '''<s>[INST] Please evaluate the student's answer to the question, and provide a score from 0-5 to the student's answer. Assess for both factual accuracy and relevance to the question. Following are the scoring criterion:

{criterion}

Here are some examples.

{examples}

Now it's your turn.

Question: {question}

Answer: {answer}

Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation. Assess for both factual accuracy and relevance to the question.[/INST]
'''

template_self_eval_five_pnt_range_examples_asqa = '''<s>[INST] Please evaluate the student's answer to the question, and provide a score from 0-5 to the student's answer. Assess for both factual accuracy and relevance to the question. Following are the scoring criterion:

{criterion}

Here are some examples.

{examples}

Now it's your turn.

Question: {question}

Answer: {answer}

Now please provide your score range about this answer in the format of “Score: <score lower bound>-<score upper bound>/5” and give your explanation. Assess for both factual accuracy and relevance to the question.[/INST]
'''

template_self_eval_categorical_examples = '''<s>[INST] {task_instruction}

You will be given a question, and a student's answer. Please evaluate the student's answer, and provide a score from 0-5 to the student's answer based on the following scoring criterion:

{criterion}

Here are some examples.

{examples}

Now it's your turn.

Question: {question}

Answer: {answer}

Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation. Assess for both factual accuracy and relevance to the question.[/INST]
'''

template_self_eval_categorical = '''<s>[INST] {task_instruction}

You will be given a question, and a student's answer. Please evaluate the student's answer, and provide a score from 0-5 to the student's answer based on the following scoring criterion:

{criterion}

Question: {question}

Answer: {answer}

Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation. Assess for both factual accuracy and relevance to the question.[/INST]
'''


#
# template_self_eval_five_pnt_asqa = fit_content(template_self_eval_five_pnt_asqa, examples=EXAMPLES["asqa_eval_5"], criterion=CRITERION["asqa"])
# template_self_eval_five_pnt_examples_asqa = fit_content(template_self_eval_five_pnt_examples_asqa, examples=EXAMPLES["asqa_eval_5"], criterion=CRITERION["asqa"])
# template_self_eval_five_pnt_range_examples_asqa = fit_content(template_self_eval_five_pnt_range_examples_asqa, examples=EXAMPLES["asqa_eval_5"], criterion=CRITERION["asqa"])

template_chat_question_rephrase = '''<s>[INST] You will be given a question. Please rephrase the question to {rephrase_num} same questions and provide your rephrased questions in the format of
"Question 1: <Your rephrased question 1>
Question 2: <Your rephrased question 2>
Question 3: <Your rephrased question 3>
..."

Now given the original question, Please provide your rephrased questions.
Question: {question} [/INST]'''

template_chat_choose_entities_11_10 = '''<s>[INST] To validate the answer to "{question}", which {entity_num} named entities should you primarily check? Choose from options below.
1) Cardinal value
2) Date and times
3) Event name
4) Building name
5) Geo-political entity
6) Language name
7) Law name
8) Location name
9) Monetary value
10) Affiliation
11) Ordinal value
12) Organization name
13) Percentage
14) Person name
15) Product name
16) Quantity value
17) Time value
18) Work of art name [/INST]'''

template_chat_choose_entities = '''<s>[INST] To validate the answer to "{question}", which {entity_num} named entities should you primarily check? Choose from options below.
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
If you think Number is the most important, Location is the second important, Organization is the third, Event is the fourth, and Date_and_times is the last, then your answer should be "Number, Location, Organization, Event, Date_and_times" [/INST]'''

TEMPLATES_CHAT = {
    # "asqa": template_chat_asqa,
    # "eli5": template_chat_eli5,
    "self_eval": template_chat_self_eval,
    "self_verification": template_chat_self_verification,
    "self_eval_examples": template_chat_self_eval_examples,
    # "self_eval_five_pnt_asqa": template_self_eval_five_pnt_asqa,
    # "self_eval_five_pnt_examples_asqa": template_self_eval_five_pnt_examples_asqa,
    # "self_eval_five_pnt_range_examples_asqa": template_self_eval_five_pnt_range_examples_asqa,

    "question_rephrase": template_chat_question_rephrase,
    "choose_entities": template_chat_choose_entities,

}
for dataset_name in DATASET_NAMES:
    TEMPLATES_CHAT[dataset_name] = template_task.replace("{task_instruction}", TASK_INSTRUCTIONS[dataset_name])
    TEMPLATES_CHAT[f"self_eval_categorical_{dataset_name}"] = fit_content(template_self_eval_categorical,
                                                                       criterion=CRITERION[dataset_name],
                                                                       task_instruction=TASK_INSTRUCTIONS[f"{dataset_name}_eval"])

    TEMPLATES_CHAT[f"self_eval_categorical_examples_{dataset_name}"] = fit_content(template_self_eval_categorical_examples,
                                                                                examples=EXAMPLES[f"{dataset_name}_eval_categorical"],
                                                                                criterion=CRITERION[dataset_name],
                                                                                task_instruction=TASK_INSTRUCTIONS[f"{dataset_name}_eval"])
