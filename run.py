import os, sys, asyncio
import faulthandler

faulthandler.enable()

if sys.platform != 'win32' and 'CASROOT' in os.environ:
    del os.environ['CASROOT']

if 'QT_QPA_PLATFORM' not in os.environ:
    os.environ['QT_QPA_PLATFORM'] = 'xcb'

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from cq_editor.__main__ import main

main()
