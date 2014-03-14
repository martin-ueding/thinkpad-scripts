import logging

logger = logging.getLogger(__name__)

def set_launcher(autohide):
    if not tps.has_program('dconf'):
        logger.warning('dconf is not installed')
        return

    logger.error('set_laucher() not implemented')

