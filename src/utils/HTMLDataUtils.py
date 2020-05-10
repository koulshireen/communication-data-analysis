import enum
import os
from fnmatch import fnmatch

import pandas as pd

from src.PreProcessing import pre_process_text
from src.StressScore import word_net_stress_score
from src.utils.DateTimeUtils import convert_string_date, off_working_hours_deviation


class CommType(enum.Enum):
    sms = 1
    chat = 2


def load_html_files_data(file_path, comm_type):
    col_names = ['File Name', 'From', 'Participants', 'Date', 'Text', 'Net Linguistic Stress Score',
                 'Max Pos Stress Score', 'Max Neg Stress Score', 'Off-Work Stress Score', 'Aggregated Stress Score']
    df = pd.DataFrame(columns=col_names)
    for path, subdirs, files in os.walk(file_path):
        for name in files:
            if fnmatch(name, "*.html"):
                try:
                    chat_file = open(os.path.join(path, name), "r", encoding="mbcs")
                    reader = chat_file.read()
                    try:
                        from BeautifulSoup import BeautifulSoup
                    except ImportError:
                        from bs4 import BeautifulSoup
                    parsed_html = BeautifulSoup(reader, "html.parser")
                    if comm_type == CommType.chat:
                        text_tags = parsed_html.body.findAll('div', attrs={'class': 'text'})
                        body_tag = ""
                        for text_tag in text_tags:
                            body_tag += text_tag.text
                        from_tag = parsed_html.body.find('span', attrs={'class': 'author'}).text
                        # Not complete participants_tag
                        participants_tag = parsed_html.body.find('div', attrs={'class': 'participants'}).find('span',
                                                                                                              attrs={
                                                                                                                  'class': 'person'}).next_sibling.next_sibling.text + " ; " + from_tag
                        date_tag = parsed_html.body.find('span', attrs={'class': 'date'}).text
                    if comm_type == CommType.sms:
                        text_tags = parsed_html.body.findAll('div', attrs={'class': 'text'})
                        body_tag = ""
                        for text_tag in text_tags:
                            body_tag += text_tag.text
                        from_tag = parsed_html.body.find('div', attrs={
                            'class': 'content'}).b.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
                        participants_tag = parsed_html.body.find('span',
                                                                 attrs={'class': 'contact'}).text + ";" + from_tag
                        date_tag = parsed_html.body.find('div', attrs={'class': 'content'}).b.next_sibling
                    cleaned_text = pre_process_text(body_tag)
                    date = convert_string_date(date_tag)
                    net_linguistic_stress_score, max_pos_stress_score, max_neg_stress_score = word_net_stress_score(cleaned_text)
                    off_working_hours_score = off_working_hours_deviation(date)
                    aggregated_stress = net_linguistic_stress_score if off_working_hours_score == 0 else (
                                                                                                             off_working_hours_score + net_linguistic_stress_score) / 2.0
                    df.loc[len(df)] = [name, from_tag, participants_tag, date, body_tag, net_linguistic_stress_score,
                                       max_pos_stress_score, max_neg_stress_score, off_working_hours_score, aggregated_stress]
                except Exception as e:
                    print(e)
                finally:
                    chat_file.close()
    return df
