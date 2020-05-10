import email
import os
from fnmatch import fnmatch

import pandas as pd

from src.PreProcessing import pre_process_text
from src.StressScore import word_net_stress_score
from src.utils.DateTimeUtils import convert_string_date, off_working_hours_deviation


def load_email_files_data(file_path):
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
                    net_linguistic_stress_score, max_pos_stress_score, max_neg_stress_score = word_net_stress_score(
                        cleaned_text)
                    off_working_hours_score = off_working_hours_deviation(date)
                    aggregated_stress = net_linguistic_stress_score if off_working_hours_score == 0 else (
                                                                                                                 off_working_hours_score + net_linguistic_stress_score) / 2.0
                    participants_tag = ';'.join([p for p in (from_tag, to_tag) if p])
                    dirname = path.split(os.path.sep)[-1] + "//" + name
                    df.loc[len(df)] = [dirname, participants_tag, to_tag, date, cleaned_text,
                                       net_linguistic_stress_score, max_pos_stress_score, max_neg_stress_score,
                                       off_working_hours_score, aggregated_stress]
                except Exception as e:
                    print(e)
                finally:
                    chat_file.close()
    return df
