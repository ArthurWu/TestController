import os
import shutil

def get_latest_ipagent(srcpath, pattern='qsInfoPortalAgent*.zip', reverse=True):
    import glob
    files_name = glob.glob1(srcpath,pattern)
    return sorted(files_name,reverse=reverse)[0]


def check_folder(dest):
    if not os.path.exists(dest):
        os.mkdir(dest)


def get_build(src, dest, msi, ipagent):
    check_folder(dest)
    msi_source_path = os.path.join(src,msi)
    ipagent_source_path = os.path.join(src,ipagent)
    msi_distination_path = os.path.join(dest,msi)
    ipagent_distination_path = os.path.join(dest,ipagent)
    shutil.copyfile(ipagent_source_path, ipagent_distination_path)
    shutil.copyfile(msi_source_path, msi_distination_path)

def unzip_ipagent(dest, ipagent):
    ipagent_distination_path = os.path.join(dest,ipagent)
    unziped_ipagent_path = os.path.join(dest,'IPAgent')
    check_folder(unziped_ipagent_path)
    import zipfile
    zfile = zipfile.ZipFile(ipagent_distination_path)
    zfile.extractall(unziped_ipagent_path)

def copy_files_to_pending(build_destination_path, cmdlets_source_path, licence_source_path, pending_path):
    msi_source_path = os.path.join(build_destination_path, 'qsInfoPortal.msi')
    msi_destination_path = os.path.join(pending_path, 'qsInfoPortal.msi')
    licence_destination_path = os.path.join(pending_path, 'current_license.asc')
    ipagent_source_path = os.path.join(build_destination_path, 'IPAgent')
    ipagent_destination_path = os.path.join(pending_path, 'IPAgent')
    cmdlets_destination_path = os.path.join(pending_path, 'cmdlets')

    shutil.copyfile(msi_source_path, msi_destination_path)
    shutil.copyfile(licence_source_path, licence_destination_path)
    shutil.copytree(ipagent_source_path, ipagent_destination_path)
    shutil.copytree(cmdlets_source_path, cmdlets_destination_path)

