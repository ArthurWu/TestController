from copybuild import *
from cleanfolder import *
def update_fitnesse_root(fitnesseroot, workingfitroot):
    import win32serviceutil
    win32serviceutil.StopService('FitNesse')
    remove_folder(workingfitroot)
    copy_fitnesse_root(fitnesseroot, workingfitroot)
    win32serviceutil.StartService('FitNesse')