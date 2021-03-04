import pdb
import sys
import traceback

try:
    print("Dangerous code here")

except:
    # debugger
    extype, value, tb = sys.exc_info()
    traceback.print_exc()
    pdb.post_mortem()
