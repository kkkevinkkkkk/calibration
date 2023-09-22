import logging
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


def get_prompt(eval_item, dataset_name="asqa", ndoc=5):
    template = templates[dataset_name]
    if dataset_name == "asqa":
        question = eval_item["ambiguous_question"]
        prompt = template.format(question=question)
    elif dataset_name == "eli5":
        question = eval_item["question"]
        doc_list = get_shorter_text(eval_item, eval_item["docs"], ndoc, "summary")
        inline_doc = "".join([make_doc_prompt(doc_list[doc_id], doc_id, doc_prompt) for doc_id in range(len(doc_list))])
        prompt = template.format(documents=inline_doc, question=question)
    else:
        raise Exception

    return prompt


