'''
An application that facilitates the creation of Version Info Files for PyInstaller.

Alias: nwvinfo
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
class CLISTRING:

    '''Collects all the CLI-related strings.'''

    PROGRAM_NAME : Final[str] = "nwvinfo"
    PROGRAM_DESCRIPTION : Final[str] = "A CLI application to create and verify Version Info Files for PyInstaller."

    OPTION_COMPANYNAME_FLAGS : Final[list[str]] = ["--company_name"]
    OPTION_COMPANYNAME_REQUIRED : Final[bool] = True
    OPTION_COMPANYNAME_HELP : Final[str] = "Includes the company name in the Version Info File."

    OPTION_FILEDESCRIPTION_FLAGS : Final[list[str]] = ["--file_description"]
    OPTION_FILEDESCRIPTION_REQUIRED : Final[bool] = True
    OPTION_FILEDESCRIPTION_HELP : Final[str] = "Includes the file description in the Version Info File."

    OPTION_FILEVERSION_FLAGS : Final[list[str]] = ["--file_version"]
    OPTION_FILEVERSION_REQUIRED : Final[bool] = True
    OPTION_FILEVERSION_HELP : Final[str] = "Includes the file version in the Version Info File. Supported formats: '1.0.0.0' or '1.0.0'."

    OPTION_LEGALCOPYRIGHT_FLAGS : Final[list[str]] = ["--legal_copyright"]
    OPTION_LEGALCOPYRIGHT_REQUIRED : Final[bool] = True
    OPTION_LEGALCOPYRIGHT_HELP : Final[str] = "Includes the legal copyright in the Version Info File."

    OPTION_ORIGINALFILENAME_FLAGS : Final[list[str]] = ["--original_filename"]
    OPTION_ORIGINALFILENAME_REQUIRED : Final[bool] = True
    OPTION_ORIGINALFILENAME_HELP : Final[str] = "Includes the original filename in the Version Info File."

    OPTION_PRODUCTNAME_FLAGS : Final[list[str]] = ["--product_name"]
    OPTION_PRODUCTNAME_REQUIRED : Final[bool] = True
    OPTION_PRODUCTNAME_HELP : Final[str] = "Includes the product name in the Version Info File."

    OPTION_OUTPUTPATH_FLAGS : Final[list[str]] = ["--output_path"]
    OPTION_OUTPUTPATH_REQUIRED : Final[bool] = False
    OPTION_OUTPUTPATH_HELP : Final[str] = "Defines the output path for the Version Info File. If not provided: './<original_filename>.txt'."

    OPTION_VERIFY_FLAGS : Final[list[str]] = ["--verify"]
    OPTION_VERIFY_REQUIRED : Final[bool] = False
    OPTION_VERIFY_ACTION : Final[str] = "store_true"
    OPTION_VERIFY_HELP : Final[str] = "Verifies the Version Info File (Windows-only)."

# STATIC CLASSES
class _MessageCollection():

    '''Collects all the messages used for logging and for the exceptions.'''

    # VersionInfoFileCreator
    @staticmethod
    def provided_file_version_invalid(file_version : str) -> str:
        return f"The provided 'file_version' ('{file_version}') is invalid. Supported formats: '2.3.14' or '2.3.14.4355'."
    
    # VersionInfoFileWriter
    @staticmethod
    def provided_vinf_successfully_written(output_path : str) -> str:
        return f"The provided Version Info File ('{output_path}') has been successfully written to disk."
    @staticmethod
    def provided_vinf_not_written(output_path : str, e : Exception) -> str:
        return f"The provided Version Info File ('{output_path}') has not been written to disk ('{e}')."

    # VersionInfoFileVerifier
    @staticmethod
    def this_library_not_running_on_windows() -> str:
        return "This library is not running on Windows, the verification is not possible."
    @staticmethod
    def provided_vinf_compliant(file_path : str) -> str:
        return f"The provided Version Info File ('{file_path}') is compliant with PyInstaller."
    @staticmethod
    def provided_vinf_not_compliant(file_path : str, e : Exception) -> str:
        return f"The provided Version Info File ('{file_path}') is not compliant with PyInstaller ('{e}')."

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
class CLIManager:

    '''Handles CLI argument parsing and corresponding actions.'''
    
    __argument_parser : ArgumentParser
    __vinf_creator : VersionInfoFileCreator
    __vinf_writer : VersionInfoFileWriter
    __vinf_verifier : VersionInfoFileVerifier
    __print_function : Callable[[str], None]

    def __init__(
        self, 
        argument_parser : ArgumentParser = ArgumentParser(
            prog = CLISTRING.PROGRAM_NAME, 
            description = CLISTRING.PROGRAM_DESCRIPTION
        ),
        vinf_creator : VersionInfoFileCreator = VersionInfoFileCreator(),
        vinf_writer : VersionInfoFileWriter = VersionInfoFileWriter(),
        vinf_verifier : VersionInfoFileVerifier = VersionInfoFileVerifier(),
        print_function : Callable[[str], None] = lambda msg : print(msg)
        ) -> None:
        
        self.__argument_parser = argument_parser
        self.__vinf_creator = vinf_creator
        self.__vinf_writer = vinf_writer
        self.__vinf_verifier = vinf_verifier
        self.__print_function = print_function

    def __initialize_parser(self):
        
        self.__argument_parser.add_argument(
            *CLISTRING.OPTION_COMPANYNAME_FLAGS, 
            required = CLISTRING.OPTION_COMPANYNAME_REQUIRED, 
            help = CLISTRING.OPTION_COMPANYNAME_HELP
        )
        self.__argument_parser.add_argument(
            *CLISTRING.OPTION_FILEDESCRIPTION_FLAGS, 
            required = CLISTRING.OPTION_FILEDESCRIPTION_REQUIRED, 
            help = CLISTRING.OPTION_FILEDESCRIPTION_HELP
        )
        self.__argument_parser.add_argument(
            *CLISTRING.OPTION_FILEVERSION_FLAGS, 
            required = CLISTRING.OPTION_FILEVERSION_REQUIRED, 
            help = CLISTRING.OPTION_FILEVERSION_HELP
        )
        self.__argument_parser.add_argument(
            *CLISTRING.OPTION_LEGALCOPYRIGHT_FLAGS, 
            required = CLISTRING.OPTION_LEGALCOPYRIGHT_REQUIRED, 
            help = CLISTRING.OPTION_LEGALCOPYRIGHT_HELP
        )
        self.__argument_parser.add_argument(
            *CLISTRING.OPTION_ORIGINALFILENAME_FLAGS, 
            required = CLISTRING.OPTION_ORIGINALFILENAME_REQUIRED, 
            help = CLISTRING.OPTION_ORIGINALFILENAME_HELP
        )
        self.__argument_parser.add_argument(
            *CLISTRING.OPTION_PRODUCTNAME_FLAGS, 
            required = CLISTRING.OPTION_PRODUCTNAME_REQUIRED, 
            help = CLISTRING.OPTION_PRODUCTNAME_HELP
        )
        self.__argument_parser.add_argument(
            *CLISTRING.OPTION_OUTPUTPATH_FLAGS, 
            required = CLISTRING.OPTION_OUTPUTPATH_REQUIRED, 
            help = CLISTRING.OPTION_OUTPUTPATH_HELP
        )
        self.__argument_parser.add_argument(
            *CLISTRING.OPTION_VERIFY_FLAGS, 
            required = CLISTRING.OPTION_VERIFY_REQUIRED, 
            help = CLISTRING.OPTION_VERIFY_HELP,
            action = CLISTRING.OPTION_VERIFY_ACTION
        )
    def __get_default_output_path(self, original_filename : str) -> str:

        '''
            Example:
                - filename.exe => <current_folder>/filename.txt
        '''

        base_name : str = os.path.splitext(original_filename)[0]
        output_path : str = os.path.join(os.getcwd(), f"{base_name}.txt")

        return output_path
    def __print_messages(self, messages : Iterable[str]) -> None:
                       
        '''Prints messages.'''

        for message in messages:
            self.__print_function(message)
    def __try_dispatch(self, namespace : Namespace) -> None:
        
        '''Attempts to dispatch the provided arguments to the corresponding actions.'''

        content : str = self.__vinf_creator.create(
            company_name = namespace.company_name,
            file_description = namespace.file_description,
            file_version = namespace.file_version,
            legal_copyright = namespace.legal_copyright,
            original_filename = namespace.original_filename,
            product_name = namespace.product_name
        )
        
        output_path : str = self.__get_default_output_path(namespace.original_filename)
        if namespace.output_path:
            output_path = namespace.output_path
        
        if not self.__vinf_writer.write(content = content, output_path = output_path):
            self.__print_messages(self.__vinf_writer.messages)
            sys.exit(1)
        
        if namespace.verify:
            if not self.__vinf_verifier.try_verify(output_path):
                self.__print_messages(self.__vinf_verifier.messages)
                sys.exit(1)

        sys.exit(0)

    def parse(self, args: Optional[list[str]] = None) -> None:

        '''Parses args.'''

        try:

            self.__initialize_parser()

            namespace : Namespace = self.__argument_parser.parse_args(args)
            
            self.__try_dispatch(namespace)

        except Exception as e:
            self.__print_function(str(e))
            sys.exit(1)

# MAIN
if __name__ == "__main__":
    CLIManager().parse()