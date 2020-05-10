from tabulate import tabulate
import matplotlib.pyplot as plt


def prettify_output(df_bbg, df_bbg_group_by_participants, df_chat, df_chat_group_by_participants, df_sms,
                    df_sms_group_by_participants, df_email, df_email_group_by_participants, df_patopa,
                    df_patopa_group_by_participants, reportsFilePath):
    reports_file = open(reportsFilePath + "//stress_score_report.txt", "w")

    reports_file.write(
        "***************************************************  BBG Communications Data Report *************************************************** ")
    generate_report(df_bbg[['File Name', 'Date', 'Participants', 'Net Linguistic Stress Score', 'Max Pos Stress Score',
                            'Max Neg Stress Score', 'Off-Work Stress Score', 'Aggregated Stress Score']], reports_file)
    generate_report(df_bbg_group_by_participants, reports_file)
    plotGraph(df_bbg, reportsFilePath + "//bbg_graph.png")

    reports_file.write(
        "***************************************************  Chat Communications Data Report *************************************************** ")
    generate_report(df_chat[['File Name', 'Date', 'Participants', 'Net Linguistic Stress Score', 'Max Pos Stress Score',
                             'Max Neg Stress Score', 'Off-Work Stress Score', 'Aggregated Stress Score']], reports_file)
    generate_report(df_chat_group_by_participants, reports_file)
    plotGraph(df_chat, reportsFilePath + "//chat_graph.png")


    reports_file.write(
        "***************************************************  SMS Communications Data Report *************************************************** ")
    generate_report(df_sms[['File Name', 'Date', 'Participants', 'Net Linguistic Stress Score', 'Max Pos Stress Score',
                            'Max Neg Stress Score', 'Off-Work Stress Score', 'Aggregated Stress Score']], reports_file)
    generate_report(df_sms_group_by_participants, reports_file)
    plotGraph(df_sms, reportsFilePath + "//sms_graph.png")


    reports_file.write(
        "*************************************************** Patopa Communications Data Report *************************************************** ")
    generate_report(
        df_patopa[['File Name', 'Date', 'Participants', 'Net Linguistic Stress Score', 'Max Pos Stress Score',
                   'Max Neg Stress Score', 'Off-Work Stress Score', 'Aggregated Stress Score']], reports_file)
    generate_report(df_patopa_group_by_participants, reports_file)
    plotGraph(df_patopa, reportsFilePath + "//patopa_graph.png")


    reports_file.write(
        "*************************************************** EMAIL Communications Data Report *************************************************** ")
    generate_report(
        df_email[['File Name', 'Date', 'Participants', 'Net Linguistic Stress Score', 'Max Pos Stress Score',
                  'Max Neg Stress Score', 'Off-Work Stress Score', 'Aggregated Stress Score']], reports_file)
    generate_report(df_email_group_by_participants, reports_file)
    plotGraph(df_email, reportsFilePath + "//email_graph.png")



def generate_report(df, file):
    df_tabulate = lambda df: tabulate(df, headers='keys', tablefmt='grid', stralign='left')
    file.write("\n\n")
    file.write(df_tabulate(df))
    file.write("\n\n\n")


def plotGraph(df, graphFilePath):
    fig, graph = plt.subplots()
    graph.plot(df["File Name"], df["Net Linguistic Stress Score"], marker="o")
    graph.set_xlabel("File Name")
    graph.axes.get_xaxis().set_visible(False)
    graph.set_ylabel("Net stress")
    graph.plot(df["File Name"], df["Off-Work Stress Score"], marker="o")
    plt.savefig(graphFilePath)
    graph.axes.get_xaxis().set_visible(False)

