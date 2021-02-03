# -*- coding: utf8 -*-
import schedule, time, wordsRanking, twitterSteam, sentimentsAnalysis, os, threading


while True:
    try:
        # stream launch for retrieve live tweet 24/7
        threading.Thread(target=twitterSteam.startStream).start()

        # CRON for trigger word counting and opinion mining every days
        
        threading.Thread(target=schedule.every().days.at('00:03').do(sentimentsAnalysis.saveSentiments)).start()
        threading.Thread(target=schedule.every().days.at('00:03').do(wordsRanking.saveData)).start()
        
        # check date every seconds
        while True:
            schedule.run_pending()
            time.sleep(1)
    # restart python file
    except:
        os.system("script.py")


