import launch
import os,sys
import os,time,json,pickle
import shutil
module_path = os.path.dirname(__file__)
sys.path.insert(0, module_path)
# if not launch.is_installed("pyjwt"):
#     launch.run_pip("install pyjwt", "")
if not launch.is_installed("cryptography"):
   launch.run_pip("install cryptography", "")
if not launch.is_installed("psutil"):
   launch.run_pip("install psutil", "")
from scripts.cryp_gui_func import  uninstall_encryption
uninstall_encryption()

