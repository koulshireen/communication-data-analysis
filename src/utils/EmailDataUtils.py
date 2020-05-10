import email
import os
from fnmatch import fnmatch
from statistics import mean

import pandas as pd

from src.PreProcessing import pre_process_text
from src.StressScore import word_net_stress_score
from src.utils.DateTimeUtils import convert_string_date, off_working_hours_deviation
import logging as log

max_pos_score_weight = 1.5
max_neg_score_weight = 1.5

def load_email_files_data(file_path):
    log.info("-------Email Parsing Initiated-------")
    col_names = ['File Name', 'Participants', 'To', 'Date', 'Text', 'Net Linguistic Stress Score',
                 'Max Pos Stress Score', 'Max Neg Stress Score', 'Off-Work Stress Score',
                 'Aggregated Stress Score']
    df = pd.DataFrame(columns=col_names)
    for path, subdirs, files in os.walk(file_path):
        for name in files:
            if fnmatch(name, "*.eml"):
                try:
                    chat_file = open(os.path.join(path, name), "r", encoding="mbcs")
                    email_msg = email.message_from_file(chat_file)
                    if email_msg.is_multipart():
                        for payload in email_msg.get_payload():
                            from_tag = payload.get("From")
                            to_tag = payload.get("To")
                            body_tag = payload.get_payload()
                            date_tag = payload.get("Date")
                    else:
                        from_tag = email_msg.get("From")
                        to_tag = email_msg.get("To")
                        body_tag = email_msg.get_payload()
                        date_tag = email_msg.get("Date")
                    cleaned_text = pre_process_text(body_tag)
                    date = convert_string_date(date_tag)
                    try:
                        net_linguistic_stress_score, max_pos_stress_score, max_neg_stress_score = word_net_stress_score(cleaned_text)
                    except TypeError:
                        net_linguistic_stress_score, max_pos_stress_score, max_neg_stress_score = 0, 0, 0
                    off_working_hours_score = off_working_hours_deviation(date)

                    if max_neg_stress_score != 0:
                        max_neg_stress_score = -max_neg_stress_score

                    weighted_max_pos_score = max_pos_score_weight * max_pos_stress_score
                    weighted_max_neg_score = max_neg_score_weight * max_neg_stress_score

                    if off_working_hours_score == 0:
                        aggregated_stress = mean([net_linguistic_stress_score, weighted_max_pos_score,
                                                  weighted_max_neg_score])
                    else:
                        aggregated_stress = mean(
                            [net_linguistic_stress_score, weighted_max_pos_score, weighted_max_neg_score,
                             off_working_hours_score])

                    participants_tag = ';'.join([p for p in (from_tag, to_tag) if p])
                    dirname = path.split(os.path.sep)[-1] + "//" + name
                    df.loc[len(df)] = [dirname, participants_tag, to_tag, date, cleaned_text,
                                       net_linguistic_stress_score, max_pos_stress_score, max_neg_stress_score,
                                       off_working_hours_score, aggregated_stress]
                except Exception as e:
                    print()
                finally:
                    chat_file.close()
    log.info("-------Email Parsing Finished-------")
    return df
