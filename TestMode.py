import logging
import coloredlogs
from pygame import time
import examples.launchpad_pro
import launchpad_py
import examples

def runTest():
    logging.warning("Are you sure you wish to run tests? Press CTRL + C to cancel test or press enter to continue.")
    answer = input("")
    examples.launchpad_pro.main()
    
    
        
    