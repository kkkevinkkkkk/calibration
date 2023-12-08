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

asqa_eval_examples_categorical = '''Example 1: 

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

eli5_eval_categorical = '''Example 1:

Question: "why are things ___.99 and they dont just round up?"

Answer:  "Stores often price items at $4.99 or $9.99 instead of rounding up to the nearest dollar because of "cents." Cents are smaller units of money like pennies. Stores use these cents to manage their finances, ensuring they have enough money for necessary expenses. This pricing strategy is a common practice in retail, and it can sometimes lead to finding items on sale for even less! It's a unique way adults handle money, and one day, you might do the same."

Comment: "Score: 0/5
Explanation: The answer fails to address the core concept of the question, which is the psychological impact of .99 pricing on consumer perception. Instead, it discusses the use of cents in retail pricing for financial management, which is not relevant to the question about why prices are often set just below a round number. Therefore, the answer is given a score of 0 for its lack of factual accuracy and relevance to the specific question asked."

Example 2:

Question: "Why is second day chili better? "

Answer: "Second day chili tastes better because the flavors have more time to meld and intensify. As it rests, the spices and ingredients infuse more deeply, creating a richer and more harmonious flavor when reheated."

Comment: "Score: 5/5
Explanation: The answer effectively conveys why second day chili might taste better. It explains that the flavors have more time to meld and intensify, which is a valid point. The idea that spices and ingredients infuse more deeply over time, creating a richer and more harmonious flavor, is accurate and relevant to the question. This explanation aligns well with the general understanding of how flavors develop in dishes like chili over time."

Example 3:

Question: "Why is it that I've lost weight by the time I have awaken in the morming, yet I haven't gone to the washroom? Where did all of the weight go? "

Answer: "When we sleep, our bodies perform a neat trick – they slightly shrink! This happens because our bodies don't need as much energy while we're resting, so they use this time for a bit of weight-loss magic. That's why you might feel lighter in the morning, even before visiting the bathroom. Remember, your body is capable of some amazing things while you sleep! "

Comment: "Score: 1/5
Explanation: The answer is creative but factually inaccurate. It suggests the body "shrinks" and performs "weight-loss magic" during sleep, which is not scientifically correct. The key point is that weight loss overnight is due to exhaling carbon dioxide, which was not mentioned in the response. Therefore, while engaging for young listeners, the answer is misleading and lacks relevance to the actual process of weight loss during sleep. "
'''

EXAMPLES = {
    "asqa_eval": asqa_eval_examples,
    "asqa_eval_categorical": asqa_eval_examples_categorical,
    "eli5_eval_categorical": eli5_eval_categorical
}