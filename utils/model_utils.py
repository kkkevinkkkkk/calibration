from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
from span_marker import SpanMarkerModel
from collections import defaultdict

class NERModel:
    # options for model_name:
    # - Babelscape/wikineural-multilingual-ner
    # - tomaarsen/span-marker-roberta-large-ontonotes5
    def __init__(self,
                 model_name="tomaarsen/span-marker-roberta-large-ontonotes5"):

        self.model_name = model_name
        if model_name == "Babelscape/wikineural-multilingual-ner":
            self.tokenizer_name = model_name
        else:
            self.tokenizer_name = None
        if "span-marker" in model_name:
            self.model = SpanMarkerModel.from_pretrained(model_name)
            self.model.cuda()
        else:
            model = AutoModelForTokenClassification.from_pretrained(self.model_name)
            tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_name)
            self.model = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)

        self.entity_groups = {
            "CARDINAL": "Cardinal value",
            "DATE": "Date and times",
            "EVENT": "Event name",
            "FAC": "Building name",
            "GPE": "Geo-political entity",
            "LANGUAGE": "Language name",
            "LAW": "Law name",
            "LOC": "Location name",
            "MONEY": "Monetary value",
            "NORP": "Affiliation",
            "ORDINAL": "Ordinal value",
            "ORG": "Organization name",
            "PERCENT": "Percentage",
            "PERSON": "Person name",
            "PRODUCT": "Product name",
            "QUANTITY": "Quantity value",
            "TIME": "Time value",
            "WORK_OF_ART": "Work of art name",
        }
        self.meaning_to_group = {v: k for k, v in self.entity_groups.items()}

    @staticmethod
    def map_entities(entities):
        new_entities = []
        for entity in entities:
            new_entities.append(
                {
                    'entity_group': entity['label'],
                    'score': entity["score"],
                    "word": entity["span"],
                    'start': entity['char_start_index'],
                    'end': entity['char_end_index'],
                }
            )
            if entity['label'] in ["CARDINAL", "QUANTITY"]:
                new_label = "QUANTITY" if entity['label'] == "CARDINAL" else "CARDINAL"
                new_entities.append(
                    {
                        'entity_group': new_label,
                        'score': entity["score"],
                        "word": entity["span"],
                        'start': entity['char_start_index'],
                        'end': entity['char_end_index'],
                    }
                )
        return new_entities

    def extract_chosen_entities(self, chosen_entities_text):
        chosen_entities_text = chosen_entities_text.lower()
        entity_groups = []
        for k, v in self.entity_groups.items():
            if v.lower() in chosen_entities_text:
                entity_groups.append(k)
        return entity_groups

    def __call__(self, text, *args, **kwargs):
        if "span-marker" in self.model_name:
            entites = self.model.predict(text)
            return self.map_entities(entites)
        else:
            return self.model(text, *args, **kwargs)

    def get_entities_dict(self, text):
        entities_dict = defaultdict(set)
        entities = self.__call__(text)
        for entity in entities:
            entities_dict[entity["entity_group"]].add(entity["word"].lower())

        return entities_dict