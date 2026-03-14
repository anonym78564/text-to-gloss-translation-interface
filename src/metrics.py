from nltk.translate.bleu_score import corpus_bleu, SmoothingFunction
from datasets import load_dataset

# nltk.download("popular")

dataset = load_dataset("Arseney/parallel_corpus_russian_rsl_glosses")
target_data = [[item["rsl"].split()] for item in dataset["test"]]
smooth = SmoothingFunction().method1

with open("translated_sentences\\nllb.txt", "rt", encoding="utf-8") as file:
    hypotheses = [item.replace("\n", "").split() for item in file.readlines()]

bleu_scores = {
    "bleu_1": corpus_bleu(hypotheses=hypotheses, 
                list_of_references=target_data, 
                smoothing_function=smooth,
                weights=(1, 0, 0, 0)),
    "bleu_2": corpus_bleu(hypotheses=hypotheses, 
                list_of_references=target_data, 
                smoothing_function=smooth,
                weights=(0, 1, 0, 0)),
    "bleu_3": corpus_bleu(hypotheses=hypotheses, 
                list_of_references=target_data, 
                smoothing_function=smooth,
                weights=(0, 0, 1, 0)),
    "bleu_4": corpus_bleu(hypotheses=hypotheses, 
                list_of_references=target_data, 
                smoothing_function=smooth,
                weights=(0, 0, 0, 1))
}

print(bleu_scores)