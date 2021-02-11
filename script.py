# -*- coding: utf8 -*-
import time, schedule, wordsRanking, sentimentsAnalysis

try:

    # CRON for trigger word counting and opinion mining every days
    schedule.every().day.at("23:58").do(sentimentsAnalysis.saveSentiments)
    schedule.every().day.at("23:59").do(wordsRanking.saveData)

    while True:
        schedule.run_pending()
        time.sleep(1)

# print error
except Exception as e:
    print(e)


