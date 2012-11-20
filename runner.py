import sys, ConfigParser
from copybuild import *

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

        #Get file name of latest IPAgent
        latest_agent = get_latest_ipagent(build_source_path)

        #Copy builds
        get_build(build_source_path,build_destination_path,'qsInfoPortal.msi',latest_agent)

        #Unzip IPAgent
        unzip_ipagent(build_destination_path, latest_agent)
    except Exception, ex:
        print str(ex)



