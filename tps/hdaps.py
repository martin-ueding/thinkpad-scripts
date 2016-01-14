# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

"""
HDAPS accelerometer sensor machinery

Information:
http://www.thinkwiki.org/wiki/HDAPS
http://www.thinkwiki.org/wiki/Active_Protection_System
http://www.thinkwiki.org/wiki/Tp_smapi
https://wiki.archlinux.org/index.php/Hard_Drive_Active_Protection_System
http://www.thinkwiki.org/wiki/Script_for_theft_alarm_using_HDAPS
http://liken.otsoa.net/blog/?x=entry:entry080617-120522 - x41 example

Inspired by:
https://github.com/caio/playground/blob/master/hdaps/hdaps.py
"""

import logging
import math
import os
import sys

from tps import LEFT, RIGHT, NORMAL, INVERTED

logger = logging.getLogger(__name__)

class Hdaps(object):
    '''Hdaps accelerometer sensor machinery
    
    The x-axis is in the plane of the keyboard and points to the right 
    (from the perspective of a user sitting at the computer).
    
    The y-axis in in the plane of the keyboard and points towards the 
    back of the computer. 
    
    Rotation about the x-axis is Pitch and rotation about the y-axis 
    is Roll. The Thinkpad coordinate system differs from the the 
    aeronautical standard where the x-axis points "forward" and the 
    y-axis "out the right wing", so the relationship to pitch and 
    roll is different as well.
    
    Pitch, or rotation about the x-axis: As the screen of the Thinkpad 
    is tilted towards the user the "x" readings from the sensor 
    increase to a maximum when the keyboard is vertical with the space 
    bar being the lowest key. The "x" readings reach a minimum value 
    when the keyboard is vertical with the Esc key being the lowest 
    key. It appears that the "x" readings are proportional to the sine 
    of the angle of rotation about the x-axis.
    Place your right hand on to the keyboard and turn it over so the 
    palm faces up. Your thumb points to the right and in the direction 
    of the x-axis. If you curl your fingers towards you (making a 
    fist), your fingers are moving in the direction of positive 
    x-rotation angles.
    
    Roll, or rotation about the y-axis: As the left side of the 
    keyboard is lifted upwards, rotating the keyboard in a clockwise 
    direction, the "y" readings from the sensor increase to a maximum 
    value when the Thinkpad is on its right side (the Enter key is the 
    lowest key). It appears that the "y" readings are proportional to 
    the sine of the angle of rotation about the y-axis.
    
    Data indicates that the "x" readings can be converted to angles 
    (pitch) as: PITCH = ASIN(A_x / g) assuming that g is gravity and 
    the x readings A_x have been normalized such that they vary from 
    -1g to 1g. For y this would be: ROLL = ASIN(A_y / g)
    Once we have calibrated the readings by establishing the value when 
    flat and the maximum value, we can convert to angles (in degrees) 
    as follows (the example is for x, for y it is the analogous):

    x_normalized = ( x - avg_x_when_flat ) / ( max_x - avg_x_when_flat )
    radians_x = arcsine ( x_normalized )
    degrees_x = radians_x * 180 / PI

    Note that in my case the maximum and minimum readings were not 
    symmetrically positioned about the average "flat" reading. 
    I found that the readings for x range from +150 to -156 and for y 
    they range between +152 to -155. There is a good chance my work 
    surface is not horizontal.
    
    In order to achieve a good calibration read position data with 
    sampling interval of 150ms and log the output to this text file 
    while slowly rotating the computer through all pitch and roll 
    angles, moving slowly through the expected extremes. Then import 
    this data into a spreadsheet and compute the maximum and minimum 
    x and y values. With the assumption that the sensor's 
    sensitivity and accuracy are symmetrical about the zero position, 
    you should arrive at similar sensor range calibration for your 
    device:

    rest position    resolution
      x: 494.5       +/- 159.5
      y: 566.0       +/- 157.0
    
    @source: http://www.stanford.edu/~bsuter/thinkpad-accelerometer/
    '''
    
    HDAPS_SYSFS_BASE = '/sys/devices/platform/hdaps/'
    
    # HDAPS current position (ro)
    HDAPS_POSITION_FILE = 'position'
    
    # HDAPS calibration - device "resting" position (rw)
    HDAPS_CALIBRATION_FILE = 'calibrate'
    
    # HDAPS accelerometer sapling rate (ro)
    HDAPS_SAMPLING_RATE_FILE = 'sampling_rate'
    
    # HDAPS axis position data inversion (rw):
    HDAPS_INVERT_FILE = 'invert'
    
    def __init__(self, calibration, resolution = (150, 150)):
        """Allowing to specify custom callibration.
        If not provided current driver calibration setting is used.
        Resolution (unit/earth gravity) is used to obtain normalized 
        device position if real device resolution is different 
        than advertised.
        """
        if not Hdaps.hasHDAPS():
            logger.error('HDAPS not available in sysfs. Have you loaded hdaps kernel module?')
        else:
            self.setRestingPosition(calibration)
        self.setResolution(resolution)

    @staticmethod
    def hasHDAPS():
        return os.path.exists(Hdaps.HDAPS_SYSFS_BASE + Hdaps.HDAPS_POSITION_FILE) \
            and os.path.exists(Hdaps.HDAPS_SYSFS_BASE + Hdaps.HDAPS_CALIBRATION_FILE)

    @staticmethod
    def getAbsolutePosition():
        """Current Absolute Position, Raw data, unaffected by calibration 
        offset. Position values are in [1000,1000] range, but realistically
        most of time are constrained in [350,650] due to accelerometer
        lower than advertised resolution."""
        return Hdaps._readPosition(Hdaps.HDAPS_POSITION_FILE)
    
    def getRelativePosition(self, rounding = 1):
        """Current Relative Position to Resting/calibration position.
        Rounding: rounding = 5 means every value x returned will be x mod 5 = 0
        """
        position = Hdaps.getAbsolutePosition()
        return [ Hdaps._getRelativePosition(position[n], self._calibration[n], rounding) for n in (0, 1) ]
        
    def getNormalizedPosition(self):
        """Normalized position bound [-1;1]
        
        Reasoning: HDAPS accelerometers (good example here is ADXL320) 
        although advertising higher resolution, actually fall behind.
        """
        relativePosition = self.getRelativePosition(0)
        return [ Hdaps._getNormalizedPosition(relativePosition[n], self._resolution[n]) for n in (0, 1) ]
    
    def getRotation(self):
        """Calculate rotation about x and y axis (Pitch and Roll accoridingly).
        """
        normalizedPosition = self.getNormalizedPosition(0)
        return list(map(Hdaps._getAngle, normalizedPosition))
        
    def getRestingPosition(self):
        return self._calibration
    
    def setRestingPosition(self, calibration):
        self._calibration = calibration \
                if calibration is not None else Hdaps.getDriverRestingPosition()
                
    def getResolution(self):
        return self._resolution
        
    def setResolution(self, resolution):
        self._resolution = resolution
    
    @staticmethod
    def getDriverRestingPosition():
        """AKA Calibration - leveled/flat/resting position:
        - set by the hdaps kernel driver to the first obtained x,y 
          position during kernel driver initialization (which is useless 
          unless laptop was perfectly positioned during that time),
        - updated when calibrate or invert file is written,
        - therefore must be changed manually by the user to obtain 
          accurate calibration,
        @see: https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/drivers/platform/x86/hdaps.c
        """
        return Hdaps._readPosition(Hdaps.HDAPS_CALIBRATION_FILE)
    
    @staticmethod
    def setDriverRestingPositionToCurrent():
        """Initialize calibration settings to current position reading.
        Warning: Will require root priviledges to write to sysfs!
        """
        try:
            with open(Hdaps.HDAPS_SYSFS_BASE + Hdaps.HDAPS_CALIBRATION_FILE, 'w') as f:
                f.write("1")
            return True
        except IOError:
            logger.error('Unable to initialize HDAPS sensor calibration!')
            return False
    
    @staticmethod
    def getSamplingRate():
        """Accelerometer Sampling Rate in Hz"""
        try:
            with open(Hdaps.HDAPS_SYSFS_BASE + Hdaps.HDAPS_SAMPLING_RATE_FILE, 'r') as f:
                return int(f.read())
        except IOError:
            logger.error('Unable to read HDAPS sampling rate!')
            raise
            
    @staticmethod
    def getInvertion():
        try:
            with open(Hdaps.HDAPS_SYSFS_BASE + Hdaps.HDAPS_INVERT_FILE, 'r') as f:
                return int(f.read())
        except IOError:
            logger.error('Unable to read HDAPS invertion!')
            raise
            
    @staticmethod
    def setInvertion(invertion):
        """For some ThinkPads, the invert module parameter is needed in 
        order to handle the X and Y rotation axes correctly. 
        
        The invert option takes the following values: 
        invert=1 invert both X and Y axes;
        invert=2 invert the X axes (uninvert if already both axes inverted)
        invert=4 swap X and Y (takes place before inverting)
        Note that options can be summed. For instance, invert=5 swaps 
        the axes and inverts them. The maximum value of invert is obviously 7.
        
        Invert parameters
        value 	R 	P
          0     X   Y
          1    -X   -Y
          2    -X   Y
          3     X   -Y
          4     Y   X
          5    -Y   -X
          6    -Y   X
          7     Y   -X

        @see: http://www.thinkwiki.org/wiki/Tp_smapi for reference values
        Warning: Will require root priviledges to write to sysfs!
        Warning: Will cause to refresh driver calibration settings!
        """
        try:
            with open(Hdaps.HDAPS_SYSFS_BASE + Hdaps.HDAPS_INVERT_FILE, 'w') as f:
                f.write(str(invertion))
            return True
        except IOError:
            logger.error('Unable to write HDAPS invertion!')
            return False
        
    def getOrientation(self, inverted = False):
        """Orientation based upon a normalized position.
        The exception here is that we swap x<>y for the sake of the 
        well known algorithm using aeronautical coordinate system.
        @see: Tilt Sensing Using a Three-Axis Accelerometer by: Mark Pedle
        """
        dy, dx = self.getNormalizedPosition()
        if dx > 0.5 and abs(dy) < 0.4:
            return INVERTED if inverted else NORMAL
        elif dx < -0.5 and abs(dy) < 0.4:
            return NORMAL if inverted else INVERTED
        elif abs(dx) < 0.4 and dy > 0.5:
            return RIGHT if inverted else LEFT
        elif abs(dx) < 0.4 and dy < -0.5: 
            return LEFT if inverted else RIGHT

    def getOrientationWithThreshold(self, threshold = 40, inverted = False):
        dx, dy = self.getRelativePosition()
        if abs(dx) - abs(dy) > threshold:
            if dx > threshold:
                return RIGHT if inverted else LEFT
            elif dx < -threshold: 
                return LEFT if inverted else RIGHT
        elif abs(dy) - abs(dx) > threshold:
            if dy > threshold:
                return INVERTED if inverted else NORMAL
            elif dy < -threshold:
                return NORMAL if inverted else INVERTED
            
    @staticmethod
    def _getAngle(normalizedPosition):
        return math.degrees(math.asin(normalizedPosition))
    
    @staticmethod
    def _getNormalizedPosition(relativePosition, resolution):
        constrainedPosition = Hdaps._getConstrainedPosition(relativePosition, resolution)
        return float(constrainedPosition) / resolution

    @staticmethod
    def _getConstrainedPosition(relativePosition, resolution):
        return min(relativePosition, resolution) if relativePosition >= 0 \
            else max(relativePosition, -resolution)
            
    @staticmethod
    def _getRoundedPosition(position, rounding):        
        return int(float(position) / rounding) * rounding if rounding > 0 else position
        
    @staticmethod
    def _getRelativePosition(position, restingPosition, rounding):
        return Hdaps._getRoundedPosition(position - restingPosition, rounding)

    @staticmethod
    def _readPosition(positionFile):
        try:
            with open(Hdaps.HDAPS_SYSFS_BASE + positionFile, 'r') as f:
                return list(map(int, f.read()[1:-2].split(",")))
        except IOError:
            logger.error('Unable to read HDAPS sensor file: %s!' % positionFile)
            raise
