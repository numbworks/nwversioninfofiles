'''
A library that facilitates the creation of Version Info Files for PyInstaller.

Alias: nwvinf
'''

# GLOBAL MODULES
import platform
import os
import sys
from argparse import ArgumentParser, Namespace
from typing import Callable, Final, Iterable, Optional, Tuple

# LOCAL/NW MODULES
# GENERIC CLASSES
# CONSTANTS
# STATIC CLASSES
class _MessageCollectionVersionInfoFileCreator():

    '''Collects all the messages used for logging and for the exceptions for VersionInfoFileCreator.'''

    @staticmethod
    def provided_file_version_invalid(file_version : str) -> str:
        return f"The provided 'file_version' ('{file_version}') is invalid. Supported formats: '2.3.14' or '2.3.14.4355'."
class _MessageCollectionVersionInfoFileWriter():

    '''Collects all the messages used for logging and for the exceptions for VersionInfoFileWriter.'''

    @staticmethod
    def provided_vinf_successfully_written(output_path : str) -> str:
        return f"The provided Version Info File ('{output_path}') has been successfully written to disk."
    @staticmethod
    def provided_vinf_not_written(output_path : str, e : Exception) -> str:
        return f"The provided Version Info File ('{output_path}') has not been written to disk ('{e}')."
class _MessageCollectionVersionInfoFileVerifier():

    '''Collects all the messages used for logging and for the exceptions for VersionInfoFileVerifier.'''

    @staticmethod
    def this_library_not_running_on_windows() -> str:
        return "This library is not running on Windows, the verification is not possible."
    @staticmethod
    def provided_vinf_compliant(file_path : str) -> str:
        return f"The provided Version Info File ('{file_path}') is compliant with PyInstaller."
    @staticmethod
    def provided_vinf_not_compliant(file_path : str, e : Exception) -> str:
        return f"The provided Version Info File ('{file_path}') is not compliant with PyInstaller ('{e}')."
class _MessageCollection(
        _MessageCollectionVersionInfoFileCreator,
        _MessageCollectionVersionInfoFileWriter,
        _MessageCollectionVersionInfoFileVerifier
):

    '''Collects all the messages used for logging and for the exceptions.'''

# CLASSES
class VersionInfoFileCreator:

    '''Collects all the logic related to the creation of a Version Info File.'''
    
    def __create_template(self) -> str:

        '''Creates the template for a Version Info File.'''

        return (
            "VSVersionInfo(\n"
            "  ffi=FixedFileInfo(\n"
            "    filevers=(MAJOR, MINOR, PATCH, BUILD),\n"
            "    prodvers=(MAJOR, MINOR, PATCH, BUILD),\n"
            "    mask=0x3f,\n"
            "    flags=0x0,\n"
            "    OS=0x40004,\n"
            "    fileType=0x1,\n"
            "    subtype=0x0,\n"
            "    date=(0, 0)\n"
            "    ),\n"
            "  kids=[\n"
            "    StringFileInfo(\n"
            "      [\n"
            "      StringTable(\n"
            "        '040904B0',\n"
            "        [StringStruct('CompanyName', 'COMPANY_NAME'),\n"
            "        StringStruct('FileDescription', 'FILE_DESCRIPTION'),\n"
            "        StringStruct('FileVersion', 'FILE_VERSION'),\n"
            "        StringStruct('InternalName', 'ORIGINAL_FILENAME'),\n"
            "        StringStruct('LegalCopyright', 'LEGAL_COPYRIGHT'),\n"
            "        StringStruct('OriginalFilename', 'ORIGINAL_FILENAME'),\n"
            "        StringStruct('ProductName', 'PRODUCT_NAME'),\n"
            "        StringStruct('ProductVersion', 'FILE_VERSION')])\n"
            "      ]), \n"
            "    VarFileInfo([VarStruct('Translation', [1033, 1200])])\n"
            "  ]\n"
            ")"
        )
    def __tokenize(self, file_version : str) -> Tuple[int, int, int, int]:

        '''
            Tokenizes a version string into [major, minor, patch, build] components.

            Supported formats:
                - "2.3.14.4355" -> [2, 3, 14, 4355]
                - "2.3.14" -> [2, 3, 14, 0]
        '''

        tokens : list[str] = file_version.split('.')

        if len(tokens) == 3:
            return (int(tokens[0]), int(tokens[1]), int(tokens[2]), 0)
        elif len(tokens) == 4:
            return (int(tokens[0]), int(tokens[1]), int(tokens[2]), int(tokens[3]))
        else:
            raise ValueError(_MessageCollection.provided_file_version_invalid(file_version))
    
    def create(
        self,
        company_name : str, 
        file_description : str, 
        file_version : str, 
        legal_copyright : str, 
        original_filename : str, 
        product_name : str) -> str:
        
        '''Creates a Version Info File out of the provided arguments.'''

        major, minor, patch, build = self.__tokenize(file_version)

        content : str = self.__create_template()        
        content = content.replace('MAJOR', str(major))
        content = content.replace('MINOR', str(minor))
        content = content.replace('PATCH', str(patch))
        content = content.replace('BUILD', str(build))
        content = content.replace('COMPANY_NAME', company_name)
        content = content.replace('FILE_DESCRIPTION', file_description)
        content = content.replace('FILE_VERSION', file_version)
        content = content.replace('LEGAL_COPYRIGHT', legal_copyright)
        content = content.replace('ORIGINAL_FILENAME', original_filename)
        content = content.replace('PRODUCT_NAME', product_name)
        
        return content
class VersionInfoFileWriter:
    
    '''Collects all the logic related to writing a Version Info File to disk.'''

    @property
    def messages(self) -> tuple[str, ...]:
        '''Returns an immutable copy of messages.'''
        return tuple(self.__messages)

    def __init__(self) -> None:
        self.__messages : list[str] = []

    def write(self, content : str, output_path : str) -> bool:

        '''Returns True if the provided Version Info File has been successfully written to disk.'''

        try:

            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok = True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.__messages.append(_MessageCollection.provided_vinf_successfully_written(output_path))

            return True
            
        except Exception as e:

            self.__messages.append(_MessageCollection.provided_vinf_not_written(output_path, e))
            
            return False
class VersionInfoFileVerifier:
    
    '''Collects all the logic related to the verification of a Version Info File.'''
    
    @property
    def messages(self) -> tuple[str, ...]:
        '''Returns an immutable copy of messages.'''
        return tuple(self.__messages)

    def __init__(self) -> None:
        self.__messages : list[str] = []

    def __is_windows(self) -> bool:

        '''Returns True if this package is running on Windows.'''

        status : bool = (platform.system() == "Windows")
        
        return status
    
    def try_verify(self, file_path: str) -> bool:

        '''
            Returns True if the provided Version Info File can be successfully parsed by PyInstaller.

            Returns False if the library isn't running on Windows or if the Version Info File is not compliant with PyInstaller.
        '''

        if not self.__is_windows():
            
            self.__messages.append(_MessageCollection.this_library_not_running_on_windows())
            
            return False
        
        try:

            from PyInstaller.utils.win32.versioninfo import load_version_info_from_text_file    # type: ignore
            load_version_info_from_text_file(file_path)
            
            self.__messages.append(_MessageCollection.provided_vinf_compliant(file_path))

            return True
        
        except Exception as e:

            self.__messages.append(_MessageCollection.provided_vinf_not_compliant(file_path, e))            

            return False

# MAIN
if __name__ == "__main__":
    pass