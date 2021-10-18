# python3 ./spectracsServer.py --spectralSensors AMS_7262 --mock

from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import curses
import json
from random import random
#from urllib.parse import urlparse
import urllib.parse
#import SpectralMeasurement
import jsonpickle
import SpectracsServerHardware
import SpectralMeasurement
import SpectralSensorName
import sys
import argparse

from colormath.color_objects import SpectralColor,XYZColor,sRGBColor
from colormath.color_conversions import convert_color

from firmware.as7265x import As7265x


class ConsolePrinter:

    __instance = None

    @staticmethod 
    def getInstance():

        """ Static access method. """
        if ConsolePrinter.__instance == None:
            ConsolePrinter()
        return ConsolePrinter.__instance

    def __init__(self):

        """ Virtually private constructor. """
        if ConsolePrinter.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ConsolePrinter.__instance = self
            self.screen = screen = curses.initscr()
            curses.curs_set(0)

    def getScreen(self):
        return self.screen

    def printCenter(self,message,yOffset=0):

        screen=self.getScreen()
        num_rows, num_cols = screen.getmaxyx()

        # Calculate center row
        middle_row = int(num_rows / 2)+yOffset

        # Calculate center column, and then adjust starting position based
        # on the length of the message
        half_length_of_message = int(len(message) / 2)
        middle_column = int(num_cols / 2)
        x_position = middle_column - half_length_of_message 

        # Draw the text
        screen.addstr(middle_row, x_position, message)
        screen.refresh()

    def printStatusLine(self,message,yOffset=0):

        screen=self.getScreen()
        num_rows, num_cols = screen.getmaxyx()

        # Calculate center row
        middle_row = int(num_rows / 2)+yOffset

        # Calculate center column, and then adjust starting position based
        # on the length of the message
        half_length_of_message = int(len(message) / 2)
        middle_column = int(num_cols / 2)
        x_position = 1

        # Draw the text

        screen.addstr(num_rows-2, x_position, message.ljust(num_cols-1,' '))
        screen.refresh()


    def finish(self,message,yOffset=0):
        curses.endwin()

class SpectracsServerCommand:

    HARDWARE="hardware"
    VERSION="version"
    MEASUREMENT="measurement"

class SpectracsServerCommandLineArgument():        

    SPECTRAL_SENSORS="spectralSensors"
    SPECTRAL_SENSORS_LIGHTS="spectralSensorsLights"    

    MOCK="mock"

    SERVER_NAME = "serverName"
    SERVER_PORT = "serverPort"

class SpectracsServer(HTTPServer):        

    def __init__(self,server_address, RequestHandlerClass):
        super(HTTPServer, self).__init__(server_address, RequestHandlerClass)        

    def setCommandLineArguments(self,commandLineArguments):
        self.commandLineArguments=commandLineArguments

    def getCommandLineArguments(self):
        return self.commandLineArguments


class SpectracsRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        #self.send_header("Content-Type", "audio/x-wav")
        self.end_headers()

        parsed_path = urllib.parse.urlsplit(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)

        action=query['action'][0]    

        if action=='measurement':
            ConsolePrinter.getInstance().printStatusLine("measurement: 32665,32665,32665,32665,32665,32665")
            spectralMeasurement=SpectralMeasurement.SpectralMeasurementAms7262()
            #spectralMeasurement.setValues({450:random(),500:random(),550:random(),570:random(),600:random(),650:random()})

            
            #spectralMeasurement.setValues({450:1.1165746450424194,500:1.1915769577026367,550:1.0741294622421265,570:0.9279702305793762,600:4.03620719909668,650:5.880025863647461})




            spectralMeasurement.setValues({450:0.0,500:0,550:0,570:0,600:0,650:20000.0/32000.0})

            spectralMeasurement.setValues({450:0.0,500:0,550:0,570:0,600:0,650:4000.0/32000.0})

            spectralMeasurement.setValues({450:0,500:0,550:15000.0/32000.0,570:0,600:0,650:20000.0/32000.0})

            spectralMeasurement.setValues({450:710.54541015625/32000.0,500:2814.272705078125/32000.0,550:1892.8314208984375/32000.0,570:3259.364013671875/32000.0,600:2497.695556640625/32000.0,650:4386.8564453125/32000.0})



            factor=500

            #spectralMeasurement.setValues({450:710.54541015625/factor,500:2814.272705078125/factor,550:1892.8314208984375/factor,570:3259.364013671875/factor,600:2497.695556640625/factor,650:4386.8564453125/factor})
            spectralMeasurement.setValues({450:random(),500:random(),550:random(),570:random(),600:random(),650:random()})


                #foo= [5.880025863647461, 4.03620719909668, 0.9279702305793762, 1.0741294622421265, 1.1915769577026367, 1.1165746450424194];

            as7265x=As7265x.As7265x()
            spectralMeasurement.setValues(as7265x.measure())



            timestamp=datetime.now()
            cur_day_format = timestamp.strftime("%Y-%m-%d,%H:%M:%S ")
            ConsolePrinter.getInstance().printStatusLine(cur_day_format+'measurement')

            self.wfile.write(bytes(jsonpickle.encode(spectralMeasurement).replace('py/object','class'), "utf-8"))




            #xyzcol = self.spectral_to_xyz(spectralMeasurement) 
            #rgbcol=self.convert_to_rgb(xyzcol,1))

            #print (xyzcol)


            

        if action=='version':

            timestamp=datetime.now()
            cur_day_format = timestamp.strftime("%Y-%m-%d,%H:%M:%S ")
            ConsolePrinter.getInstance().printStatusLine(cur_day_format+'version')

            self.wfile.write(bytes("version: 1.0", "utf-8"))        

        if action==SpectracsServerCommand.HARDWARE:
            spectracsServerServer=SpectracsServerHardware.SpectracsServerServer()

            timestamp=datetime.now()
            cur_day_format = timestamp.strftime("%Y-%m-%d,%H:%M:%S ")
            ConsolePrinter.getInstance().printStatusLine(cur_day_format+'hardware')

            self.wfile.write(bytes(jsonpickle.encode(spectracsServerServer).replace('py/object','class'), "utf-8"))


    def log_message(self, format, *args):
            return


    def spectral_to_xyz(self,spectralMeasurement):
        """Convert Scan to RGB Colour"""

        spectralMeasurementValues=spectralMeasurement.getValues();

        spc = SpectralColor(
            observer='10', illuminant='D65',
            spec_650nm=str(spectralMeasurementValues[650]), 
            spec_600nm=str(spectralMeasurementValues[600]),
            spec_570nm=str(spectralMeasurementValues[570]),
            spec_550nm=str(spectralMeasurementValues[550]),
            spec_500nm=str(spectralMeasurementValues[500]),
            spec_450nm=str(spectralMeasurementValues[450]))



        xyz = convert_color(spc, XYZColor) #convert spectral signals to XYZ colour space
        return xyz
        
    #def convert_to_rgb(SpectralMeasurement.SpectralMeasurementAms7262 spectralMeasurement,clip):
    #    """Convert colour object to RGB for Screen Colours as r,g,b"""
    #    #Colour object can be XYZColor, sRGBColor or other colormath color object
    #    #clip of 1 will restrict the max value to 255, possibly alter the colour.
    #    rgbcol = convert_color(self, sRGBColor,is_upscaled=False)  #convert to sRGB screen colours
    #    if clip == 1:
    #        #Clip RB Values to 255
    #        rgbcol = sRGBColor(rgbcol.clamped_rgb_r,rgbcol.clamped_rgb_g,rgbcol.clamped_rgb_b) #limit RGB max to 1
    #    rgbcol = rgbcol.get_upscaled_value_tuple() # convert from 0-1 to 0-255
    #    return rgbcol[0],rgbcol[1],rgbcol[2] #return r,g,b values 0-255


if __name__ == "__main__":        
   
    ConsolePrinter.getInstance().printCenter("  _____ _____  ______ _____ _______ _____            _____  _____ ",-6)
    ConsolePrinter.getInstance().printCenter(" / ____|  __ \|  ____/ ____|__   __|  __ \     /\   / ____|/ ____|",-5)
    ConsolePrinter.getInstance().printCenter("| (___ | |__) | |__ | |       | |  | |__) |   /  \ | |    | (___  ",-4)
    ConsolePrinter.getInstance().printCenter(" \___ \|  ___/|  __|| |       | |  |  _  /   / /\ \| |     \___ \ ",-3)
    ConsolePrinter.getInstance().printCenter(" ____) | |    | |___| |____   | |  | | \ \  / ____ \ |____ ____) |",-2)
    ConsolePrinter.getInstance().printCenter("|_____/|_|    |______\_____|  |_|  |_|  \_\/_/    \_\_____|_____/ ",-1)

    ConsolePrinter.getInstance().printCenter("... and there was light ...",1)
                                                              
    # Wait and cleanup
    #curses.napms(3000)


    parser = argparse.ArgumentParser(description='spectracs server')

    parser.add_argument('--'+SpectracsServerCommandLineArgument.SERVER_NAME, dest=SpectracsServerCommandLineArgument.SERVER_NAME, type=str, help='server name',default="localhost")
    parser.add_argument('--'+SpectracsServerCommandLineArgument.SERVER_PORT, dest=SpectracsServerCommandLineArgument.SERVER_PORT, type=int, help='server port',default=8877)

    parser.add_argument('--'+SpectracsServerCommandLineArgument.SPECTRAL_SENSORS, dest=SpectracsServerCommandLineArgument.SPECTRAL_SENSORS, type=str, help='spectral sensors')
    parser.add_argument('--'+SpectracsServerCommandLineArgument.SPECTRAL_SENSORS_LIGHTS, dest=SpectracsServerCommandLineArgument.SPECTRAL_SENSORS_LIGHTS, type=str, help='spectral sensors')
    parser.add_argument('--'+SpectracsServerCommandLineArgument.MOCK, dest=SpectracsServerCommandLineArgument.MOCK, action='store_true')
    parser.set_defaults(mock=False)

    commandLineArguments=parser.parse_args()

    spectracsServer = SpectracsServer((commandLineArguments.serverName, commandLineArguments.serverPort), SpectracsRequestHandler)

    spectracsServer.setCommandLineArguments(commandLineArguments)
    #print(spectracsServer.getCommandLineArguments())

    ConsolePrinter.getInstance().printStatusLine("started server")



    try:
        spectracsServer.serve_forever()
    except KeyboardInterrupt:
        pass

    spectracsServer.server_close()
    ConsolePrinter.getInstance().finish()
    print("Server stopped.")




