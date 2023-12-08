asqa_criterion = '''5 - Completely Correct and Highly Relevant: The answer fully addresses the question, resolves the ambiguity, and provides a well-rounded resolution. All facts presented in the answer are accurate and relevant.
4 - Mostly Correct and Relevant: The answer is very relevant and addresses the ambiguity well, but might have a minor oversight or inaccuracy. All the facts presented are accurate and relevant, or with only minor errors.
3 - Partially Correct and Relevant: The answer is generally on topic and attempts to address the ambiguity, but there might be inaccuracies or omissions. The majority of the facts are correct, with a few errors.
2 - Flawed but Somewhat Relevant: The answer somewhat addresses the topic but does not fully explore the question's ambiguity or does not provide a complete resolution. The facts presented are a mix of correct and incorrect information, with about half being accurate.
1 - Mostly Incorrect or Mostly Irrelevant: The answer slightly touches upon the topic but misses the main point. The majority of the facts presented are incorrect, with only a small portion being accurate.
0 - Completely Incorrect or Completely Irrelevant: The student's answer is completely off-topic, not related to the question at all, or contains only incorrect information.
'''


# eli5_criterion_11_12 = '''5 - Exceptional Clarity, Accuracy, and Engagement: The answer perfectly addresses the question with high accuracy and is presented in a clear, engaging, and imaginative manner that is perfectly tailored to a five-year-old's understanding. The response not only simplifies complex ideas but does so in a way that is captivating and memorable for a child.
# 4 - Clear, Accurate, and Child-Friendly: The answer is accurate, relevant to the question, and presented in a way that is engaging and understandable for a five-year-old. It simplifies complex concepts effectively but may miss a small opportunity for further clarification or engagement.
# 3 - Moderately Accurate and Understandable: The answer is mostly accurate and somewhat understandable to a five-year-old. It addresses the question reasonably well but may lack detail or contain some inaccuracies. The language and concepts are simplified, but the explanation might not be entirely engaging or clear for a child.
# 2 - Partially Correct but Lacking: The answer addresses the question but is incomplete or has significant inaccuracies. It may contain some elements that are understandable to a five-year-old but fails to provide a clear or comprehensive explanation. Key aspects of the question are either ignored or misrepresented.
# 1 - Significantly Flawed: The answer has a remote connection to the question but is largely inaccurate or confusing. It contains major factual errors or is mostly irrelevant to the question. It may be somewhat understandable to a five-year-old but does not provide a coherent or correct explanation.
# 0 - Completely Inaccurate or Irrelevant: The answer is entirely off-topic, irrelevant, or factually incorrect. It does not address the question in any form suitable for a five-year-old or otherwise.
# '''

eli5_criterion = '''5 - Perfectly Addressed, Accurate and Clarity: The answer flawlessly addresses the question with exceptional accuracy and clarity. It simplifies complex concepts effectively and does so in a way that is captivating and memorable.
4 - Accurate and clear: The answer is accurate, relevant to the question, and presented in a way that is engaging and understandable. It simplifies complex concepts effectively but may miss a small opportunity for further clarification or engagement.
3 - Moderately Accurate and Understandable: The answer is mostly accurate and somewhat understandable. It addresses the question reasonably well but may lack detail or contain some inaccuracies. It may use complex terms or concepts that are not broken down into simpler ideas. 
2 - Relevant but Lacks Clarity or Accuracy: The answer is related to the question but lacks clarity or contains partial inaccuracies. It attempts to simplify the idea but does not do so effectively, leaving room for confusion or misunderstanding.
1 - Significantly Flawed: The answer addresses the question to a minimal extent but contains significant inaccuracies or misleading information. It might show a basic attempt to simplify the concept but fail in accuracy or relevance.
0 - Completely Inaccurate or Irrelevant: The answer is entirely off-topic, irrelevant, or factually incorrect. It fails to address the question and does not simplify complex ideas.
'''

CRITERION = {"asqa": asqa_criterion, "eli5": eli5_criterion}