import re
import json
import pandas as pd
from sklearn.model_selection import train_test_split

def unique_glosses_extraction():
    df = pd.read_csv("data\\sign_language_corpus\\annotations.csv", sep="\t")
    glosses = list(set(df["text"]))

    daktyl = ["Й", "Ц", "У", "К", "Е",
          "Н", "Г", "Ш", "Щ", "З",
          "Х", "Ъ", "Ф", "Ы", "В",
          "А", "П", "Р", "О", "Л", 
          "Д", "Ж", "Э", "Я", "Ч",
          "С", "М", "И", "Т", "Ь", 
          "Б", "Ю", "Ё"]

    glosses = sorted([re.sub(r"[^а-яa-zё\s\d-]", "", gloss.lower()) for gloss in glosses if gloss not in daktyl and gloss != "no_event"])

    glosses_one_word = [gloss for gloss in glosses if len(gloss.split())==1]
    glosses_several_words = [gloss for gloss in glosses if len(gloss.split())>1]

    with open("data\\sign_language_corpus\\unique_glosses_one_word.txt", "wt", encoding="utf-8") as file:
        for gloss in glosses_one_word:
            file.write(gloss)
            file.write("\n")
    
    with open("data\\sign_language_corpus\\unique_glosses_several_words.txt", "wt", encoding="utf-8") as file:
        for gloss in glosses_several_words:
            file.write(gloss)
            file.write("\n")

def checking_extra_words():
    with open("data\\gloss_sentences_corpus\\sentences.txt", "rt", encoding="utf-8") as file:
        sentences_all = file.read().replace("\n", " ")
    
    with open("data\\sign_language_corpus\\unique_glosses_one_word.txt", "rt", encoding="utf-8") as file:
        unique_glosses_several_words = [item.replace("\n", "") for item in file.readlines()]
    
    with open("data\\sign_language_corpus\\unique_glosses_several_words.txt", "rt", encoding="utf-8") as file:
        unique_glosses_one_word = [item.replace("\n", "") for item in file.readlines()]

    for unique_gloss in unique_glosses_several_words:
        if unique_gloss in sentences_all:
            start_points = [item.start() for item in re.finditer(unique_gloss, sentences_all)]
            end_points = [item.end() for item in re.finditer(unique_gloss, sentences_all)]

            for i in range(len(start_points)):
                if i == 0:
                    sentences_all = sentences_all[0:start_points[i]] + sentences_all[end_points[i]:len(sentences_all)]
                else:
                    sentences_all = sentences_all[0:start_points[i]-len(unique_gloss)] + sentences_all[end_points[i]-len(unique_gloss):len(sentences_all)]
    
    extra_words = [token for token in sentences_all.split() if token not in unique_glosses_one_word]
    print("Слова, которых нет в корпусе ", extra_words)
    
def checking_all_glosses():
    with open("data\\gloss_sentences_corpus\\sentences.txt", "rt", encoding="utf-8") as file:
        sentences = file.read()
    
    with open("data\\sign_language_corpus\\unique_glosses_one_word.txt", "rt", encoding="utf-8") as file:
        unique_glosses_several_words = [item.replace("\n", "") for item in file.readlines()]
    
    with open("data\\sign_language_corpus\\unique_glosses_several_words.txt", "rt", encoding="utf-8") as file:
        unique_glosses_one_word = [item.replace("\n", "") for item in file.readlines()]
    
    glosses_in, glosses_out = [], []
    for gloss in unique_glosses_one_word:
        if gloss in sentences:
            glosses_in.append(gloss)
        else:
            glosses_out.append(gloss)
    for gloss in unique_glosses_several_words:
        if gloss in sentences:
            glosses_in.append(gloss)
        else:
            glosses_out.append(gloss)

    glosses_in, glosses_out = sorted(glosses_in), sorted(glosses_out)
    print("Использованные глоссы из корпуса ", glosses_in)
    print("Количество использованных глосс ", len(glosses_in))
    print("Неиспользованные глоссы из корпуса ", glosses_out)
    print("Количество неиспользованных глосс ", len(glosses_out))

def pos_tagged():
    with open("pos.json", "rt", encoding="utf-8") as file:
        pos_dict = json.load(file)

    S_tags = ["имя собственное", "существительное", 
              "местоимение", "числительное"]
    V_tags = ["глагол"]
    ADV_tags = ["наречие"]
    ATTR_tags = ["прилагательное", "причастие"]
    functional_tags = ["союз", "предлог", "частица"]

    S_glosses, V_glosses, ADV_glosses, ATTR_glosses, functional_glosses = [], [], [], [], []
              
    for pos in pos_dict:
        if pos_dict[pos] in S_tags:
            S_glosses.append(pos)
        elif pos_dict[pos] in V_tags:
            V_glosses.append(pos)
        elif pos_dict[pos] in ADV_tags:
            ADV_glosses.append(pos)
        elif pos_dict[pos] in ATTR_tags:
            ATTR_glosses.append(pos)
        elif pos_dict[pos] in functional_tags:
            functional_glosses.append(pos)

    stat = {
        "S (подлежащее):": S_glosses,
        "V (сказуемое)": V_glosses,
        "ATTR (определение)": ATTR_glosses,
        "ADV (обстоятельство)": ADV_glosses,
        "functional (служебные части речи)": functional_glosses,
    }

    len_stat = {
        "S (подлежащее):":len(S_glosses),
        "V (сказуемое)": len(V_glosses),
        "ATTR (определение)": len(ATTR_glosses),
        "ADV (обстоятельство)": len(ADV_glosses),
        "functional (служебные части речи)": len(functional_glosses),
    }
    return stat, len_stat, sum(len_stat.values())

def corpus_checking_non_cyrillic():
    with open("data\\parallel_corpus\\corpus.json", "rt", encoding="utf-8") as file:
        dict_file = json.loads(file.read())
    sentences = list(dict_file.keys())
    extra_symbols = [re.findall(r"[^А-Яа-яёЁ\d\s\.,:;\!\?—-]", sentence) for sentence in sentences]
    extra_symbols = [sentence for sentence in extra_symbols if len(sentence)!=0]
    print("Некириллические символы ", extra_symbols)

def coprus_checking_all_sentences():
    with open("data\\parallel_corpus\\corpus.json", "rt", encoding="utf-8") as file:
        dict_file = json.loads(file.read())
    sentences_llm = list(set(dict_file.values()))
    
    with open("data\\gloss_sentences_corpus\\sentences.txt", "rt", encoding="utf-8") as file:
        sentences_target = [sentence.replace("\n", "") for sentence in file.readlines()]
    no_sentences = [sentence.strip() for sentence in sentences_target if sentence.strip() not in sentences_llm and len(sentence.strip())!=0]
    print("Неиспользованные предложения ", no_sentences)
    print("Количество неиспользованных предложений ", len(no_sentences))

def dataset_convertion():
    with open("data\\parallel_corpus\\corpus.json", "rt", encoding="utf-8") as file:
        corpus = json.load(file)
    corpus_hf = [{"russian": key, "rsl": value} for key, value in corpus.items()]
    X = [item["russian"] for item in corpus_hf]
    y = [item["rsl"] for item in corpus_hf]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
    train_sample = [{"russian": X_train[i], "rsl": y_train[i]} for i in range(len(X_train))]
    test_sample = [{"russian": X_test[i], "rsl": y_test[i]} for i in range(len(X_test))]
    
    with open("corpus_train_hf.json", "wt", encoding="utf-8") as file:
        json.dump(train_sample, file, ensure_ascii=False, indent=2)
    
    with open("corpus_test_hf.json", "wt", encoding="utf-8") as file:
        json.dump(test_sample, file, ensure_ascii=False, indent=2)