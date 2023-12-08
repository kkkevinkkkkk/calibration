DATASET_NAMES = ["asqa", "eli5"]

asqa_eval_instruction = "Given an ambiguous factoid question that has different correct answers depending on interpretation, the answer should be a long-form summary that resolves the ambiguity. "
asqa_instruction = "You will be given an ambiguous factoid question which have different correct answers depneding on interpretation. Your answer should synthesize factual information from multiple sources into a long-form summary that resolves the ambiguity. Provide a clear and concise answer with an unbiased tone."
eli5_instruction = "You will be given a question and you need to provide an answer that's easy to understand. Keep it accurate, comprehensible and concise."
eli5_eval_instruction = "A student has been challenged to tackle a complex question and provide an answer that is clear and easy to grasp."



TASK_INSTRUCTIONS = {
    "asqa": asqa_instruction,
    "asqa_eval": asqa_eval_instruction,
    "eli5": eli5_instruction,
    "eli5_eval": eli5_eval_instruction
}