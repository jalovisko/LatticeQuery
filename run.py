import os
if 'CASROOT' in os.environ:
    del os.environ['CASROOT']

from cq_editor.__main__ import main

main()
