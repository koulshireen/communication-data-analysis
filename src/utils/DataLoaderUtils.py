from src.Prettify import prettify_output
from src.StressScore import stress_score_group_by_participants
from src.utils.BBGDataUtils import load_data_for_bbg_model
from src.utils.EmailDataUtils import load_email_files_data
from src.utils.HTMLDataUtils import load_html_files_data, CommType
import logging as log


# Change these files paths before starting execution
bbgFilePath = "C:\\Users\\15144\\PycharmProjects\\CommunicationsDataAnalysis\\testdata\\Communication_samples\\bbg"
chatsFilePath = "C:\\Users\\15144\\PycharmProjects\\CommunicationsDataAnalysis\\testdata\\Communication_samples\\chats"
emailsFilePath = "C:\\Users\\15144\\PycharmProjects\\CommunicationsDataAnalysis\\testdata\\Communication_samples\\emails"
patopaFilePath = "C:\\Users\\15144\\PycharmProjects\\CommunicationsDataAnalysis\\testdata\\Communication_samples\\patopa"
smsFilePath = "C:\\Users\\15144\\PycharmProjects\\CommunicationsDataAnalysis\\testdata\\Communication_samples\\sms"
reportsFilePath = "C:\\Users\\15144\\PycharmProjects\\CommunicationsDataAnalysis"
log.basicConfig(filename='log.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S',
                            level=log.INFO)

def load_data_set():
    log.info("-------BBG data analysis started-------")
    df_bbg = load_data_for_bbg_model(bbgFilePath)
    df_bbg_group_by_participants = stress_score_group_by_participants(df_bbg)
    log.info("-------BBG data analysis completed-------")

    log.info("-------Chat data analysis started-------")
    df_chat = load_html_files_data(chatsFilePath, CommType.chat)
    df_chat_group_by_participants = stress_score_group_by_participants(df_chat)
    log.info("-------Chat data analysis finished-------")

    log.info("-------SMS data analysis started-------")
    df_sms = load_html_files_data(smsFilePath, CommType.sms)
    df_sms_group_by_participants = stress_score_group_by_participants(df_sms)
    log.info("-------SMS data analysis finished-------")

    log.info("-------Email data analysis started-------")
    df_email = load_email_files_data(emailsFilePath)
    df_email_group_by_participants = stress_score_group_by_participants(df_email)
    log.info("-------Email data analysis finished-------")

    log.info("-------Patopa data analysis started-------")
    df_patopa = load_email_files_data(patopaFilePath)
    df_patopa_group_by_participants = stress_score_group_by_participants(df_patopa)
    log.info("-------Patopa data analysis finished-------")

    prettify_output(df_bbg, df_bbg_group_by_participants, df_chat, df_chat_group_by_participants, df_sms,
                    df_sms_group_by_participants, df_email, df_email_group_by_participants, df_patopa,
                    df_patopa_group_by_participants, reportsFilePath)

