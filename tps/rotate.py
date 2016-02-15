# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

import logging
import sys
import time

from tps.acpi.thinkpad_acpi import ThinkpadAcpi
from tps.hdaps import Hdaps
from tps.compositor import NORMAL, UnknownDirectionException, \
                           ScreenNotFoundException, get_rotation, \
                           new_rotation, rotate, get_input_state, \
                           set_inputs_state 
from tps.utils import check_call, check_output

logger = logging.getLogger(__name__)



def rotate_cmdline(options, config):
    try:
        new_direction = new_rotation(
            get_rotation(config['screen']['internal']),
            options.direction, config, options.force_direction)
    except UnknownDirectionException:
        logger.error(_('Direction cannot be understood.'))
        sys.exit(1)
    except ScreenNotFoundException as e:
        logger.error(_('Unable to determine rotation of "{}": {}').format(
            config['screen']['internal'], e))
        sys.exit(1)
        
    input_state = get_input_state(options.state, options.direction)

    rotate(new_direction, config, input_state)

def rotate_daemon(options, config):
    if not Hdaps.hasHDAPS():
        sys.exit(1)
    
    try:
        current_rotation = get_rotation(config['screen']['internal'])
    except ScreenNotFoundException as e:
        logger.error(_('Unable to determine rotation of "{}": {}').format(
            config['screen']['internal'], e))
        sys.exit(1)
       
    hdaps_resting_x = config['hdaps'].getint('resting_x')
    hdaps_resting_y = config['hdaps'].getint('resting_y')
    hdaps_resolution_x = config['hdaps'].getint('resolution_x')
    hdaps_resolution_y = config['hdaps'].getint('resolution_y')
    hdaps_invert = config['hdaps'].getint('invert')
    hadps_poll_interval = config['hdaps'].getfloat('poll_interval')
    
    hdaps = Hdaps((hdaps_resting_x, hdaps_resting_y), 
        (hdaps_resolution_x, hdaps_resolution_y))
    if hdaps_invert > 0:
        hdaps.setInvertion(hdaps_invert)
    
    autorotate_tablet_mode = config['rotate'].\
        getboolean('autorotate_tablet_mode')
    autorotate_laptop_mode = config['rotate'].\
        getboolean('autorotate_laptop_mode')
        
    default_rotation = translate_direction(
        config['rotate']['default_rotation'])
    tablet_mode = ThinkpadAcpi.inTabletMode()
    
    while True:
        time.sleep(hadps_poll_interval);
        tablet_mode_prev = tablet_mode
        tablet_mode = ThinkpadAcpi.inTabletMode()
        try:
            if tablet_mode:
                if not autorotate_tablet_mode:
                    desired_rotation = default_rotation
                else:
                    desired_rotation = hdaps.getHdapsOrientation(True)
            elif not autorotate_laptop_mode:
                desired_rotation = NORMAL
            else:
                desired_rotation = hdaps.getHdapsOrientation(False)
                
            if desired_rotation is None or \
                current_rotation == desired_rotation:                    
                if tablet_mode != tablet_mode_prev:
                    # when orientation does not change but table mode
                    # does we're left with disabled controls
                    set_inputs_state(config, not tablet_mode)
                continue
        except UnknownDirectionException:
            logger.error(_('Direction cannot be understood.'))
            sys.exit(1)

        rotate(desired_rotation, config, not tablet_mode)
        current_rotation = desired_rotation
