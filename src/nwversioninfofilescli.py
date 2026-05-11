'''
    A CLI application that facilitates the creation of Version Info Files for PyInstaller.
'''

# GLOBAL MODULES
import platform
import os
import sys
from argparse import ArgumentParser, Namespace
from typing import Callable, Final, Iterable, Optional, Tuple

# LOCAL/NW MODULES
from nwversioninfofiles import VersionInfoFileCreator, VersionInfoFileWriter, VersionInfoFileVerifier

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
# CLASSES
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
def main(): pass

if __name__ == "__main__":
    main()