import logging
import numpy as np
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


template_asqa = '''<s>[INST] <<SYS>>
    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
    
    You will be given an ambiguous factoid question which have different correct answers depneding on interpretation. Your answer should synthesize factual information from multiple sources into a long-form summary that resolves the ambiguity.
    <</SYS>>
    
    Question: {question} [/INST]'''

template_eli5 = '''<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
<</SYS>>

You will be given a question and you need to provide an answer which is comprehensible by five year olds. You will also have some web documents for reference

Documents: {documents}
Question: {question} [/INST]'''
templates = {"asqa": template_asqa, "eli5": template_eli5}
doc_prompt = "Document [{ID}](Title: {T}): {P}\n"

def make_doc_prompt(doc, doc_id, doc_prompt, use_shorter=None):
    # For doc prompt:
    # - {ID}: doc id (starting from 1)
    # - {T}: title
    # - {P}: text
    # use_shorter: None, "summary", or "extraction"

    text = doc['text']
    if use_shorter is not None:
        text = doc[use_shorter]
    return doc_prompt.replace("{T}", doc["title"]).replace("{P}", text).replace("{ID}", str(doc_id+1))

def get_shorter_text(item, docs, ndoc, key):
    doc_list = []
    for item_id, item in enumerate(docs):
        if key not in item:
            if len(doc_list) == 0:
                # If there aren't any document, at least provide one (using full text)
                item[key] = item['text']
                doc_list.append(item)
            logger.warning(f"No {key} found in document. It could be this data do not contain {key} or previous documents are not relevant. This is document {item_id}. This question will only have {len(doc_list)} documents.")
            break
        if "irrelevant" in item[key] or "Irrelevant" in item[key]:
            continue
        doc_list.append(item)
        if len(doc_list) >= ndoc:
            break
    return doc_list


def make_chat_prompt(eval_item, dataset_name="asqa", ndoc=5):
    template = templates[dataset_name]
    if dataset_name == "asqa":
        question = eval_item["question"]
        prompt = template.format(question=question)
    elif dataset_name == "eli5":
        question = eval_item["question"]
        doc_list = get_shorter_text(eval_item, eval_item["docs"], ndoc, "summary")
        inline_doc = "".join([make_doc_prompt(doc_list[doc_id], doc_id, doc_prompt) for doc_id in range(len(doc_list))])
        prompt = template.format(documents=inline_doc, question=question)
    else:
        raise Exception

    return prompt


def make_demo(item, template,
              ndoc=None,
              doc_prompt=None,
              instruction=None,
              use_shorter=None,
              test=False):
    # For demo template
    # - {INST}: the instruction
    # - {D}: the documents
    # - {Q}: the question
    # - {A}: the answers
    # ndoc: number of documents to put in context
    # use_shorter: None, "summary", or "extraction"

    if instruction is None:
        prompt = template.replace('{INST}\n\n', "")
        prompt = prompt.replace("{Q}", item['question'])
    else:
        prompt = template.replace("{INST}", instruction).replace("{Q}", item['question'])
    if "{D}" in prompt:
        if ndoc == 0:
            prompt = prompt.replace("{D}\n", "") # if there is no doc we also delete the empty line
        else:
            doc_list = get_shorter_text(item, item["docs"], ndoc, use_shorter) if use_shorter is not None else item["docs"][:ndoc]
            text = "".join([make_doc_prompt(doc, doc_id, doc_prompt, use_shorter=use_shorter) for doc_id, doc in enumerate(doc_list)])
            prompt = prompt.replace("{D}", text)

    if not test:
        answer = "\n" + "\n".join(item["answer"]) if isinstance(item["answer"], list) else item["answer"]
        prompt = prompt.replace("{A}", "").rstrip() + answer
    else:
        prompt = prompt.replace("{A}", "").rstrip() # remove any space or \n

    return prompt


def make_head_prompt(prompt_data: dict,
                     n_shot: int = 0,
                     n_doc: int = 0,
                     n_doc_in_demo: int = 0,
                     fewer_doc_in_demo: bool = False,
                     no_doc_in_demo: bool = True,
                     use_shorter: str = "summary",
                     ):
    train_ids = np.random.choice(len(prompt_data["demos"]), n_shot, replace=False)
    head_prompt = prompt_data["instruction"]
    if n_shot > 0:
        head_prompt += "Here are some examples:\n\n"

    for train_id in train_ids:
        train_item = prompt_data["demos"][train_id]
        n_doc = n_doc
        if no_doc_in_demo:
            n_doc = 0
        elif fewer_doc_in_demo:
            assert n_doc_in_demo is not None
            n_doc = n_doc_in_demo
        head_prompt += make_demo(
            train_item, template=prompt_data["demo_prompt"], ndoc=n_doc, doc_prompt=prompt_data["doc_prompt"],
            instruction=None, use_shorter=use_shorter
        )
        head_prompt += prompt_data["demo_sep"]

    head_prompt += "Now let's answer:\n\n"
    return head_prompt

def make_text_input(
        eval_item: dict,
        head_prompt: str = None,
        model_name: str = "llama-7b-hf",
        n_doc: int = 0,
        template: str = None,
        doc_prompt: str = None,
        instruction: str = None,
        use_shorter: str = "summary",
        test: bool = True,
        dataset_name: str = "asqa",
                ):
    if "chat" in model_name:
        text_input = make_chat_prompt(eval_item, dataset_name, ndoc=n_doc)
    else:
        text_input = head_prompt + make_demo(
            eval_item,
            template=template,
            ndoc=n_doc,
            doc_prompt=doc_prompt,
            instruction=None,
            use_shorter=use_shorter,
            test=True
        )
    return text_input



