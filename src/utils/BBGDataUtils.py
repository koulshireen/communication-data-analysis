import os
import re
from fnmatch import fnmatch
from statistics import mean

import pandas as pd
from src.PreProcessing import pre_process_text
from src.StressScore import word_net_stress_score
from src.utils.DateTimeUtils import convert_string_date, off_working_hours_deviation
import logging as log

max_pos_score_weight = 1.5
max_neg_score_weight = 1.5


def load_data_for_bbg_model(file_path):
    log.info("-------BBG Parsing Initiated-------")
    col_names = ['File Name', 'From', 'Participants', 'Date', 'Text', 'Net Linguistic Stress Score',
                 'Max Pos Stress Score', 'Max Neg Stress Score', 'Off-Work Stress Score', 'Aggregated Stress Score']
    df = pd.DataFrame(columns=col_names)
    for path, subdirs, files in os.walk(file_path):
        for name in files:
            if fnmatch(name, "*.blm"):
                try:
                    chat_file = open(os.path.join(path, name), "r", encoding="mbcs")
                    reader = chat_file.read()
                    try:
                        from BeautifulSoup import BeautifulSoup
                    except ImportError:
                        from bs4 import BeautifulSoup
                    parsed_text = BeautifulSoup(reader, "lxml")
                    date_tag = re.findall(r'Date:+(.*)', parsed_text.body.p.getText())[0]
                    date = convert_string_date(date_tag)
                    from_tag = re.findall(r'Sender:+(.*)', parsed_text.body.p.getText())[0]
                    participants_tag = re.findall(r'Bcc:+(.*)', parsed_text.body.p.getText())[0] + ";" + from_tag
                    body_tag = re.findall(r'Content-Transfer-Encoding.*\n+(.*)', parsed_text.body.p.getText())[0]
                    cleaned_text = pre_process_text(body_tag)
                    net_linguistic_stress_score, max_pos_stress_score, max_neg_stress_score = word_net_stress_score(cleaned_text)
                    off_working_hours_score = off_working_hours_deviation(date)
                    if max_neg_stress_score != 0:
                        max_neg_stress_score = -max_neg_stress_score

                    weighted_max_pos_score = max_pos_score_weight * max_pos_stress_score
                    weighted_max_neg_score = max_neg_score_weight * max_neg_stress_score

                    if off_working_hours_score == 0:
                        aggregated_stress = mean([net_linguistic_stress_score, weighted_max_pos_score, weighted_max_neg_score])
                    else:
                        aggregated_stress = mean([net_linguistic_stress_score, weighted_max_pos_score, weighted_max_neg_score, off_working_hours_score])

                    df.loc[len(df)] = [name, from_tag, participants_tag, date, body_tag, net_linguistic_stress_score,
                                       max_pos_stress_score, max_neg_stress_score, off_working_hours_score,
                                       aggregated_stress]
                except Exception as e:
                    print(e)
                finally:
                    chat_file.close()
    log.info("-------BBG Parsing Finished-------")
    return df
