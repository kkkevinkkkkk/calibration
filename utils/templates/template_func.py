
def fit_content(template, examples=None, criterion=None, task_instruction=None):
    if examples:
        template = template.replace("{examples}", examples)
    if criterion:
        template = template.replace("{criterion}", criterion)
    if task_instruction:
        template = template.replace("{task_instruction}", task_instruction)
    return template