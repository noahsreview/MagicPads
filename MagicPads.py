import time
import launchpad_py as launchpad
import colour_logs
from launchpad_py import Launchpad
import logging
import argparse
import PadParse as parse
import TestMode as test

parser = argparse.ArgumentParser(description='MagicPads: a python script that is used to control MagicQ over OSC by using launchpads')
parser.add_argument('-t', "--test", required=False, default=False, type=bool, help='Testing Mode: will do various testing patterns on the launchpad')

args = parser.parse_args()

def main():
    # Try to open the Launchpad Pro
    lp = launchpad.LaunchpadPro()

    # Check and initialize the first available Launchpad
    if not lp.Open(0, "pad pro"):
        logging.critical("FAILED TO ESTABLISH A CONNECTION TO LAUNCHPAD PRO")
        return

    logging.info("Launchpad connected successfully! Please make sure to set it to live mode.")
    

    
    # Display an 8x8 PNG image on the central 8x8 grid
    parse.display_image_on_launchpad(lp, "your_image.png")  # Change "your_image.png" to your actual image file

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
    if(args.test):
        logging.warning("TEST MODE. THIS WILL TEST YOUR LAUNCHPAD")
        test.runTest()
    else:
        main()
