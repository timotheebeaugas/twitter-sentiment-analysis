# -*- coding: utf8 -*-
import schedule, time, wordsRanking, twitterSteam, sentimentsAnalysis, os, threading

while True:
    try:
        # stream launch for retrieve live tweet 24/7
        th1 = threading.Thread(target=twitterSteam.startStream)

        # CRON for trigger word counting and opinion mining every days
        schedule.every().days.at('00:01').do(sentimentsAnalysis.saveSentiments)
        schedule.every().days.at('00:01').do(wordsRanking.saveData)

        th1.start()
        
        # check date every seconds
        while True:
            th2 = threading.Thread(target=schedule.run_pending())
            th2.start()
            time.sleep(1)

    # restart python file
    except:
        os.system("script.py")


