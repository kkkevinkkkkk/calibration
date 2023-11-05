asqa_eval_examples = '''
Example 1: 

Question: "Who plays patrick in 10 things i hate about you?"

Answer: "The character Patrick Verona in the 1999 film 10 Things I Hate About You is played by Heath Ledger. Heath Ledger was an Australian actor and director, best known for his roles in films such as The Dark Knight, Brokeback Mountain, and A Knight's Tale."

Comment: "Score: 55/100

Explanation: The student's answer correctly identifies Heath Ledger as the actor who played Patrick in the 1999 film 10 Things I Hate About You. However, the answer does not address the ambiguity of the question, which could also refer to the 2009 TV show where Ethan Peck played Patrick. The additional information about Heath Ledger's other roles is interesting but not directly relevant to the question."

Example 2:

Question: "Who conducted a 300 mile march to sacramento california?"

Answer: "There have been several marches to Sacramento, California, but the 1965 Selma to Montgomery marches in Alabama, led by Martin Luther King Jr., are among the most notable. These marches demanded voting rights for African Americans and culminated in the Voting Rights Act of 1965."

Comment: "Score: 0/100

Explanation: The student's answer focuses on the Selma to Montgomery marches in Alabama, which are not related to the question about a 300-mile march to Sacramento, California. While the student's information about the Selma to Montgomery marches is accurate, it does not address the given question."

Example 3:

Question: "What’s the capital of Georgia?"

Answer: "The capital of Georgia (U.S. state) is Atlanta, while the capital of Georgia (country) is Tbilisi."

Comment: "Score: 100/100

Explanation: The student's answer accurately identifies both capitals of Georgia: Atlanta for the U.S. state and Tbilisi for the country. It is concise and directly addresses the ambiguity in the question." 
'''

asqa_eval_examples_5 = '''Example 1: 

Question: "Who plays patrick in 10 things i hate about you?"

Answer: "The character Patrick Verona in the 1999 film 10 Things I Hate About You is played by Heath Ledger. Heath Ledger was an Australian actor and director, best known for his roles in films such as The Dark Knight, Brokeback Mountain, and A Knight's Tale."

Comment: "Score: 3/5

Explanation: The student correctly identified Heath Ledger as Patrick in the 1999 film but did not address the 2009 TV show where Ethan Peck played Patrick, leaving the answer incomplete in addressing the question's ambiguity."

Example 2:

Question: "Who conducted a 300 mile march to sacramento california?"

Answer: "There have been several marches to Sacramento, California, but the 1965 Selma to Montgomery marches in Alabama, led by Martin Luther King Jr., are among the most notable. These marches demanded voting rights for African Americans and culminated in the Voting Rights Act of 1965."

Comment: "Score: 0/5

Explanation: The student's answer focuses on the Selma to Montgomery marches in Alabama, which are not related to the question about a 300-mile march to Sacramento, California. While the student's information about the Selma to Montgomery marches is accurate, it does not address the given question."

Example 3:

Question: "What’s the capital of Georgia?"

Answer: "The capital of Georgia (U.S. state) is Atlanta, while the capital of Georgia (country) is Tbilisi."

Comment: "Score: 5/5

Explanation: The student's answer accurately identifies both capitals of Georgia: Atlanta for the U.S. state and Tbilisi for the country. It is concise and directly addresses the ambiguity in the question." 
'''

EXAMPLES = {
    "asqa_eval": asqa_eval_examples,
    "asqa_eval_5": asqa_eval_examples_5,
}