"""
apple_coding.py that has class FilesContainKeyword and main function.
Author: Omer Can Palaz
"""

import sys
import os
import re
import mmap
import matplotlib.pyplot as plot

class FilesContainKeyword(object):
    """
    Class to recursively walk a <root_dir> and detect all the files under 
    that dir contains <keywords> and count the number of files for that sub dir.
    """

    """Constructor
    :param root_dir: Root directory path from command line.
    :param keyword: Regular expression.
    """
    def __init__(self, root_dir, keyword):
        if root_dir is None:
            raise ValueError("Root directory: root_dir is None! \n")
        if keyword is None:
            raise ValueError("Keyword: keyword is None! \n")
        if not FilesContainKeyword.is_dir(root_dir):
            raise ValueError("Root directory: {} DOES NOT exist! \n".format(root_dir))
        if not FilesContainKeyword.is_keyword_valid(keyword):
            raise ValueError("Keyword: {} is not a VALID regexp! \n".format(keyword))

        root_abs_path = os.path.abspath(os.path.normpath(root_dir))

        self.base_root_path = os.path.dirname(root_abs_path) # Path of the root whic does not consist dir name.
        self.root_dir = os.path.basename(root_abs_path) # Root directory name.
        self.compiled_regexp = re.compile(keyword) # Compiled regexp.

    """Walks the root directory and returns count dictionary.
    :return : Count dictionary.
    """
    def walk_root_dir(self):
        # Initiliaze count_dict to keep track of number of files that contains the keyword for each subdir.
        count_dict = {}
        # Initiliaze file_dict to keep track of visited files by their real paths with their search results.
        file_dict = {}
    
        self.walk_root_dir_helper(self.root_dir, count_dict, file_dict)
        return count_dict
    
    """Helper function to walk the root directory.
    :param dir_path: Current directory path (e.g. a/b/c).
    :param count_dict: Dictionary which holds count of each sub.
    :param file_dict: Dictionary which holds file process results.
    """
    def walk_root_dir_helper(self, dir_path, count_dict, file_dict):
        # Keep real path of current directory.
        dir_real_path = self.to_real_path(os.path.join(self.base_root_path, dir_path))
        # Initliaze count value for current directory.
        self.init_dir_count_in_dict(dir_path, count_dict)

        # Get file list in current directory and iterate through the file list and process them.
        file_list = FilesContainKeyword.get_files(os.path.join(self.base_root_path, dir_path))
        for f in file_list:
            self.process_file(f, file_dict, dir_path, count_dict)

        # Recursively walk sub dirs.
        subdir_list = FilesContainKeyword.get_subdirs(os.path.join(self.base_root_path, dir_path))
        for d in subdir_list:
            # Check if real path of subdir links to a parent directory to prevent loops.
            if  self.to_real_path(d) not in dir_real_path:
                self.walk_root_dir_helper(os.path.join(dir_path, os.path.basename(d)), count_dict, file_dict)
    
    """Helper function to walk the root directory.
    :param file_path: File path of the file to process.
    :param file_dict: Dictionary which holds file process results.
    :param dir_path: Current directory path (e.g. a/b/c).
    :param count_dict: Dictionary which holds count of each sub.
    """
    def process_file(self, file_path, file_dict, dir_path, count_dict):
        real_file_path = FilesContainKeyword.to_real_path(file_path)
        if file_dict.get(real_file_path) is not None and file_dict.get(real_file_path) is True:
            self.increase_count_in_dict(dir_path, count_dict)

        elif file_dict.get(real_file_path) is None:
            contains = self.file_contains_keyword(real_file_path)
            if contains:
                self.increase_count_in_dict(dir_path, count_dict)
            file_dict[real_file_path] = contains

    """Prints count for each subdir.
    :param dict_to_print: Dictionary which holds count of each subdir.
    """
    def print_count_of_subdirs(self, dict_to_print):
        print "Result Data: {}".format(dict_to_print)

    """Shows plot of count of each subdir.
    :param dict_to_print: Dictionary which holds count of each subdir.
    """
    def show_graph(self, dict_to_print):        
        plot.bar(range(len(dict_to_print)), dict_to_print.values(), align='center')
        plot.xticks(range(len(dict_to_print)), dict_to_print.keys())
        plot.xlabel('Subdir')
        plot.ylabel('Count')
        plot.title('Subdir - Count Graph')
        plot.show()

    """Searches file for the keyword and returns search result.
    :param file_path: File path.
    :return : True if keyword exists in the file, otherwise False.
    """
    def file_contains_keyword(self, file_path):
        return_value = False
        try:
            f = open(file_path, 'r+')
            m = mmap.mmap(f.fileno(), 0, access = mmap.ACCESS_READ)
            if self.compiled_regexp.search(m) is not None:
                return_value = True
        except Exception as e:
            print e
        finally:
            f.close()
            m.close()
        return return_value
    
    """Increase the count of the corresponsing subdir in the count dict.
    :param dir_path: Current directory path (e.g. a/b/c).
    :param count_dict: Dictionary which holds count of each sub.
    """
    def increase_count_in_dict(self, dir_path, count_dict):
        if count_dict.get(dir_path) is not None:
            count_dict[dir_path] += 1
        else:
            count_dict[dir_path] = 1
    
    """Initialize count for the directory.
    :param dir_path: Current directory path (e.g. a/b/c).
    :param count_dict: Dictionary which holds count of each sub.
    """
    def init_dir_count_in_dict(self, dir_path, count_dict):
        if count_dict.get(dir_path) is None:
            count_dict[dir_path] = 0

    """Converts path to real path to get real path of links.
    :param path: Path to convert.
    :return : Real path.
    """
    @staticmethod
    def to_real_path(path):
        return os.path.realpath(path)
    
    """Returns list of files in a directory.
    :param dir_path: Directory path.
    :return : List of file paths.
    """
    @staticmethod
    def get_files(dir_path):
        try:
            return [os.path.join(dir_path, f) for f in os.listdir(dir_path) if FilesContainKeyword.is_file(os.path.join(dir_path, f))]
        except:
            return []

    """Returns list of directories in a directory.
    :param dir_path: Directory path.
    :return : List of directories.
    """
    @staticmethod
    def get_subdirs(dir_path):
        try:
            return [os.path.join(dir_path, f) for f in os.listdir(dir_path) if FilesContainKeyword.is_dir(os.path.join(dir_path, f))]
        except:
            return []
    
    """Checks if keyword is a valid regular expression.
    :param keyword: Regular expression.
    :return : Result of regexp validation.
    """
    @staticmethod
    def is_keyword_valid(keyword):
        try:
            re.compile(keyword)
            return True
        except re.error:
            return False
    
    """Checks if path is a directory.
    :param path: Path
    :return : True if path is a dir or links to a dir, otherwise False.
    """
    @staticmethod
    def is_dir(path):
        try:
            return os.path.isdir(path)
        except:
            return False
    
    """Checks if path is a file.
    :param path: Path
    :return : True if path is a file or links to a file, otherwise False.
    """
    @staticmethod
    def is_file(path):
        try:
            return os.path.isfile(path)
        except:
            return False

"""
Main function.
"""
if __name__ == "__main__":
    # Checks if any command line paramter is missing or more than 2.
    if len(sys.argv) == 3:
        try:
            fck = FilesContainKeyword(sys.argv[1], sys.argv[2]) # Instance of FilesContainKeyword
            result_count_dict = fck.walk_root_dir() # Walks throught the root dir and returns count dict
            fck.print_count_of_subdirs(result_count_dict) # Print count dict
            fck.show_graph(result_count_dict) # Shows plot graph of count dict
        except Exception as e:
            print e
    else:
        # Show usage to user.
        print 'Usage: apple_coding.py <root_dir> "<keyword>"'
