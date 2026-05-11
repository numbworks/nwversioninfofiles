'''
    A CLI application that facilitates the creation of Version Info Files for PyInstaller.
'''

# GLOBAL MODULES
import os
import sys
from argparse import ArgumentParser, Namespace
from typing import Callable, Final, Iterable, Optional

# LOCAL/NW MODULES
from nwversioninfofiles import VersionInfoFileCreator, VersionInfoFileWriter, VersionInfoFileVerifier
from setupinfo import CLI_DESCRIPTION, PROJECT_VERSION

# GENERIC CLASSES
# CONSTANTS
class CLISTRING:

    '''Collects all the CLI-related strings.'''

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
class _MessageCollectionAsciiBannerManager():

    '''Collects all the messages used for logging and for the exceptions.'''

    @staticmethod
    def provided_version_empty_whitespace() -> str:
        return "The provided 'version' is empty or whitespace."
class _MessageCollection(
        _MessageCollectionAsciiBannerManager):

    '''Collects all the messages used for logging and for the exceptions.'''

# CLASSES
class AsciiBannerManager:

    """Creates the ASCII banner for the provided library's version."""

    def __validate(self, version: str) -> None:
        
        """Validates the provided 'version'."""

        if not version or not version.strip():
            raise ValueError(_MessageCollection.provided_version_empty_whitespace())
    def __create_figlet(self) -> tuple:
        
        """Returns a tuple containing the figlet and its width."""
        
        lines : list[str] = [
            "'##::: ##:'##:::::'##:'##::::'##:'####:'##::: ##:'########:",
            " ###:: ##: ##:'##: ##: ##:::: ##:. ##:: ###:: ##: ##.....::",
            " ####: ##: ##: ##: ##: ##:::: ##:: ##:: ####: ##: ##:::::::",
            " ## ## ##: ##: ##: ##: ##:::: ##:: ##:: ## ## ##: ######:::",
            " ##. ####: ##: ##: ##:. ##:: ##::: ##:: ##. ####: ##...::::",
            " ##:. ###: ##: ##: ##::. ## ##:::: ##:: ##:. ###: ##:::::::",
            " ##::. ##:. ###. ###::::. ###::::'####: ##::. ##: ##:::::::",
            "..::::..:::...::...::::::...:::::....::..::::..::..::::::::"
        ]

        return (os.linesep.join(lines), len(lines[0]))
    def __create_frame(self, version: str, max_length: int) -> tuple:
        
        """Returns a tuple containing the frame of the figlet."""
        
        version_token : str = f"Version: {version}"
        
        margin_length : int = 5
        total_length : int = max_length - len(version_token) - margin_length

        top_line : str = "*" * max_length
        bottom_line : str = f"{top_line[:total_length]}{version_token}{'*' * margin_length}"

        return (top_line, bottom_line)

    def create(self, version: str) -> str:
        
        """Creates the formatted ASCII banner with a versioned frame."""
        
        self.__validate(version)

        figlet, max_length = self.__create_figlet()
        top_line, bottom_line = self.__create_frame(version, max_length)

        ascii_banner : str = os.linesep.join([
            top_line,
            figlet,
            bottom_line,
            ""
        ])

        return ascii_banner
class APFactory():

    '''Encapsulates all the logic related to the creation of a custom instance of argparse.ArgumentParser.'''

    def create(self) -> ArgumentParser:

        '''
            Creates a custom instance of argparse.ArgumentParser.

            The "prog" argument is not provided in order to make the "usage" statement  dynamic:

                usage: nwversioninfofilescli.py ...
        '''

        argument_parser : ArgumentParser = ArgumentParser(description = CLI_DESCRIPTION)

        argument_parser.add_argument(
            *CLISTRING.OPTION_COMPANYNAME_FLAGS, 
            required = CLISTRING.OPTION_COMPANYNAME_REQUIRED, 
            help = CLISTRING.OPTION_COMPANYNAME_HELP
        )
        
        argument_parser.add_argument(
            *CLISTRING.OPTION_FILEDESCRIPTION_FLAGS, 
            required = CLISTRING.OPTION_FILEDESCRIPTION_REQUIRED, 
            help = CLISTRING.OPTION_FILEDESCRIPTION_HELP
        )
        
        argument_parser.add_argument(
            *CLISTRING.OPTION_FILEVERSION_FLAGS, 
            required = CLISTRING.OPTION_FILEVERSION_REQUIRED, 
            help = CLISTRING.OPTION_FILEVERSION_HELP
        )
        
        argument_parser.add_argument(
            *CLISTRING.OPTION_LEGALCOPYRIGHT_FLAGS, 
            required = CLISTRING.OPTION_LEGALCOPYRIGHT_REQUIRED, 
            help = CLISTRING.OPTION_LEGALCOPYRIGHT_HELP
        )
        
        argument_parser.add_argument(
            *CLISTRING.OPTION_ORIGINALFILENAME_FLAGS, 
            required = CLISTRING.OPTION_ORIGINALFILENAME_REQUIRED, 
            help = CLISTRING.OPTION_ORIGINALFILENAME_HELP
        )
        
        argument_parser.add_argument(
            *CLISTRING.OPTION_PRODUCTNAME_FLAGS, 
            required = CLISTRING.OPTION_PRODUCTNAME_REQUIRED, 
            help = CLISTRING.OPTION_PRODUCTNAME_HELP
        )
        
        argument_parser.add_argument(
            *CLISTRING.OPTION_OUTPUTPATH_FLAGS, 
            required = CLISTRING.OPTION_OUTPUTPATH_REQUIRED, 
            help = CLISTRING.OPTION_OUTPUTPATH_HELP
        )
        
        argument_parser.add_argument(
            *CLISTRING.OPTION_VERIFY_FLAGS, 
            required = CLISTRING.OPTION_VERIFY_REQUIRED, 
            help = CLISTRING.OPTION_VERIFY_HELP,
            action = CLISTRING.OPTION_VERIFY_ACTION
        )

        return argument_parser
class CLIManager():

    '''Collects all the logic related to the CLI management.'''

    __ap_factory : APFactory
    __ascii_banner_manager : AsciiBannerManager
    __vinf_creator : VersionInfoFileCreator
    __vinf_writer : VersionInfoFileWriter
    __vinf_verifier : VersionInfoFileVerifier
    __logging_function : Callable[[str], None]

    def __init__(
        self, 
        ap_factory : APFactory = APFactory(), 
        ascii_banner_manager : AsciiBannerManager = AsciiBannerManager(),
        vinf_creator : VersionInfoFileCreator = VersionInfoFileCreator(),
        vinf_writer : VersionInfoFileWriter = VersionInfoFileWriter(),
        vinf_verifier : VersionInfoFileVerifier = VersionInfoFileVerifier(),
        logging_function : Callable[[str], None] = lambda msg : print(msg)) -> None:
        
        self.__ap_factory = ap_factory
        self.__ascii_banner_manager = ascii_banner_manager
        self.__vinf_creator = vinf_creator
        self.__vinf_writer = vinf_writer
        self.__vinf_verifier = vinf_verifier
        self.__logging_function = logging_function

    def __log_ascii_banner(self) -> None:

        '''Logs the ASCII banner.'''

        self.__logging_function(self.__ascii_banner_manager.create(PROJECT_VERSION))
    def __log_namespace(self, namespace : Namespace):

        '''Logs the provided args.'''

        for key, value in vars(namespace).items():
            self.__logging_function(f"{key}: '{value}'")
            
        self.__logging_function("")
    def __log_messages(self, messages : Iterable[str]) -> None:
                       
        '''Prints messages.'''

        for message in messages:
            self.__logging_function(message)

    def __get_default_output_path(self, original_filename : str) -> str:

        '''
            Example:
                - filename.exe => <current_folder>/filename.txt
        '''

        base_name : str = os.path.splitext(original_filename)[0]
        output_path : str = os.path.join(os.getcwd(), f"{base_name}.txt")

        return output_path
    def __run_and_log(self, namespace : Namespace) -> None:
        
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
            self.__log_messages(self.__vinf_writer.messages)
            sys.exit(1)
        
        if namespace.verify:
            if not self.__vinf_verifier.try_verify(output_path):
                self.__log_messages(self.__vinf_verifier.messages)
                sys.exit(1)

        sys.exit(0)

    def run_and_log(self) -> None:

        '''
            Performs the user-provided and log them.
            
            The SystemExit exception occurs when a required option is not provided.
            SystemExit doesn't inherit from Exception and has no message, therefore we need to handle it accordingly.            
        '''

        try:

            self.__log_ascii_banner()

            argument_parser : ArgumentParser = self.__ap_factory.create()
            namespace : Namespace = argument_parser.parse_args()

            self.__log_namespace(namespace)          
            self.__run_and_log(namespace)

        except (Exception, SystemExit) as e:
            
            if not isinstance(e, SystemExit):
                self.__logging_function(str(e))

# MAIN
def main(): CLIManager().run_and_log()

if __name__ == "__main__":
    main()