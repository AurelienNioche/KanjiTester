# -*- coding: utf-8 -*-
# 
#  __init__.py
#  consoleLog
#  
#  Created by Lars Yencken on 2008-06-12.
#  Copyright 2008-06-12 Lars Yencken. All rights reserved.
# 

__all__ = [
        'consoleLog',
        'io',
        'progressBar',
        # 'shell',
        'slot',
    ]



import consoleLog.consoleLog as consoleLog
import consoleLog.progressBar as progressBar
from consoleLog.progressBar import withProgress
import consoleLog.slot as slot


# Provide a default logging object 
default = consoleLog.ConsoleLogger()


def demo():
    import time
    sl = time.sleep
    log = consoleLog.ConsoleLogger()

    log.start('Starting logger demo')
    log.log('Performing some initialisation')
    sl(1.0)

    log.start('Serious processing with substeps')
    log.log('Substep 1')
    sl(1.0)
    log.log('Substep 2')
    sl(1.0)
    log.log('Substep 3 with progress ', newLine=False)
    for _ in withProgress(range(100)):
        sl(0.1)
    log.start('Substep 4 with slot', nSteps=1)
    log.log('', newLine=False)
    s = slot.Slot()
    j = 0
    for _ in range(637):
        j += 1
        time.sleep(0.01)
        if j % 100 == 0:
            s.update(str(j))
    s.finish(str(j))
    log.finish()

    log.finish('Completed ok')

    log.log('Postprocessing step')
    sl(1.0)
    log.finish()
