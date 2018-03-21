from Classes import Run_All_web
from Classes import Run_All_Not_Web


def start():
    run_all_scrapes = Run_All_web.RunAll()
    run_all_scrapes.run()


start()
