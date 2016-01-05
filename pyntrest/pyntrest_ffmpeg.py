r"""This module contains FFMPEG and Audio/Video related functions."""

import re
import subprocess 

class FFMPEG_Handler:
    """Python handler binding for ffmpeg"""
    
    def __init__(self, ffmpeg_executable_path='ffmpeg'):
        self.ffmpeg_path = ffmpeg_executable_path
        initcommand = self.ffmpeg_path + ' -version'
        print 'command: {0}'.format(initcommand)
        code, _, _ = self.__runcommand(initcommand)
        if code is not 0:
            raise IOError('FFMPEG not available at location \'{0}\''.format(
                                               ffmpeg_executable_path)) 
    
    def get_file_duration(self, filepath):
        """Returns the duration of the given media filepath as 
        ffmpeg timestamp and in milliseconds"""
        
        if not self.__file_exists(filepath):
            raise IOError('Given filepath {0} does not exist!'.format(filepath))
        command = '{0} -i {1}'.format(self.ffmpeg_path, filepath)
        print 'command: {0}'.format(command)
        _, _, err = self.__runcommand(command, True, True)
        dur_line = None
        print '------- ffmpeg --------';
        for e in err:
            if 'Duration: ' in e:
                print e
                
                dur_line = e
        print '-----------------------';
        if dur_line is None:
            raise IOError('FFMPEG Error. Consider using verbose-mode.') 
        logline_split = dur_line.split(' ')
        duration_string = re.sub(',.*', '', logline_split[1]) 
        return (duration_string, 
                self.__convert_ffmpeg_timestamp_to_milliseconds(duration_string))
    
    def extract_thumbnail(self, video_filepath, target_thumbpath, at_time=0):
        if not self.__file_exists(video_filepath):
            raise IOError('Given filepath {0} does not exist!'.format(video_filepath))
        command = '{0} -y -ss {1} -i {2} -vframes 1 -f image2 {3}'.format(
                self.ffmpeg_path, at_time, video_filepath, target_thumbpath)
        print 'command: {0}'.format(command)
        _, _, _ = self.__runcommand(command, True, True)

    def __runcommand (self, command, suppress_stdout=False, suppress_stderr=False,
                useshell=True):
        """Run a command on the command line"""
        
        log_stdout = []
        handle = subprocess.Popen(command, shell=useshell, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
            
        while handle.poll() is None:
            line = handle.stdout.readline().strip()
            if line is not None and line != "":
                log_stdout.append(line)
                if suppress_stdout == False:
                    print line
        
        log_stderr = log_stdout
        return handle.returncode, log_stdout, log_stderr

    def __convert_ffmpeg_timestamp_to_milliseconds (self, timestamp):
        """Converts a timestamp of form hh:mm:ss.fff to a millisecond 
        integer representation"""
        
        tmp = re.sub('[^0-9]', ' ', timestamp)
        split = tmp.split(' ')
        total_time = 0
        if len(split) == 4:
            split[3] = split[3].ljust(3, '0')
            total_time += int(split[3])
        total_time = total_time + (int(split[2]) * 1000)
        total_time = total_time + (int(split[1]) * 1000 * 60)
        total_time = total_time + (int(split[0]) * 1000 * 60 * 60)
        return total_time
    
    def __file_exists (self, path):
        """Tests if a file exists"""
        
        try:
            with open(path):
                return True
        except IOError:
            return False