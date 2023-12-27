from utils import make_head_prompt, TEMPLATES, make_demo, DATASET_PROFILES

class Prompter:
    def __init__(self, prompt_data=None,
                 model_name="gpt-3.5-turbo",
                 dataset_name=None,
                 n_shot=0,
                 n_doc=0,
                 n_doc_in_demo=0,
                 fewer_doc_in_demo=False,
                 no_doc_in_demo=True,
                 use_shorter="summary",
                 oracle_doc=False,
                 ):

        self.prompt_data = prompt_data
        self.model_name = model_name
        self.dataset_name = dataset_name
        self.n_shot = n_shot
        self.n_doc = n_doc
        self.n_doc_in_demo = n_doc_in_demo
        self.fewer_doc_in_demo = fewer_doc_in_demo
        self.no_doc_in_demo = no_doc_in_demo
        self.use_shorter = use_shorter
        self.oracle_doc = oracle_doc

        self.head_prompt = None

    def generate_main_task_input(self, eval_item=None):
        if self.head_prompt is None:
            self.head_prompt = make_head_prompt(self.prompt_data,
                                                n_shot=self.n_shot,
                                                n_doc=self.n_doc,
                                                n_doc_in_demo=self.n_doc_in_demo,
                                                fewer_doc_in_demo=self.fewer_doc_in_demo,
                                                no_doc_in_demo=self.no_doc_in_demo,
                                                use_shorter=self.use_shorter, )

        text_input = self.head_prompt + make_demo(eval_item,
                                                  n_doc=self.n_doc,
                                                  template=self.prompt_data["demo_prompt"],
                                                  doc_prompt=self.prompt_data["doc_prompt"],
                                                  instruction=None,
                                                  use_shorter=self.use_shorter,
                                                  test=True,
                                                  oracle_doc=self.oracle_doc,)

        return text_input

    def generate_text_input(self, task_type="self_eval", dataset_name=None, **kwargs):
        dataset_name = dataset_name or self.dataset_name
        dataset_profile = DATASET_PROFILES[dataset_name] if dataset_name in DATASET_PROFILES else None
        if task_type == "main":
            assert "eval_item" in kwargs
            text_input = self.generate_main_task_input(eval_item=kwargs["eval_item"])
            if "chat" in self.model_name:
                text_input = text_input.rstrip("Answer:")


        elif task_type == "self_eval":
            assert "question" in kwargs and "answer" in kwargs

            text_input = TEMPLATES["self_eval_categorical_examples"].format(
                task_instruction=dataset_profile["eval_instruction"],
                criterion=dataset_profile["criterion"],
                examples=dataset_profile["eval_examples_categorical"],
                question=kwargs["question"],
                answer=kwargs["answer"],
            )
        elif task_type == "self_eval_doc":
            assert "eval_item" in kwargs and "question" in kwargs and "answer" in kwargs and "oracle_doc" in kwargs
            doc_prompt = "Document [{ID}](Title: {T}): {P}\n"
            doc_text = make_demo(kwargs["eval_item"], template="{D}\n",
                                 n_doc=self.n_doc, doc_prompt=doc_prompt,
                                 oracle_doc=kwargs["oracle_doc"], test=True)
            text_input = TEMPLATES["self_eval_categorical_examples_doc"].format(
                task_instruction=dataset_profile["eval_instruction"],
                criterion=dataset_profile["criterion"],
                examples=dataset_profile["eval_examples_categorical"],
                question=kwargs["question"],
                documents=doc_text,
                answer=kwargs["answer"],
            )


        elif task_type == "self_eval_range":
            assert "question" in kwargs and "answer" in kwargs

            text_input = TEMPLATES["self_eval_range"].format(
                task_instruction=dataset_profile["eval_instruction"],
                criterion=dataset_profile["criterion"],
                examples=dataset_profile["eval_examples_categorical"],
                question=kwargs["question"],
                answer=kwargs["answer"],
            )
        elif task_type == "eval":
            assert "question" in kwargs and "answer" in kwargs and "reference_answer" in kwargs
            text_input = TEMPLATES["eval_categorical_examples"].format(
                task_instruction=dataset_profile["eval_instruction"],
                criterion=dataset_profile["criterion"],
                examples=dataset_profile["eval_examples_categorical"],
                question=kwargs["question"],
                answer=kwargs["answer"],
                reference_answer=kwargs["reference_answer"],
            )
        elif task_type == "repetition":
            assert "question" in kwargs and "answer1" in kwargs and "answer2" in kwargs
            text_input = TEMPLATES["repetition"].format(
                question=kwargs["question"],
                answer1=kwargs["answer1"],
                answer2=kwargs["answer2"],
            )
        elif task_type == "repetition_split":
            assert "sentence" in kwargs and "response" in kwargs
            text_input = TEMPLATES["repetition_split"].format(
                sentence=kwargs["sentence"],
                response=kwargs["response"],
            )
        elif task_type == "choose_entities":
            assert "question" in kwargs and "entity_num" in kwargs
            text_input = TEMPLATES["choose_entities"].format(
                question=kwargs["question"],
                entity_num=kwargs["entity_num"],
            )
        elif task_type == "compare_questions":
            assert "question1" in kwargs and "question2" in kwargs
            text_input = TEMPLATES["compare_questions"].format(
                question1=kwargs["question1"],
                question2=kwargs["question2"],
            )
        elif task_type == "question_rephrase":
            assert "question" in kwargs and "rephrase_num" in kwargs
            text_input = TEMPLATES["question_rephrase"].format(
                question=kwargs["question"],
                rephrase_num=kwargs["rephrase_num"],
            )
        else:
            raise NotImplementedError

        if "chat" in self.model_name or self.model_name in ["5.0.1"]:
            text_input = TEMPLATES["llama2_chat"].format(task_instruction=text_input)

        return text_input