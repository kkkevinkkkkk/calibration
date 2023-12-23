asqa = {
    "instruction": "You will be given an ambiguous factoid question that has different correct answers depending on the interpretation. Your answer should synthesize factual information from multiple sources into a long-form summary that resolves the ambiguity. Provide a clear and concise answer with an unbiased tone.",
    "eval_instruction": "Given an ambiguous factoid question that has different correct answers depending on interpretation, the answer should be a long-form summary that resolves the ambiguity. ",
    "criterion": "5 - Completely Correct and Highly Relevant: The answer fully addresses the question, resolves the ambiguity, and provides a well-rounded resolution. All facts presented in the answer are accurate and relevant.\n4 - Mostly Correct and Relevant: The answer is very relevant and addresses the ambiguity well, but might have a minor oversight or inaccuracy. All the facts presented are accurate and relevant, or with only minor errors.\n3 - Partially Correct and Relevant: The answer is generally on topic and attempts to address the ambiguity, but there might be inaccuracies or omissions. The majority of the facts are correct, with a few errors.\n2 - Flawed but Somewhat Relevant: The answer somewhat addresses the topic but does not fully explore the question's ambiguity or does not provide a complete resolution. The facts presented are a mix of correct and incorrect information, with about half being accurate.\n1 - Mostly Incorrect or Mostly Irrelevant: The answer slightly touches upon the topic but misses the main point. The majority of the facts presented are incorrect, with only a small portion being accurate.\n0 - Completely Incorrect or Completely Irrelevant: The student's answer is completely off-topic, not related to the question at all, or contains only incorrect information.\n",
    "eval_examples_categorical": 'Example 1: \n\nQuestion: "Who plays patrick in 10 things i hate about you?"\n\nAnswer: "The character Patrick Verona in the 1999 film 10 Things I Hate About You is played by Heath Ledger. Heath Ledger was an Australian actor and director, best known for his roles in films such as The Dark Knight, Brokeback Mountain, and A Knight\'s Tale."\n\nComment: "Score: 3/5\n\nExplanation: The student correctly identified Heath Ledger as Patrick in the 1999 film but did not address the 2009 TV show where Ethan Peck played Patrick, leaving the answer incomplete in addressing the question\'s ambiguity."\n\nExample 2:\n\nQuestion: "Who conducted a 300 mile march to sacramento california?"\n\nAnswer: "There have been several marches to Sacramento, California, but the 1965 Selma to Montgomery marches in Alabama, led by Martin Luther King Jr., are among the most notable. These marches demanded voting rights for African Americans and culminated in the Voting Rights Act of 1965."\n\nComment: "Score: 0/5\n\nExplanation: The student\'s answer focuses on the Selma to Montgomery marches in Alabama, which are not related to the question about a 300-mile march to Sacramento, California. While the student\'s information about the Selma to Montgomery marches is accurate, it does not address the given question."\n\nExample 3:\n\nQuestion: "What’s the capital of Georgia?"\n\nAnswer: "The capital of Georgia (U.S. state) is Atlanta, while the capital of Georgia (country) is Tbilisi."\n\nComment: "Score: 5/5\n\nExplanation: The student\'s answer accurately identifies both capitals of Georgia: Atlanta for the U.S. state and Tbilisi for the country. It is concise and directly addresses the ambiguity in the question." \n',
    "demo_sep": "\n\n\n",
    "demo_prompt": "{INST}\n\nQuestion: {Q}\n\n{D}\nAnswer: {A}",
    "doc_prompt": "Document [{ID}](Title: {T}): {P}\n",
    "demos": [
        {
            "question": "Which is the most rainy place on earth?",
            "answer": "Several places on Earth claim to be the most rainy, such as Lloró, Colombia, which reported an average annual rainfall of 12,717 mm between 1952 and 1989, and López de Micay, Colombia, which reported an annual 12,892 mm between 1960 and 2012. However, the official record is held by Mawsynram, India with an average annual rainfall of 11,872 mm, although nearby town Sohra, India, also known as Cherrapunji, holds the record for most rain in a calendar month for July 1861 and most rain in a year from August 1860 to July 1861.",
            "docs": [
                {
                    "title": "Cherrapunji",
                    "text": "Cherrapunji Cherrapunji (; with the native name Sohra being more commonly used, and can also be spelled Cherrapunjee or Cherrapunji) is a subdivisional town in the East Khasi Hills district in the Indian state of Meghalaya. It is the traditional capital of aNongkhlaw \"hima\" (Khasi tribal chieftainship constituting a petty state), both known as Sohra or Churra. Cherrapunji has often been credited as being the wettest place on Earth, but for now nearby Mawsynram currently holds that distinction. Cherrapunji still holds the all-time record for the most rainfall in a calendar month for July 1861 and most rain in a year from August 1860 to July 1861, however: it received in"
                },
                {
                    "title": "Cherrapunji",
                    "text": "Radio relay station known as Akashvani Cherrapunji. It broadcasts on FM frequencies. Cherrapunji Cherrapunji (; with the native name Sohra being more commonly used, and can also be spelled Cherrapunjee or Cherrapunji) is a subdivisional town in the East Khasi Hills district in the Indian state of Meghalaya. It is the traditional capital of aNongkhlaw \"hima\" (Khasi tribal chieftainship constituting a petty state), both known as Sohra or Churra. Cherrapunji has often been credited as being the wettest place on Earth, but for now nearby Mawsynram currently holds that distinction. Cherrapunji still holds the all-time record for the most rainfall"
                },
                {
                    "title": "Mawsynram",
                    "text": "Mawsynram Mawsynram () is a village in the East Khasi Hills district of Meghalaya state in north-eastern India, 65 kilometres from Shillong. Mawsynram receives one of the highest rainfalls in India. It is reportedly the wettest place on Earth, with an average annual rainfall of 11,872 mm, but that claim is disputed by Lloró, Colombia, which reported an average yearly rainfall of 12,717 mm between 1952 and 1989 and López de Micay, also in Colombia, which reported an annual 12,892 mm per year between 1960 and 2012. According to the \"Guinness Book of World Records\", Mawsynram received of rainfall in 1985. Mawsynram is located at 25° 18′"
                },
                {
                    "title": "Earth rainfall climatology",
                    "text": "Pacific Northwest, and the Sierra Nevada range are the wetter portions of the nation, with average rainfall exceeding per year. The drier areas are the Desert Southwest, Great Basin, valleys of northeast Arizona, eastern Utah, central Wyoming, eastern Oregon and Washington and the northeast of the Olympic Peninsula. The Big Bog on the island of Maui receives, on average, every year, making it the wettest location in the US, and all of Oceania. The annual average rainfall maxima across the continent lie across the northwest from northwest Brazil into northern Peru, Colombia, and Ecuador, then along the Atlantic coast of"
                },
                {
                    "title": "Going to Extremes",
                    "text": "in the world. Oymyakon in Siberia, where the average winter temperature is −47 °F (− 44 °C). Arica in Chile, where there had been fourteen consecutive years without rain. Fog is the only local source of water. Mawsynram in India, where average annual rainfall is 14 meters, falling within a four-month period in the monsoon season. The rainfall is approximately equal to that of its neighbor Cherrapunji. Dallol in Ethiopia, known as the 'Hell-hole of creation' where the temperature averages 94 °F (34 °C) over the year. In his second series, Middleton visited places without permanent towns, locations where \"survival\""
                }
            ]
        },
        {
            "question": "When did the us break away from england?",
            "answer": "The United States took the first step towards gaining independence from Great Britain when it declared independence from Great Britain on July 2, 1776 (although the event is now commemorated on July 4, 1776, the date when the Declaration of Independence was officially adopted by Congress). The Treaty of Paris was later signed on September 3, 1783, formally separating the United States from the British Empire.",
            "docs": [
                {
                    "title": "United States withdrawal from Saudi Arabia",
                    "text": "United States withdrawal from Saudi Arabia Beginning during Operation Desert Shield in August 1990, while preparing for the Gulf War, the United States sent a large troop contingent to Saudi Arabia. After the war, remnant troops, primarily U.S. Air Force personnel, augmented by a smaller number of coordinating and training personnel from the U.S. Navy, U.S. Army and U.S. Marine Corps remained in Saudi Arabia under the aegis of Joint Task Force Southwest Asia (JTF-SWA), as part of Operation Southern Watch (OSW). The United Kingdom and France also maintained a small contingent of Royal Air Force and French Air Force"
                },
                {
                    "title": "Decolonization of the Americas",
                    "text": "and France has fully \"integrated\" most of its former colonies as fully constituent \"departments\" of France. The United States of America declared independence from Great Britain on July 2, 1776 (although the event is now commemorated on July 4, the date when the Declaration of Independence was officially adopted by Congress), in so doing becoming the first independent, foreign-recognized nation in the Americas and the first European colonial entity to break from its mother country. Britain formally acknowledged American independence in 1783 after its defeat in the American Revolutionary War. Although initially occupying only the land east of the Mississippi"
                },
                {
                    "title": "American Revolution",
                    "text": "second British army at Yorktown in the fall of 1781, effectively ending the war. The Treaty of Paris was signed September 3, 1783, formally ending the conflict and confirming the new nation's complete separation from the British Empire. The United States took possession of nearly all the territory east of the Mississippi River and south of the Great Lakes, with the British retaining control of Canada and Spain taking Florida. Among the significant results of the revolution was the creation of the United States Constitution, establishing a relatively strong federal national government that included an executive, a national judiciary, and"
                },
                {
                    "title": "Decolonization",
                    "text": "accelerate decolonialization and bring an end to the colonial empires of its Western allies, most importantly during the 1956 Suez Crisis, but American military bases were established around the world and direct and indirect interventions continued in Korea, Indochina, Latin America (\"inter alia\", the 1965 occupation of the Dominican Republic), Africa, and the Middle East to oppose Communist invasions and insurgencies. Since the dissolution of the Soviet Union, the United States has been far less active in the Americas, but invaded Afghanistan and Iraq following the September 11 attacks in 2001, establishing army and air bases in Central Asia. Before"
                },
                {
                    "title": "Decolonization",
                    "text": "the responsibility of the United Kingdom (with a copy of the new constitution annexed), and finally, if approved, issuance of an Order of Council fixing the exact date of independence. After World War I, several former German and Ottoman territories in the Middle East, Africa, and the Pacific were governed by the UK as League of Nations mandates. Some were administered directly by the UK, and others by British dominions – Nauru and the Territory of New Guinea by Australia, South West Africa by the Union of South Africa, and Western Samoa by New Zealand. Egypt became independent in 1922,"
                }
            ]
        },
        {
            "question": "Who set the record for longest field goal?",
            "answer": "The record for the longest field goal in an NFL game was set by Matt Prater at 64 yards, but the record for the longest field goal at any level was 69 yards, kicked by collegiate kicker Ove Johansson in a 1976 Abilene Christian University football game against East Texas State University.",
            "docs": [
                {
                    "title": "Field goal",
                    "text": "toward its own end. The longest field goal kick in NFL history is 64 yards, a record set by Matt Prater on December 8, 2013. The previous record was 63, originally set by Tom Dempsey (1970) and then matched by Jason Elam (1998), Sebastian Janikowski (2011), David Akers (2012), and Graham Gano (2018). High school, college and most professional football leagues offer only a three-point field goal; however, some professional leagues have encouraged more rare kicks through \"four-point field goals\". NFL Europe encouraged long field goals of 50 yards or more by making those worth four points instead of three"
                },
                {
                    "title": "Field goal range",
                    "text": "35 and 40 yard lines (closer in a crosswind) often will go for the more risky fourth down conversion rather than risk either the touchback or the missed field goal. The longest field goal in recorded football history was 69 yards, set by collegiate kicker Ove Johansson, who was born in Sweden, in a 1976 Abilene Christian University football game against East Texas State University (now Texas A&M Commerce) at Shotwell Stadium in Abilene. The longest successful field goal in the NFL was 64 yards and was completed by Matt Prater in 2013. The NCAA record is 67 yards held"
                },
                {
                    "title": "Field goal",
                    "text": "both end zones) is only 66 yards. Scaccia, while playing indoor football, attempted a 64-yard kick that was inches short of success, hitting the crossbar. Longer field goals have been attempted at times; the longest attempt in the NFL, which was well short and was kicked into the wind, was 76 yards, attempted by Sebastian Janikowski of the Oakland Raiders, in a September 28, 2008 game against the San Diego Chargers. NFL Europe rewarded kickers that successfully kicked a field goal of longer than 50 yards with a bonus point, making such field goals worth 4 points instead of 3;"
                },
                {
                    "title": "Field goal",
                    "text": "this accomplishment is not the official record. All of the above kicks were successful with the use of a kicking tee, which was banned by the NCAA after the 1988 season. The longest known drop-kicked field goal in college football was a 62-yard kick from Pat O'Dea, an Australian kicker who played on the Wisconsin Badgers football team. O'Dea's kick took place in a blizzard against Northwestern on November 15, 1898. The longest field goal in U Sports football history is 59 yards, by Niko Difonte of Calgary Dinos, playing against the UBC Thunderbirds on November 11, 2017. The field"
                },
                {
                    "title": "Field goal range",
                    "text": "NFL and have been banned from NCAA since 1989) is 68 yards held by Fabrizio Scaccia, and the high school record 68 yards held by Dirk Borgognone; high school has wider goal posts and treats a field goal attempt that lands short in the field of play the same as a punt, making longer attempts much less risky. The indoor football record, with narrower and higher goal posts, is 63 yards (set by Aaron Mills), which is practically as long of a field goal as is possible in that variant of the sport, since the field in indoor football (including"
                }
            ]
        },
        {
            "question": "Who played galen in planet of the apes?",
            "answer": "In the 1968 film Planet of the Apes, Galen was played by Wright King. And in the tv series Planet of the Apes, Galen was played by Roddy McDowall.",
            "docs": [
                {
                    "title": "Planet of the Apes",
                    "text": "installment. Jacobs died on June 27, 1973, bringing an end to the APJAC Productions era of the \"Planet of the Apes\" franchise. Former Fox executive Stan Hough took over as producer for the television project, titled \"Planet of the Apes\". CBS picked up the series for its 1974 autumn lineup. Ron Harper and James Naughton played Alan Virdon and Peter Burke, two 20th-century American astronauts who pass through a time warp to a future where apes subjugate humans (unlike the original film, the humans can speak). Roddy McDowall returned to the franchise as Galen, a chimpanzee who joins the astronauts."
                },
                {
                    "title": "Planet of the Apes (1968 film)",
                    "text": "chimpanzees: animal psychologist Zira (Kim Hunter) and surgeon Galen (Wright King). While unable to speak as his throat wound is healing, called \"Bright Eyes\" by Zira and placed with one of the captive primitive humans he later names \"Nova\", Taylor observes the enhanced society of talking apes and in a strict caste system: the gorillas being the military police, hunters and workers; the orangutans overseeing the affairs of government, science, and religion; and intellectual chimpanzees being mostly scientists. While their society is a theocracy similar to the beginnings of the human Industrial Era, the apes consider the primitive humans as"
                },
                {
                    "title": "Planet of the Apes (1968 film)",
                    "text": "Planet of the Apes (1968 film) Planet of the Apes is a 1968 American science fiction film directed by Franklin J. Schaffner. It stars Charlton Heston, Roddy McDowall, Kim Hunter, Maurice Evans, James Whitmore, James Daly and Linda Harrison. The screenplay by Michael Wilson and Rod Serling was loosely based on the 1963 French novel \"La Plan\u00e8te des Singes\" by Pierre Boulle. Jerry Goldsmith composed the groundbreaking avant-garde score. It was the first in a series of five films made between 1968 and 1973, all produced by Arthur P. Jacobs and released by 20th Century Fox. The film tells the"
                },
                {
                    "title": "Planet of the Apes",
                    "text": "Rupert Wyatt. To portray ape characters realistically, the production avoided practical effects in favor of performance capture acting, partnering with New Zealand visual effects company Weta Digital. Wyatt cast James Franco as Will Rodman, while veteran performance capture actor Andy Serkis signed on to star as Caesar. \"Rise\" debuted on August 5, 2011. Critics reviewed it positively, especially praising the visual effects and Serkis's performance. It was a major box office hit, taking in $482 million globally, more than five times its $93 million budget. Weta's special effects earned the film two Visual Effects Society Awards and an Oscar nomination"
                },
                {
                    "title": "Planet of the Apes",
                    "text": "film stars Mark Wahlberg as astronaut Leo Davidson, who accidentally travels through a wormhole to a distant planet where talking apes enslave humans. He leads a human revolt and upends ape civilization by discovering that the apes evolved from the normal earth primates who had accompanied his mission, and arrived years before. Helena Bonham Carter played chimpanzee Ari, while Tim Roth played the human-hating chimpanzee General Thade. The film received mixed reviews; most critics believed it failed to compare to the original. Much of the negative commentary focused on the confusing plot and twist ending, though many reviewers praised the"
                }
            ]
        }
    ]
}



eli5 = {
    "instruction": "You will be given a question and you need to provide an answer that's easy to understand. Keep it accurate, comprehensible and concise.",
    "eval_instruction": "A student has been challenged to tackle a complex question and provide an answer that is clear and easy to grasp.",
    "criterion": "5 - Perfectly Addressed, Accurate and Clarity: The answer flawlessly addresses the question with exceptional accuracy and clarity. It simplifies complex concepts effectively and does so in a way that is captivating and memorable.\n4 - Accurate and clear: The answer is accurate, relevant to the question, and presented in a way that is engaging and understandable. It simplifies complex concepts effectively but may miss a small opportunity for further clarification or engagement.\n3 - Moderately Accurate and Understandable: The answer is mostly accurate and somewhat understandable. It addresses the question reasonably well but may lack detail or contain some inaccuracies. It may use complex terms or concepts that are not broken down into simpler ideas. \n2 - Relevant but Lacks Clarity or Accuracy: The answer is related to the question but lacks clarity or contains partial inaccuracies. It attempts to simplify the idea but does not do so effectively, leaving room for confusion or misunderstanding.\n1 - Significantly Flawed: The answer addresses the question to a minimal extent but contains significant inaccuracies or misleading information. It might show a basic attempt to simplify the concept but fail in accuracy or relevance.\n0 - Completely Inaccurate or Irrelevant: The answer is entirely off-topic, irrelevant, or factually incorrect. It fails to address the question and does not simplify complex ideas.\n",
    "eval_examples_categorical": 'Example 1:\n\nQuestion: "why are things ___.99 and they dont just round up?"\n\nAnswer:  "Stores often price items at $4.99 or $9.99 instead of rounding up to the nearest dollar because of "cents." Cents are smaller units of money like pennies. Stores use these cents to manage their finances, ensuring they have enough money for necessary expenses. This pricing strategy is a common practice in retail, and it can sometimes lead to finding items on sale for even less! It\'s a unique way adults handle money, and one day, you might do the same."\n\nComment: "Score: 0/5\nExplanation: The answer fails to address the core concept of the question, which is the psychological impact of .99 pricing on consumer perception. Instead, it discusses the use of cents in retail pricing for financial management, which is not relevant to the question about why prices are often set just below a round number. Therefore, the answer is given a score of 0 for its lack of factual accuracy and relevance to the specific question asked."\n\nExample 2:\n\nQuestion: "Why is second day chili better? "\n\nAnswer: "Second day chili tastes better because the flavors have more time to meld and intensify. As it rests, the spices and ingredients infuse more deeply, creating a richer and more harmonious flavor when reheated."\n\nComment: "Score: 5/5\nExplanation: The answer effectively conveys why second day chili might taste better. It explains that the flavors have more time to meld and intensify, which is a valid point. The idea that spices and ingredients infuse more deeply over time, creating a richer and more harmonious flavor, is accurate and relevant to the question. This explanation aligns well with the general understanding of how flavors develop in dishes like chili over time."\n\nExample 3:\n\nQuestion: "Why is it that I\'ve lost weight by the time I have awaken in the morming, yet I haven\'t gone to the washroom? Where did all of the weight go? "\n\nAnswer: "When we sleep, our bodies perform a neat trick – they slightly shrink! This happens because our bodies don\'t need as much energy while we\'re resting, so they use this time for a bit of weight-loss magic. That\'s why you might feel lighter in the morning, even before visiting the bathroom. Remember, your body is capable of some amazing things while you sleep! "\n\nComment: "Score: 1/5\nExplanation: The answer is creative but factually inaccurate. It suggests the body "shrinks" and performs "weight-loss magic" during sleep, which is not scientifically correct. The key point is that weight loss overnight is due to exhaling carbon dioxide, which was not mentioned in the response. Therefore, while engaging for young listeners, the answer is misleading and lacks relevance to the actual process of weight loss during sleep. "\n',
    "demo_sep": "\n\n\n",
    "demo_prompt": "{INST}\n\nQuestion: {Q}\n\n{D}\nAnswer: {A}",
    "doc_prompt": "Document [{ID}](Title: {T}): {P}\n",
    "demos": [
        {
            "question": "Why did New York City try to ban food donations to the poor?",
            "answer": "New York City, under Mayor Michael Bloomberg's administration, banned citizens from donating food directly to homeless shelters because the city could not assess the salt, fat, and fiber content. Bloomberg's administration was heavily criticized for losing their common sense by becoming too focused on what people eat.",
            "docs": [
                {
                    "title": "The Future Of America",
                    "text": "believe that they are \u201chelping\u201d the homeless by passing such laws. In New York City, Mayor Bloomberg has banned citizens from donating food directly to homeless shelters and he is actually convinced that it was the right thing to do for the homeless\u2026 Mayor Michael Bloomberg\u2019s food police have struck again! Outlawed are food donations to homeless shelters because the city can\u2019t assess their salt, fat and fiber content, reports CBS 2\u2019s Marcia Kramer. Glenn Richter arrived at a West Side synagogue on Monday to collect surplus bagels \u2014 fresh nutritious bagels \u2014 to donate to the poor."
                },
                {
                    "title": "mayor bloomberg",
                    "text": "Amuck: Bloomberg Bans Food Donations in New York City Food Might Be Salty or Too High in Calories, City Explains Washington, D.C. \u2013 New York Mayor Michael Bloomberg\u2019s administration is now banning all food being offered to the city\u2019s homeless shelters. New York City\u2019s bureaucrats have become so singularly focused on what people eat, says the National Center for Public Policy Research, that they\u2019ve lost their common sense. \u201cSo much for serving the homeless: The Bloomberg administration is now taking the term \u2018food police\u2019 to new depths, blocking food donations to all government-run facilities that serve the"
                },
                {
                    "title": "New York City bans food donations - WND",
                    "text": "New York City bans food donations - WND Front Page Health U.S. New York City bans food donations Inability to control 'nutritional content' cited as reason New York City homeless shelters have Mayor Michael Bloomberg to thank for a halt in food donations, for which hungry families are waiting, according to one public policy advocate. \"The Bloomberg administration is now taking the term 'food police' to new depths, blocking food donations to all government-run facilities that serve the city's homeless,\" says Jeff Stier, a National Center for Public Policy Research senior fellow. Currently, no food can be given to government-run, New York City facilities, despite hungry crowds perfectly"
                },
                {
                    "title": "New York City bans food donations - WND",
                    "text": "New York City bans food donations - WND Services didn't return WND calls. Stier told WND that he specifically was told by Diamond that the policy was tied to the nutritional guidelines set by the mayor. \"They can say that this ban on donations is a long-standing policy, but they can\u2019t document it,\" Stier told WND. \"I've also been told that there are numerous food shelves that have been accepting food donations, not just one.\" Stier is a member of a New York Synagogue that has donated food for over a decade. He is outraged that the DHS' response to his demand to know why the practice can"
                },
                {
                    "title": "New York City bans food donations - WND",
                    "text": "New York City bans food donations - WND ban on donated food. In fact, it thrives because of food donations. New York City Rescue Mission has been providing food, clothing, shelter and spiritual hope for needy New Yorkers since 1872. \"We feed over 500 people a day, all through donations,\" said James Varnhagen, NYCRM director. \"Boxed food, canned food, prepared food, we take any food,\" he told WND. \"We couldn't survive without donations,\" he said."
                }
            ]
        },
        {
            "question": "What's the difference between Shia vs. Sunni Islam?",
            "answer": "The main difference between Shia and Sunni Muslim is related to ideological heritage and issues of leadership. This difference is first formed after the death of the Prophet Muhammad in 632 A.D. The ideological practice of the Sunni branch strictly follows Prophet Muhammad and his teachings, while the Shia branch follows Prophet Muhammad's son-in-law Ali. Nowadays, Sunni and Shia are the major branches of Islam.",
            "docs": [
                {
                    "title": "The Sunni vs Shia Divide - Explained - Globaloi",
                    "text": "centuries-long strained relationship between Sunnis and Shias. As a scholar of Islam and a public educator, I often field questions about Sunnis, Shias and the sects of Islam. What exactly is the Shia-Sunni divide? And what is its history? History of divide Both Sunnis and Shias \u2013 drawing their faith and practice from the Qur\u2019an and the life of the Prophet Muhammad \u2013 agree on most of the fundamentals of Islam. The differences are related more to historical events, ideological heritage and issues of leadership. The first and central difference emerged after the death of Prophet Muhammad in A.D. 632."
                },
                {
                    "title": "What\u2019s the difference between Sunni and Shia Islam? \u2013 Macrosnaps",
                    "text": "What\u2019s the difference between Sunni and Shia Islam? Sunni and Shia identities (the 2 main branches of Islam) first formed around a dispute over leadership succession after the death of the Prophet Muhammad in 632 A.D. Sunni is the larger branch (estimated 85-90% of total world Muslim population) and it's adherents are referred to as \"people of the tradition of Muhammad\", while Shia are \"followers\" of Muhammad's son-in-law and cousin Ali. Sunnis rely heavily on the practice of the Prophet Muhammad and his teachings, the Shia view their ayatollahs as reflections of God on earth. What challenges does the anti-IS"
                },
                {
                    "title": "Difference between Sunni and Shia Muslims | Sunni vs Shia Muslims",
                    "text": "of Muhammad, the last prophet of God. A follower of Islam is known as a Muslim. Many Muslims believe that their sole purpose is to worship and serve God, for which they have established five pillars of Islam that guides a Muslim on almost every aspect of life and society. Due to differences, Muslims have been divided into two primary sects: The Sunnis and the Shias. These two sects have many similarities and both consider themselves are Muslims, following the will of God. However, they are also different from each other in certain aspects. Both the Sunnis and the Shias,"
                },
                {
                    "title": "What is the difference between Shia and Sunni Islam? - Islam Stack Exchange",
                    "text": "What is the difference between Shia and Sunni Islam? - Islam Stack Exchange between Mutah marriage and Misyar marriage? What theological and historical factors distinguish Ibadi Islam from either Shia or Sunni schools? What are the principle/fundamental differences between Sunni and Shia? Nikah between a Sunni girl and Shia boy What is the difference between \u201cMubtalat-of-Wudu\u201d of Shia and Sunni? How can the Hadith be reliable when Sunnis and Shia follow different points of reference? Rejection of Mutawatir Hadith in Sunni Islam and Shia Islam"
                },
                {
                    "title": "What is the difference between Sunni and Shia Islam? | Patrick Syder Travel",
                    "text": "What is the difference between Sunni and Shia Islam? | Patrick Syder Travel What is the difference between Sunni and Shia Islam? This Channel 4 link answers some of the key questions about the difference between Sunni and Shia Islam and alarmingly, the politics on what is happening and why, in Syria\u2026\u2026. http://www.channel4.com/news/sunni-shia-islam-muslim-syria-middle-east-key-questions \u2190 Ethiopia Appeal \u2013 Help sponsor a nurse to train and to help others G\u00f6bekli Tepe, Turkey: a new wonder of the ancient world by Jeremy Seal (Telegraph Travel Section 23/04/2013) \u2192"
                }
            ]
        },
        {
            "question": "What causes Bi-polar disorder?",
            "answer": "Bipolar disorder is an emotional disorder that causes extreme mood swings between excitement and depression. The spectrum of mood swing may span from days to months. We are still not certain of the exact factors that cause such disorder, but genetics is considered a major factor.",
            "docs": [
                {
                    "title": "Bi-polar disorder | definition of Bi-polar disorder by Medical dictionary",
                    "text": "bi-polar disorder | definition of bi-polar disorder by medical dictionary https://medical-dictionary.thefreedictionary.com/bi-polar+disorder (redirected from bi-polar disorder) related to bi-polar disorder: depression bipolar disorder, formerly known as manic depression, is a mood disorder that causes radical emotional changes and mood swings, from manic, restless highs to depressive, listless lows. most bipolar individuals experience alternating episodes of mania and depression. bipolar disorder is characterized by alternating manic episodes in which the individual feels abnormally euphoric, optimistic, and energetic and depressive periods in which the individual feels sad, hopeless, guilty, and sometimes suicidal. manic or depressive periods may last for days, weeks, or months"
                },
                {
                    "title": "Mania and Bi-Polar",
                    "text": "can go from depressed to \u201csuper happy\u201d all in one day, or even in a few days, does not have a bi-polar disorder Bi-polar looks different depending on the severity of the symptoms. Most bi-polar diagnoses that are made are for bi-polar 2, with bi-polar 1 being much more rare. Bi-polar 1 is so severe that the individual will have periods of such agitation, or such reckless and seemingly foolish behavior that they put themselves or those around them in danger. It is not completely clear what causes bi-polar, but genetics seem to have a large role. The biggest factor"
                },
                {
                    "title": "Bi-Polar disorder",
                    "text": "Bi-Polar disorder Bi-polar is generally a cyclic disease where individuals display depressive and elevated episodes at regular intervals. It is a disorder resulting from the imbalance of the chemicals in the brain that causes a lot of fluctuations of mood. It is a fact that we all experience happy and sad moods, but people with bi-polar disorder experience the changes in mood at an increased level. The cause of this disorder is not known completely. However, it is estimated that there are different factors responsible for it. It is often connected to a genetic component. People suffering from the Bi-polar disorder are"
                },
                {
                    "title": "For Individuals \u2014 Adam Schwartz",
                    "text": "For Individuals \u2014 Adam Schwartz The information is extensive and covers a huge range of topics. Some of the topics include the different types of bi-polar, what it feels like, signs and symptoms, treatments and more. Black Dog Institute bi-polar causes resource specifically covers the variety of areas that could potentially be a cause of bi-polar disorder. Including genetics, environmental factors, pregnancy, and more. Black Dog Institute bi-polar treatments resource specifically covers multiple potential treatments options for bi-polar. Including management, types of psychological treatment, lifestyle changes, and more. Black Dog Institute bi-polar self-test resource is a short self-test for people who may be concerned if"
                },
                {
                    "title": "Depression Bi-polar Disorder Symptoms 2019 | Win Over Depression",
                    "text": "Depression Bi-polar Disorder Symptoms 2019 | Win Over Depression signs and symptoms of bipolar disorder. Learn more about the common symptoms of bipolar depression that some patients may experience. Home \u00bb Trending Health News \u00bb 10 Warning Signs of Bipolar Disorder: Depression. One of the most serious symptoms of bipolar disorder is. Bi Polar Depression. SEVERE SWINGS What is bipolar disorder, is it the same as manic depression, what are the symptoms and is there a cure? Bipolar disorder, or manic depression, causes symptoms of mania and depression. Read about bipolar disorder treatment, medications, and causes of this. Learn more about the different types of bipolar disorder. Find out"
                }
            ]
        },
        {
            "question": "How do student loans affect getting a mortgage?",
            "answer": "When applying for a mortgage, student loans can affect the debt to income ratio, which is a key factor in determining the amount that an individual can afford to pay for the mortgage. While student loan repayments do not appear in an individual's credit history and do not affect credit scores, lenders do consider the amount of an individual's student loan repayments when assessing their mortgage application. Some 83% of non-homeowners say student loan debt is preventing them from buying a home, according to the National Association of Realtors. It is important to note that student loans do not prevent an individual from getting a mortgage.",
            "docs": [
                {
                    "title": "Student Loans \u2013 How do they work? | The Financial Review",
                    "text": "typical debt. Student loan repayments do not appear in an individual\u2019s credit history, therefore there are no implications whatsoever. This also extends to applications for credit cards \u2013 student \u2018loans\u2019 are not acknowledged. One noteworthy aspect that is affected by student loans however, is mortgage applications. Nevertheless, it does not prevent an individual from getting a mortgage. For example, lenders will consider the amount of an individual\u2019s student loan repayments in order to assess the debt to income ratio and therefore establish the amount that the individual can afford to pay for the mortgage. Just as they do with other"
                },
                {
                    "title": "How Does Student Loan Debt Affect Buying a Home? | Experian",
                    "text": "Rates & Affordability How Student Loans Affect Getting a Mortgage Student Loan Impact on Credit Scores Other Factors for Getting Approved for a Mortgage If you're a recent college grad and hope to become a homeowner in the near future, you should know that student loan debt could affect buying a home by making it more difficult to get a mortgage. Some 83% of non-homeowners say student loan debt is preventing them from buying a home, according to the National Association of Realtors (NAR). But while student loan payments can make it harder to save for a down payment on"
                },
                {
                    "title": "Studentloanify - How your student loans affect your home mortgage prospects",
                    "text": "Though it may not seem fair, your student loan situation impacts your home mortgage outlook. Many people carry student loan debt, but it\u2019s the amount of the loan and how you handle your student loan repayment plan that will influence your ability to get a home mortgage as well as what your interest rate will be. Here are some specific factors about your student loan that will affect your home mortgage prospects. On your mortgage loan application, you will have to report how much your monthly student loan payment is. This amount will be deducted from your monthly gross income"
                },
                {
                    "title": "How do student loans affect your credit score? | Student Loan Planner",
                    "text": "How do student loans affect your credit score? | Student Loan Planner Your credit score is the three-digit number that dictates a lot in your adult life. Whether you\u2019re applying for a mortgage or looking to get an auto loan, this seemingly arbitrary number determines whether you get approved for a loan and also affects your interest rate. If you\u2019re a student loan borrower you may wonder, \u201cDo student loans affect credit score?\u201d You might be especially curious if you\u2019re in the process of applying for a mortgage. Here\u2019s how student loans affect your credit score and what to know for big life events, like getting a mortgage. Do student loans affect"
                },
                {
                    "title": "Does Student Loan Debt Affect Getting A Mortgage?",
                    "text": "Does Student Loan Debt Affect Getting A Mortgage? Home \u00bb Does Student Loan Debt Affect Getting A Mortgage? Last year, I helped answer a reader\u2019s question about applying for a mortgage while on Income Based Repayment. However, over the last several months, I\u2019ve been getting bombarded with questions about how student loan debt impacts your ability to get a mortgage. Maybe it\u2019s because the housing market is improving, or maybe it\u2019s because people are finally taking their student loan debt seriously. Anyway, I wanted to share a few reader questions and then look at whether student loan debt affects getting a mortgage. Here are the reader questions I\u2019ve"
                }
            ]
        }
    ]
}

qampari = {
    "instruction": "Provide a list of accurate answers for the given question. Separate answers by commas. For questions that have more than 5 answers, write at least 5 answers. Make sure the answer is only a list of answers, without any other text.",
    "eval_instruction": "A student has been asked to provide a list of accurate answers for a given question. The answers is seperated by commas.",
    "criterion": "TODO",
    "eval_examples_categorical": 'TODO',
    "demo_sep": "\n\n\n",
    "demo_prompt": "{INST}\n\nQuestion: {Q}\n\n{D}\nAnswer: {A}",
    "doc_prompt": "Document [{ID}](Title: {T}): {P}\n",
    "demos": [
        {
            "question": "Which books were written by Nevil Shute?",
            "answer": "Marazan, Stephen Morris, Beyond the Black Stump, Lonely Road, The Chequer Board, In the Wet, Trustee from the Toolroom, Round the Bend, No Highway, Ruined City, On the Beach.",
            "docs": [
                {
                    "title": "Nevil Shute",
                    "text": "early stages. My congratulations.\" His celebrity as a writer caused the Ministry of Information to send him to the Normandy Landings on 6 June 1944 and later to Burma as a correspondent. He finished the war with the rank of lieutenant commander in the Royal Navy Volunteer Reserves (RNVR). Shute's first novel, \"Stephen Morris\", was written in 1923, but not published until 1961. His first published novel was \"Marazan\", which came out in 1926. After that he averaged one novel every two years through the 1950s, with the exception of a six-year hiatus while he was establishing his own aircraft"
                },
                {
                    "title": "Nevil Shute",
                    "text": "theme is the bridging of social barriers such as class (\"Lonely Road\" and \"Landfall\"), race (\"The Chequer Board\"), or religion (\"Round the Bend\"). The Australian novels are individual hymns to that country, with subtle disparagement of the mores of the United States (\"Beyond the Black Stump\") and overt antipathy towards the post-World War II socialist government of Shute's native Britain (\"The Far Country\" and \"In the Wet\"). Shute's heroes tended to be like himself: middle class solicitors, doctors, accountants, bank managers, engineers, generally university graduates. However (as in \"Trustee from the Toolroom\"), Shute valued the honest artisans and their social"
                },
                {
                    "title": "Nevil Shute",
                    "text": "construction company, Airspeed Ltd. His popularity grew slowly with each novel, but he became much more famous after the publication of \"On the Beach\" in 1957. Shute's novels are written in a simple, highly readable style, with clearly delineated plot lines. Where there is a romantic element, sex is referred to only obliquely. Many of the stories are introduced by a narrator who is not a character in the story. The most common theme in Shute's novels is the dignity of work, spanning all classes, whether an Eastern European bar \"hostess\" (\"Ruined City\") or brilliant boffin (\"No Highway\"). Another recurrent"
                },
                {
                    "title": "The Chequer Board",
                    "text": "the Burmese people\", both of which are central to the book's story. Shute was concerned that sales of the book in the United States would be negatively impacted by the book's open-minded handling of racial issues; as it turned out, sales soared. Shute and his wife traveled the U.S. on Greyhound buses to \"\"get in touch with the man on the street,\"\" finding the experience refreshing. Afterwards he wrote \"\"Sincerity is the first attribute for making money in the business of writing novels.\"\" The Chequer Board The Chequer Board is a novel by Nevil Shute, first published in the United"
                },
                {
                    "title": "In the Wet",
                    "text": "had used the idea of multiple votes for merit in his short story \"The Curious Republic of Gondour\". In the Wet In The Wet is a novel by Nevil Shute that was first published in the United Kingdom in 1953. It contains many of the typical elements of a hearty and adventurous Shute yarn such as flying, the future, mystic states, and ordinary people doing extraordinary things. The story is opened by its initial narrator \u2013 an Anglican priest in the Bush Brotherhood named Roger Hargreaves \u2013 who describes his ordinary circumstances in a large parish of the Australian outback"
                }
            ]
        },
        {
            "question": "Which film has Gong Li as a member of its cast?",
            "answer": "The Story of Qiu Ju, Farewell My Concubine, Flirting Scholar, The Monkey King 2, Mulan, Saturday Fiction, Coming Home.",
            "docs": [
                {
                    "title": "Gong Li",
                    "text": "Gong Li Gong Li (born 31 December 1965) is a Chinese-born Singaporean film actress. She achieved international prominence through her close collaborations with Chinese director Zhang Yimou and won the Volpi Cup for Best Actress at Venice for her performance in his 1992 film \"The Story of Qiu Ju\". She has been credited with helping to bring Chinese cinema to prominence in Europe and the United States. In 2006, she was voted the most beautiful woman in China. Gong has won numerous accolades for her work as an actress; she won the New York Film Critics Circle Award for Best"
                },
                {
                    "title": "Gong Li",
                    "text": "making her realize that she has assisted the dark cynical system. In 1993, she received a New York Film Critics Circle award for her role in \"Farewell My Concubine\" (1993). Directed by Chen Kaige, the film was her first major role with a director other than Zhang Yimou. In the same year, she was awarded with the Berlinale Camera at the 43rd Berlin International Film Festival. \"Premiere\" magazine ranked her performance in \"Farewell My Concubine\" as the 89th greatest performance of all time. She also worked with renowned director Stephen Chow in comedy films \"\" (1991) and \"Flirting Scholar\" (1993)."
                },
                {
                    "title": "Gong Li",
                    "text": "International Film Festival. Later that same year, she reunited with Zhang Yimou for the film \"Coming Home\", which is set during the throes of the Cultural Revolution; this film was their first collaboration since 2006. In 2016, Gong took on her first action role in \"The Monkey King 2\", playing the White Bone Demon. In 2018, Gong was cast in Lou Ye's period drama \"Saturday Fiction\", where she plays an actress who is working undercover gathering intelligence for the Allies. That year, she was also cast in the live-action adaptation of the 1998 Disney animated film \"Mulan\", as an unspecified"
                },
                {
                    "title": "Zhang Yimou",
                    "text": "in Zhang's earlier films. \"Raise the Red Lantern\" was nominated in the Best Foreign Language Film category at the 1992 Academy Awards, becoming the second Chinese film to earn this distinction (after Zhang's \"Ju Dou\"). It eventually lost out to Gabriele Salvatores's \"Mediterraneo\". Zhang's next directorial work, \"The Story of Qiu Ju\", in 1992, once again starring Gong Li in the lead role. The film, which tells the tale of a peasant woman seeking justice for her husband after he was beaten by a village official, was a hit at film festivals and won the Golden Lion award at the"
                },
                {
                    "title": "Gong Li",
                    "text": "Gong Li Gong Li (born 31 December 1965) is a Chinese-born Singaporean film actress. She achieved international prominence through her close collaborations with Chinese director Zhang Yimou and won the Volpi Cup for Best Actress at Venice for her performance in his 1992 film \"The Story of Qiu Ju\". She has been credited with helping to bring Chinese cinema to prominence in Europe and the United States. In 2006, she was voted the most beautiful woman in China. Gong has won numerous accolades for her work as an actress; she won the New York Film Critics Circle Award for Best"
                }
            ]
        },
        {
            "question": "In which years did Patti LaBelle publish music?",
            "answer": "2006, 1977, 2004, 2005, 2000, 2006.",
            "docs": [
                {
                    "title": "The Gospel According to Patti LaBelle",
                    "text": "The Gospel According to Patti LaBelle The Gospel According to Patti LaBelle is the first gospel album released by singer Patti LaBelle, released in November 2006. This project began three years ago when Patti's late musical director and close friend Budd Ellison told a skeptical LaBelle that \"it's now or never, Patti.\" The album is dedicated to his memory as he succumbed to prostate cancer before the album saw a release. The album was released on November 21, 2006 through indie label Umbrella/Bungalow Records, also home to Carl Thomas, Rodney Jerkins, Dean \"DC\" Charles, and other artists. \"The Gospel According"
                },
                {
                    "title": "Patti LaBelle (album)",
                    "text": "scaled the high sixties on the \"Billboard\" R&B chart, it soon became one of her famous show-stoppers while performing the song. LaBelle performed the song at her first solo concert in London, getting a standing ovation, which helped to give LaBelle motivation to continue her career. The album, when released, performed successfully, reaching number 62 on the \"Billboard\" 200 and number 31 on the R&B albums chart, while critics hailed the album. Patti LaBelle (album) Patti LaBelle is the debut solo album by singer Patti LaBelle, released in 1977. The first album LaBelle recorded after sixteen years fronting the band"
                },
                {
                    "title": "Patti LaBelle",
                    "text": "win. In 2000, LaBelle released her final MCA album, \"When a Woman Loves\", before signing with Def Soul Classics to release the 2004 album, \"Timeless Journey\". Following the release of her 2005 covers album, \"Classic Moments\", LaBelle engaged in a rivalry with Antonio \"L.A.\" Reid over the direction of her career, leading to her leaving the label.In the same year, the World Music Awards recognized her years in the music business by awarding her the Legend Award. In 2006, she released her first gospel album, \"The Gospel According to Patti LaBelle\" on the Bungalo label, the album later peaking at"
                },
                {
                    "title": "Patti LaBelle",
                    "text": "Patti LaBelle Patti LaBelle (born Patricia Louise Holt; May 24, 1944) is an American singer, actress, and entrepreneur. LaBelle began her career in the early 1960s as lead singer and front woman of the vocal group, Patti LaBelle and the Bluebelles. Following the group's name change to Labelle in the early 1970s, they released the iconic disco song \"Lady Marmalade\" and the group later became the first African-American vocal group to land the cover of \"Rolling Stone\" magazine. After the group split in 1976, LaBelle began a successful solo career, starting with her critically acclaimed debut album, which included the"
                },
                {
                    "title": "The Gospel According to Patti LaBelle",
                    "text": "Billboard's Top Gospel Albums chart for 17 weeks. \"Where Love Begins,\" a duet with Yolanda Adams was played frequently on R&B and gospel radio stations and debuted at #68 on Billboard's Hot R&B/Hip-Hop tracks. The second single \"Anything\" featuring Kanye West, Mary Mary and Consequence hit #64 on Billboards Hot R&B/Hip-Hop tracks. In 2008, the album was nominated for a Dove Award for Contemporary Gospel Album of the Year at the 39th GMA Dove Awards. The Gospel According to Patti LaBelle The Gospel According to Patti LaBelle is the first gospel album released by singer Patti LaBelle, released in November"
                }
            ]
        },
        {
            "question": "Glenn Ford was a member of cast in which film?",
            "answer": "So Ends Our Night, Heaven with a Barbed Wire Fence, Happy Birthday to Me, The Greatest Gift, The Gift, The Brotherhood of the Bell.",
            "docs": [
                {
                    "title": "Glenn Ford",
                    "text": "name came from his father's hometown of Glenford, Alberta. His first major movie part was in the 1939 film, \"Heaven with a Barbed Wire Fence\". Top Hollywood director John Cromwell was impressed enough with his work to borrow him from Columbia for the independently produced drama, \"So Ends Our Night\" (1941), where Ford delivered a poignant portrayal of a 19-year-old German exile on the run in Nazi-occupied Europe. Working with Academy Award-winning Fredric March and wooing (onscreen) 30-year-old Margaret Sullavan, recently nominated for an Oscar, Ford's shy, ardent young refugee riveted attention even in such stellar company. \"Glenn Ford, a"
                },
                {
                    "title": "Glenn Ford",
                    "text": "were Westerns. He suggested doing a Western series, instead, which resulted in the \"modern-day Western\" series, \"Cade's County\". Ford played southwestern Sheriff Cade for one season (1971\u20131972) in a mix of police mystery and western drama. In \"The Family Holvak\" (1975\u20131976), Ford portrayed a Depression-era preacher in a family drama, reprising the same character he had played in the TV film, \"The Greatest Gift\". In 1978 Ford was host, presenter and narrator of the disaster documentary series 'When Havoc Struck'. In 1981, Ford co-starred with Melissa Sue Anderson in the slasher film \"Happy Birthday to Me\". In 1991, Ford agreed"
                },
                {
                    "title": "CBS Thursday Night Movie",
                    "text": "Night Movie\" opened its fall schedule with the premiere of a low-budget, made-for-TV movie, rather than a proven Hollywood blockbuster guaranteed to lure mass viewership, it became CBS's way of declaring its commitment to product that, although cheaply manufactured, was nevertheless new and topical. In this case, the movie was \"The Brotherhood of the Bell\", and the film's star was Glenn Ford, a movie actor who had never appeared in a television-film. In fact, before shooting on the project even began, Ford had been warned by friends in the industry that he would hate the experience. Instead, the actor reported"
                },
                {
                    "title": "The Trouble with Girls (film) ",
                    "text": "with Charlene, but when she refuses to give in, he deceives her and uses the local police force to be sure that she must leave on the train with the rest of the troupe. Cast notes In June 1959 it was announced that Don Mankiewicz would write a screenplay of an unpublished story by Mauri Grashin, Day Keene, and Dwight Babcock. By December 1960, with the project titled \"Chautauqua\", MGM was ready to make the film with Glenn Ford. Rumours circulating in Hollywood at the time stated that Presley would co-star with Ford, Hope Lange, and Arthur O'Connell, but nothing"
                },
                {
                    "title": "Trouble in the Glen",
                    "text": "Mel Ferrer. It was Orson Welles' fifth British movie in six months. Filming started 15 December 1953. The film received very poor reviews. Trouble in the Glen Trouble in the Glen is a 1954 British comedy film directed by Herbert Wilcox and starring Margaret Lockwood, Orson Welles, Forrest Tucker and Victor McLaglen. It is loosely based on Maurice Walsh's 1950 novel of the same name. It was filmed in Trucolor for Republic Pictures. After moving from South America to the Scottish Highlands, millionaire Sanin Cejador y Mengues (Welles) reassumes the title of laird of Glen Easan, which he inherited from"
                }
            ]
        }
    ]
}

DATASET_PROFILES = {
    "asqa": asqa,
    "eli5": eli5,
    "qampari": qampari,
}
TASK_PROFILES = DATASET_PROFILES
DATASET_NAMES = ["asqa", "eli5", "qampari"]