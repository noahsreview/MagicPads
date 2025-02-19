import pygame
import launchpad_py as launchpad
from launchpad_py import Launchpad
import colour_logs as colour_log
import random
import logging


def send_led_message(lp, x, y, pressed):
    """Send a message to control LEDs based on button press (True) or release (False)"""
    print(f"Sending LED control for button at ({x}, {y}) with pressed state: {pressed}")
    colors = [ [63,63,0],[0,63,0],[0,25,63],[63,63,0],[63,0,63],[0,63,63],[63,63,63] ]
    if(pressed):
        for i in range(5):
            lp.LedCtrlXY( x+1, y, 255, 0, 0, mode = "pro" )
                    
            
    
    else:
        lp.LedCtrlXY( x+1, y, 0, 0, 0, mode = "pro" )
                    
def parse_button_press(listBut, lp):
    if(len(listBut) > 0):
        x,y,vel = listBut
        if(vel > 0):
            print("valid button press at coord: ", x, y, " with a vel of :", vel);   
            send_led_message(lp, x, y, True)
        else:
            send_led_message(lp, x, y, False)
    else:
        return
    
    
    

def main():
    # Try to open any Launchpad model
    lp = launchpad.LaunchpadPro()
    
    # Check and initialize the first available Launchpad
    if not lp.Open(0, "pad pro"):
        logging.critical("FAILED TO ESTABLISH A CONNECTION TO LAUNCHPAD PRO")
        return

    print("Launchpad connected successfully! Please Make sure to set it to live")
   
    try:
        print("\nListening for button presses...")

        while True:
            # Get the button state using ButtonStateXY()
            buts = lp.ButtonStateXY()

            
            
            parse_button_press(buts, lp)
            

            

    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        # Close the Launchpad
        lp.Reset()
        lp.Close()
        print("Launchpad closed.")

if __name__ == "__main__":
    main()
