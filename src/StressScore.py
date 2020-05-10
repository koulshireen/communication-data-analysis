from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.corpus import wordnet as word_net, sentiwordnet as senti_word_net
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def convert_tree_bank_tag_to_word_net_tag(tree_bank_tag):
    first_char = tree_bank_tag[0]
    if first_char == 'J':
        return word_net.ADJ
    elif first_char == 'N':
        return word_net.NOUN
    elif first_char == 'R':
        return word_net.ADV
    elif first_char == 'V':
        return word_net.VERB
    return 'NA'


def word_net_stress_score(text):
    net_stress_score = 0.0
    max_pos_stress_score = 0.0
    max_neg_stress_score = 0.0
    no_of_tokens = 0
    sentences = sent_tokenize(text)

    for sentence in sentences:
        pos_tag_sentence = pos_tag(word_tokenize(sentence))
        for word, tree_bank_tag in pos_tag_sentence:
            word_net_tag = convert_tree_bank_tag_to_word_net_tag(tree_bank_tag)
            # if word_net_tag not in (word_net.NOUN, word_net.ADJ, word_net.ADV):
            #     continue
            # This commented line changes the stress score
            if word_net_tag not in (word_net.NOUN, word_net.ADJ, word_net.ADV, word_net.VERB):
                continue
            lemma = lemmatizer.lemmatize(word, pos=word_net_tag)
            if not lemma:
                continue

            synsets = word_net.synsets(lemma, pos=word_net_tag)
            if not synsets:
                continue

            # Generally the first sense from synset is most meaningful but can do some improvements here, might be good for score
            synset = synsets[0]
            senti_word_net_synset = senti_word_net.senti_synset(synset.name())
            max_pos_stress_score = max(max_pos_stress_score, senti_word_net_synset.pos_score())
            max_neg_stress_score = max(max_neg_stress_score, senti_word_net_synset.neg_score())
            net_score = senti_word_net_synset.pos_score() - senti_word_net_synset.neg_score()
            net_stress_score += net_score
            no_of_tokens += 1

    if not no_of_tokens:
        return 0.0

    return net_stress_score, max_pos_stress_score, max_neg_stress_score


def stress_score_group_by_participants(df):
    df = df[['Participants', 'Aggregated Stress Score']]
    df = df.loc[df['Aggregated Stress Score'] < 0].groupby(['Participants'], sort=True).sum()
    return df
