template_vicuna_self_eval = '''You will be given a question and your own answer to the question. Please evaluate the your own answer and provide a score from 0-100.

Question: {question}

Your answer: {answer}

Now please provide your score about this answer in the format of "Correctness Score: <Your score>/100" and give your explanation. After that, provide your confidence about your evaluation in the format of "Confidence Score: <Your score>/100" and give your explanation.
'''
template_vicuna_question_rephrase = '''You will be given a question. Please rephrase the question to {rephrase_num} same questions and provide your rephrased questions in the format of
"Question 1: <Your rephrased question 1>
Question 2: <Your rephrased question 2>
Question 3: <Your rephrased question 3>
..."

Now given the original question, Please provide your rephrased questions.
Question: {question}'''


TEMPLATES_VICUNA = {
    "self_eval": template_vicuna_self_eval,
    "question_rephrase": template_vicuna_question_rephrase,
}