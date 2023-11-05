from .template_criterion import asqa_criterion
from .template_examples import EXAMPLES
template_chat_asqa_0 = '''<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

You will be given an ambiguous factoid question which have different correct answers depneding on interpretation. Your answer should synthesize factual information from multiple sources into a long-form summary that resolves the ambiguity.
<</SYS>>

Question: {question} [/INST]'''

template_chat_asqa = '''<s>[INST] You will be given an ambiguous factoid question which have different correct answers depneding on interpretation. Your answer should synthesize factual information from multiple sources into a long-form summary that resolves the ambiguity. Provide a clear and concise answer with an unbiased tone.

Question: {question} [/INST]'''

template_chat_eli5 = '''<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
<</SYS>>

You will be given a question and you need to provide an answer which is comprehensible by five year olds. You will also have some web documents for reference. Provide a clear, engaging answer with a journalistic tone.

Documents: {documents}
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

Question: {question}

Answer: {answer}

Now please provide your score about this answer in the format of "Score: <Your score>/5" and give your explanation. Assess for both factual accuracy and relevance to the question.[/INST]
'''

template_self_eval_five_pnt_range_examples_asqa = '''<s>[INST] Please evaluate the student's answer to the question, and provide a score from 0-5 to the student's answer. Assess for both factual accuracy and relevance to the question. Following are the scoring criterion:

{criterion}

Here are some examples.

{examples}

Question: {question}

Answer: {answer}

Now please provide your score range about this answer in the format of “Score: <score lower bound>-<score upper bound>/5” and give your explanation. Assess for both factual accuracy and relevance to the question.[/INST]
'''


def fit_content(template, examples=None, criterion=None):
    if examples:
        template = template.replace("{examples}", examples)
    if criterion:
        template = template.replace("{criterion}", criterion)
    return template

template_self_eval_five_pnt_asqa = fit_content(template_self_eval_five_pnt_asqa, examples=EXAMPLES["asqa_eval_5"], criterion=asqa_criterion)
template_self_eval_five_pnt_examples_asqa = fit_content(template_self_eval_five_pnt_examples_asqa, examples=EXAMPLES["asqa_eval_5"], criterion=asqa_criterion)
template_self_eval_five_pnt_range_examples_asqa = fit_content(template_self_eval_five_pnt_range_examples_asqa, examples=EXAMPLES["asqa_eval_5"], criterion=asqa_criterion)

template_chat_question_rephrase = '''<s>[INST] You will be given a question. Please rephrase the question to {rephrase_num} same questions and provide your rephrased questions in the format of
"Question 1: <Your rephrased question 1>
Question 2: <Your rephrased question 2>
Question 3: <Your rephrased question 3>
..."

Now given the original question, Please provide your rephrased questions.
Question: {question} [/INST]'''

template_chat_choose_entities = '''<s>[INST] To validate the answer to "{question}", which {entity_num} named entities should you primarily check? Choose from options below.
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

TEMPLATES_CHAT = {
    "asqa": template_chat_asqa,
    "eli5": template_chat_eli5,

    "self_eval": template_chat_self_eval,
    "self_eval_examples": template_chat_self_eval_examples,
    "self_eval_five_pnt_asqa": template_self_eval_five_pnt_asqa,
    "self_eval_five_pnt_examples_asqa": template_self_eval_five_pnt_examples_asqa,
    "self_eval_five_pnt_range_examples_asqa": template_self_eval_five_pnt_range_examples_asqa,

    "question_rephrase": template_chat_question_rephrase,
    "choose_entities": template_chat_choose_entities,

}