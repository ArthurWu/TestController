import sys, ConfigParser
from copybuild import *
from cleanfolder import *

def get_config():
    try:
        config_reader = ConfigParser.ConfigParser()
        config_reader.read('config.ini')
        return config_reader
    except:
        raise Exception('Please check the config.ini exists, or its content is correct or not.')

if __name__ == '__main__':
    try:
        config_reader = get_config()

        #Get path of build in SPB builder and path of build on local
        build_source_path = config_reader.get('build', 'srcpath') % sys.argv[1]
        build_destination_path = config_reader.get('build', 'dstpath') % sys.argv[1]

        #Get path of pool
        pending_path = config_reader.get('pools','pendings')
        lab_status = config_reader.get('pools','labstatus')
        test_results = config_reader.get('pools','testresult')


        #Clean pool folders
        clean_folder(pending_path)
        clean_folder(lab_status)
        clean_folder(test_results)

        #Get file name of latest IPAgent
        latest_agent = get_latest_ipagent(build_source_path)

        #Copy builds
        get_build(build_source_path,build_destination_path,'qsInfoPortal.msi',latest_agent)

        #Unzip IPAgent
        unzip_ipagent(build_destination_path, latest_agent)

        #Copy files to pending folder
        licence_source_path = config_reader.get('prepration','licence') % sys.argv[1]
        cmdlets_source_path = config_reader.get('prepration','cmdlets') % sys.argv[1]

        copy_files_to_pending(build_destination_path, cmdlets_source_path, licence_source_path, pending_path)

        #prepare fitnesse root folder
        fitnesseroot = config_reader.get('prepration','fitnesseroot') % sys.argv[1]
        workingfitroot = config_reader.get('prepration','workingfitroot')

        update_fitnesse_root(fitnesseroot, workingfitroot)

    except Exception, ex:
        print str(ex)



