import time
import launchpad_py as launchpad

from launchpad_py import Launchpad
import logging
import argparse
import MagicPadsFiles.PadParse as parse
import MagicPadsFiles.TestMode as test
import MagicPadsFiles.colour_logs
import MagicPadsFiles.osc as oscManager

import configparser
from pygame import time as t

parser = argparse.ArgumentParser(description='MagicPads: a python script that is used to control MagicQ over OSC by using launchpads')
parser.add_argument('-t', "--test", required=False, default=False, type=bool, help='Testing Mode: will do various testing patterns on the launchpad')

args = parser.parse_args()

def create_config():
    config = configparser.ConfigParser()

    config['General'] = {'debug': True, 'log_level': 'info'}
    config['Networking & Chamsys Settings'] = {'TX_OSC_Port': '8000',
                                               'OSC_IP' : '127.0.0.1',
                                                'Executor_Page' : "3"  }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    debug_mode = config.getboolean('General', 'debug')
    log_level = config.get('General', 'log_level')
    tx_osc_port =  config.getint('Networking & Chamsys Settings', 'tx_osc_port')
    osc_ip =  config.get('Networking & Chamsys Settings', 'osc_ip')
    executor_page =  config.get('Networking & Chamsys Settings', 'executor_page')

    config_values = {
        'debug_mode' : debug_mode,
        'log_level' : log_level,
        'tx_osc_port' : tx_osc_port,
        'osc_ip' : osc_ip,
        'executor_page' : executor_page
    }

    return config_values

def main():
    # Try to open the Launchpad Pro
    lp = launchpad.LaunchpadPro()

    # Check and initialize the first available Launchpad
    if not lp.Open(0, "pad pro"):
        logging.critical("FAILED TO ESTABLISH A CONNECTION TO LAUNCHPAD PRO")
        return

    logging.info("Launchpad connected successfully! Please make sure to set it to live mode.")
    

    
    # Display an 8x8 PNG image on the central 8x8 grid
    oscManager.sendOSC(3, 1)
    parse.display_image_on_launchpad(lp, "images/N.png")  # Change "your_image.png" to your actual image file
    t.wait(1000)
    parse.display_image_on_launchpad(lp, "images/P.png")  # Change "your_image.png" to your actual image file
    t.wait(1000)
    parse.display_image_on_launchpad(lp, "images/L.png")  # Change "your_image.png" to your actual image file
    t.wait(1000)
    parse.display_image_on_launchpad(lp, "images/X.png")  # Change "your_image.png" to your actual image file
    t.wait(2500)
    parse.display_image_on_launchpad(lp, "your_image.png")


    try:
        print("\nListening for button presses...")

        while True:
            # Get the button state using ButtonStateXY()
            button_state = lp.ButtonStateXY()

            # Parse and react to button press
            parse.parse_button_press(button_state, lp)

    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        # Reset and close the Launchpad
        lp.Reset()
        lp.Close()
        print("Launchpad closed.")





    
    


if __name__ == "__main__":
    config_data = read_config()
    """ oscManager.ping() """
    parse.receive_OSC_Info(config_data["osc_ip"], config_data["tx_osc_port"], config_data["executor_page"])
    
    
    if(args.test):
        logging.warning("TEST MODE. THIS WILL TEST YOUR LAUNCHPAD")
        test.runTest()
    else:
        main()