# GLOBAL MODULES
import unittest
from argparse import ArgumentParser, Namespace
from parameterized import parameterized
from typing import Any, Tuple
from unittest.mock import Mock, mock_open, patch

# LOCAL MODULES
import sys, os
sys.path.append(os.path.dirname(__file__).replace('tests', 'src'))
from nwversioninfofiles import VersionInfoFileCreator, VersionInfoFileWriter, VersionInfoFileVerifier
from nwversioninfofilescli import CLIManager, CLISTRING, AsciiBannerManager, _MessageCollection

# SUPPORT METHODS
# TEST CLASSES
class AsciiBannerManagerTestCase(unittest.TestCase):

    def test_validate_shouldraisevalueerror_whenversionisnone(self) -> None:

        # Arrange
        # Act, Assert
        with self.assertRaises(ValueError) as context:
            AsciiBannerManager()._AsciiBannerManager__validate(version = None) # type: ignore

        self.assertEqual(_MessageCollection.provided_version_empty_whitespace(), str(context.exception))
    def test_validate_shouldraisevalueerror_whenversioniswhitespace(self) -> None:

        # Arrange
        version : str = " "

        # Act, Assert
        with self.assertRaises(ValueError) as context:
            AsciiBannerManager()._AsciiBannerManager__validate(version = version) # type: ignore

        self.assertEqual(_MessageCollection.provided_version_empty_whitespace(), str(context.exception))
    def test_createfiglet_shouldreturnexpectedmaxlength_wheninvoked(self) -> None:

        # Arrange
        expected : int = 59

        # Act
        _, max_length = AsciiBannerManager()._AsciiBannerManager__create_figlet() # type: ignore

        # Assert
        self.assertEqual(expected, max_length)
    def test_createframe_shouldreturnexpectedtuple_wheninvoked(self) -> None:

        # Arrange
        version : str = "1.0.5"
        max_length : int = 65
        
        expected_top_line : str = "*" * 65
        expected_bottom_line : str = "*" * 46 + "Version: 1.0.5" + "*" * 5

        # Act
        top_line, bottom_line = AsciiBannerManager()._AsciiBannerManager__create_frame(version = version, max_length = max_length) # type: ignore

        # Assert
        self.assertEqual(expected_top_line, top_line)
        self.assertEqual(expected_bottom_line, bottom_line)
    def test_create_shouldcallexpectedprivatemethodsandreturnbanner_wheninvoked(self) -> None:

        # Arrange
        ascii_banner_manager : AsciiBannerManager = AsciiBannerManager()
        version : str = "1.0.5"
        max_lenght : int = 65
        
        figlet_tpl : tuple = ("ascii_art", max_lenght)
        frame_tpl : tuple = ("top_border", "bottom_border")

        with patch.object(ascii_banner_manager, "_AsciiBannerManager__validate") as mocked_validate, \
                patch.object(ascii_banner_manager, "_AsciiBannerManager__create_figlet", return_value = figlet_tpl) as mocked_create_figlet, \
                patch.object(ascii_banner_manager, "_AsciiBannerManager__create_frame", return_value = frame_tpl) as mocked_create_frame:

            # Act
            actual : str = ascii_banner_manager.create(version = version)

            # Assert
            mocked_validate.assert_called_once_with(version)
            mocked_create_figlet.assert_called_once()
            mocked_create_frame.assert_called_once_with(version, max_lenght)

            self.assertIn("top_border", actual)
            self.assertIn("ascii_art", actual)
            self.assertIn("bottom_border", actual)
class CLIManagerTestCase(unittest.TestCase):

    def setUp(self):

        self.company_name : str = "numbworks"
        self.file_description : str = "An app that does something."
        self.file_version : str = "1.0.0"
        self.legal_copyright : str = "numbworks"
        self.original_filename : str = "app.exe"
        self.product_name : str = "app"

        self.output_path : str = "test_folder/version_info_file.txt"
        self.verify : bool = True

        self.default_output_path : str = "default_folder/version_info_file.txt"
        self.default_verify : bool = False

        self.content : str = "Some content"

        self.namespace_all : Namespace = Namespace(
            company_name = self.company_name,
            file_description = self.file_description,
            file_version = self.file_version,
            legal_copyright = self.legal_copyright,
            original_filename = self.original_filename,
            product_name = self.product_name,
            output_path = self.output_path,
            verify = self.verify
        )
        self.namespace_only_mandatory : Namespace = Namespace(
            company_name = self.company_name,
            file_description = self.file_description,
            file_version = self.file_version,
            legal_copyright = self.legal_copyright,
            original_filename = self.original_filename,
            product_name = self.product_name,
            output_path = self.default_output_path,
            verify = self.default_verify
        )

        self.args_all : list[str] = [
            "--company_name", self.company_name,
            "--file_description", self.file_description,
            "--file_version", self.file_version,
            "--legal_copyright", self.legal_copyright,
            "--original_filename", self.original_filename,
            "--product_name", self.product_name,
            "--output_path", self.output_path,
            "--verify"
        ]

    def test_initializeparser_shouldaddexpectedarguments_wheninvoked(self) -> None:

        # Arrange
        argument_parser : Mock = Mock(spec = ArgumentParser)

        # Act
        cli_manager : CLIManager = CLIManager(argument_parser = argument_parser)
        cli_manager._CLIManager__initialize_parser()  # type: ignore
        calls : Any = argument_parser.add_argument.call_args_list

        # Assert
        self.assertEqual(argument_parser.add_argument.call_count, 8)
        
        self.assertEqual(calls[0][0][0], CLISTRING.OPTION_COMPANYNAME_FLAGS[0])
        self.assertEqual(calls[0][1]['required'], CLISTRING.OPTION_COMPANYNAME_REQUIRED)
        self.assertEqual(calls[0][1]['help'], CLISTRING.OPTION_COMPANYNAME_HELP)
        
        self.assertEqual(calls[1][0][0], CLISTRING.OPTION_FILEDESCRIPTION_FLAGS[0])
        self.assertEqual(calls[1][1]['required'], CLISTRING.OPTION_FILEDESCRIPTION_REQUIRED)
        self.assertEqual(calls[1][1]['help'], CLISTRING.OPTION_FILEDESCRIPTION_HELP)
        
        self.assertEqual(calls[2][0][0], CLISTRING.OPTION_FILEVERSION_FLAGS[0])
        self.assertEqual(calls[2][1]['required'], CLISTRING.OPTION_FILEVERSION_REQUIRED)
        self.assertEqual(calls[2][1]['help'], CLISTRING.OPTION_FILEVERSION_HELP)
        
        self.assertEqual(calls[3][0][0], CLISTRING.OPTION_LEGALCOPYRIGHT_FLAGS[0])
        self.assertEqual(calls[3][1]['required'], CLISTRING.OPTION_LEGALCOPYRIGHT_REQUIRED)
        self.assertEqual(calls[3][1]['help'], CLISTRING.OPTION_LEGALCOPYRIGHT_HELP)
        
        self.assertEqual(calls[4][0][0], CLISTRING.OPTION_ORIGINALFILENAME_FLAGS[0])
        self.assertEqual(calls[4][1]['required'], CLISTRING.OPTION_ORIGINALFILENAME_REQUIRED)
        self.assertEqual(calls[4][1]['help'], CLISTRING.OPTION_ORIGINALFILENAME_HELP)
        
        self.assertEqual(calls[5][0][0], CLISTRING.OPTION_PRODUCTNAME_FLAGS[0])
        self.assertEqual(calls[5][1]['required'], CLISTRING.OPTION_PRODUCTNAME_REQUIRED)
        self.assertEqual(calls[5][1]['help'], CLISTRING.OPTION_PRODUCTNAME_HELP)
        
        self.assertEqual(calls[6][0][0], CLISTRING.OPTION_OUTPUTPATH_FLAGS[0])
        self.assertEqual(calls[6][1]['required'], CLISTRING.OPTION_OUTPUTPATH_REQUIRED)
        self.assertEqual(calls[6][1]['help'], CLISTRING.OPTION_OUTPUTPATH_HELP)
        
        self.assertEqual(calls[7][0][0], CLISTRING.OPTION_VERIFY_FLAGS[0])
        self.assertEqual(calls[7][1]['required'], CLISTRING.OPTION_VERIFY_REQUIRED)
        self.assertEqual(calls[7][1]['help'], CLISTRING.OPTION_VERIFY_HELP)
        self.assertEqual(calls[7][1]['action'], CLISTRING.OPTION_VERIFY_ACTION)
    def test_getdefaultoutputpath_shouldreturnexpectedstring_wheninvoked(self) -> None:

        # Arrange
        cli_manager : CLIManager = CLIManager()
        original_filename : str = "myapp.exe"
        expected : str = "/current/directory/myapp.txt"
        
        with patch("os.getcwd", return_value = "/current/directory"), \
             patch("os.path.splitext", return_value = ("myapp", ".exe")):
            
            # Act
            actual : str = cli_manager._CLIManager__get_default_output_path(original_filename = original_filename)  # type: ignore

            # Assert
            self.assertEqual(expected, actual)
    def test_printmessages_shouldprintmessagetuple_wheninvoked(self) -> None:

        # Arrange
        print_function : Mock = Mock()      
        messages : tuple[str, ...] = tuple(["Message 1", "Message 2", "Message 3"])

        # Act
        cli_manager : CLIManager = CLIManager(print_function = print_function)        
        cli_manager._CLIManager__print_messages(messages = messages)  # type: ignore

        # Assert
        self.assertEqual(print_function.call_count, 3)
        print_function.assert_any_call(messages[0])
        print_function.assert_any_call(messages[1])
        print_function.assert_any_call(messages[2])

    def test_trydispatch_shouldperformexpectedcalls_whenallarguments(self) -> None:

        # Arrange
        vinf_creator : Mock = Mock(spec = VersionInfoFileCreator)
        vinf_creator.create.return_value = self.content

        vinf_writer : Mock = Mock(spec = VersionInfoFileWriter)
        vinf_writer.write.return_value = True
        vinf_writer.messages = ()

        vinf_verifier : Mock = Mock(spec = VersionInfoFileVerifier)
        vinf_verifier.try_verify.return_value = True
        vinf_verifier.messages = ()

        print_function : Mock = Mock()
               
        cli_manager : CLIManager = CLIManager(
            vinf_creator = vinf_creator,
            vinf_writer = vinf_writer,
            vinf_verifier = vinf_verifier,
            print_function = print_function
        )

        # Act
        with patch.object(cli_manager, "_CLIManager__get_default_output_path", return_value = self.default_output_path) as mocked_get_path, \
             self.assertRaises(SystemExit) as context:
                cli_manager._CLIManager__try_dispatch(namespace = self.namespace_all)  # type: ignore

        # Assert
        vinf_creator.create.assert_called_once_with(
            company_name = self.company_name,
            file_description = self.file_description,
            file_version = self.file_version,
            legal_copyright = self.legal_copyright,
            original_filename = self.original_filename,
            product_name = self.product_name
        )
        
        mocked_get_path.assert_called_once_with(self.original_filename)
        vinf_writer.write.assert_called_once_with(content = self.content, output_path = self.output_path)
        vinf_verifier.try_verify.assert_called_once_with(self.output_path)
        print_function.assert_not_called()

        self.assertEqual(context.exception.code, 0)
    def test_trydispatch_shouldperformexpectedcalls_whenallargumentsbutwriterfails(self) -> None:

        # Arrange
        vinf_creator : Mock = Mock(spec = VersionInfoFileCreator)
        vinf_creator.create.return_value = self.content

        vinf_writer : Mock = Mock(spec = VersionInfoFileWriter)
        vinf_writer.write.return_value = False
        vinf_writer.messages = tuple(["Some writing error message."])

        vinf_verifier : Mock = Mock(spec = VersionInfoFileVerifier)       
        print_function : Mock = Mock()
               
        cli_manager : CLIManager = CLIManager(
            vinf_creator = vinf_creator,
            vinf_writer = vinf_writer,
            vinf_verifier = vinf_verifier,
            print_function = print_function
        )

        # Act  
        with patch.object(cli_manager, "_CLIManager__get_default_output_path", return_value = self.default_output_path) as mocked_get_path, \
             self.assertRaises(SystemExit) as context:
                cli_manager._CLIManager__try_dispatch(namespace = self.namespace_all)  # type: ignore

        # Assert
        vinf_creator.create.assert_called_once_with(
            company_name = self.company_name,
            file_description = self.file_description,
            file_version = self.file_version,
            legal_copyright = self.legal_copyright,
            original_filename = self.original_filename,
            product_name = self.product_name
        )
        
        mocked_get_path.assert_called_once_with(self.original_filename)
        vinf_writer.write.assert_called_once_with(content = self.content, output_path = self.output_path)
        print_function.assert_any_call("Some writing error message.")
        vinf_verifier.try_verify.assert_not_called()

        self.assertEqual(context.exception.code, 1)
    def test_trydispatch_shouldperformexpectedcalls_whenallargumentsbutverifierfails(self) -> None:

        # Arrange
        vinf_creator : Mock = Mock(spec = VersionInfoFileCreator)
        vinf_creator.create.return_value = self.content

        vinf_writer : Mock = Mock(spec = VersionInfoFileWriter)
        vinf_writer.write.return_value = True  # Writer succeeds
        vinf_writer.messages = ()

        exception : Exception = Exception("Invalid format")
        error_message : str = f"The provided Version Info File ('{self.output_path}') is not compliant with PyInstaller '({exception})'."
        
        vinf_verifier : Mock = Mock(spec = VersionInfoFileVerifier)
        vinf_verifier.try_verify.return_value = False
        vinf_verifier.messages = tuple([error_message])

        print_function : Mock = Mock()
               
        cli_manager : CLIManager = CLIManager(
            vinf_creator = vinf_creator,
            vinf_writer = vinf_writer,
            vinf_verifier = vinf_verifier,
            print_function = print_function
        )

        # Act
        with patch.object(cli_manager, "_CLIManager__get_default_output_path", return_value = self.default_output_path) as mocked_get_path, \
             self.assertRaises(SystemExit) as context:
                cli_manager._CLIManager__try_dispatch(namespace = self.namespace_all)  # type: ignore

        # Assert          
        vinf_creator.create.assert_called_once_with(
            company_name = self.company_name,
            file_description = self.file_description,
            file_version = self.file_version,
            legal_copyright = self.legal_copyright,
            original_filename = self.original_filename,
            product_name = self.product_name
        )
        
        mocked_get_path.assert_called_once_with(self.original_filename)
        vinf_writer.write.assert_called_once_with(content = self.content, output_path = self.output_path)
        vinf_verifier.try_verify.assert_called_once_with(self.output_path)
        print_function.assert_called_once_with(error_message)

        self.assertEqual(context.exception.code, 1)
    def test_trydispatch_shouldperformexpectedcalls_whenonlyoptionalarguments(self) -> None:

        # Arrange
        vinf_creator : Mock = Mock(spec = VersionInfoFileCreator)
        vinf_creator.create.return_value = self.content

        vinf_writer : Mock = Mock(spec = VersionInfoFileWriter)
        vinf_writer.write.return_value = True
        vinf_writer.messages = ()

        vinf_verifier : Mock = Mock(spec = VersionInfoFileVerifier)
        vinf_verifier.try_verify.return_value = True
        vinf_verifier.messages = ()

        print_function : Mock = Mock()
               
        cli_manager : CLIManager = CLIManager(
            vinf_creator = vinf_creator,
            vinf_writer = vinf_writer,
            vinf_verifier = vinf_verifier,
            print_function = print_function
        )

        # Act
        with patch.object(cli_manager, "_CLIManager__get_default_output_path", return_value = self.default_output_path) as mocked_get_path, \
             self.assertRaises(SystemExit) as context:
                cli_manager._CLIManager__try_dispatch(namespace = self.namespace_only_mandatory)  # type: ignore

        # Assert
        vinf_creator.create.assert_called_once_with(
            company_name = self.company_name,
            file_description = self.file_description,
            file_version = self.file_version,
            legal_copyright = self.legal_copyright,
            original_filename = self.original_filename,
            product_name = self.product_name
        )
        
        mocked_get_path.assert_called_once_with(self.original_filename)
        vinf_writer.write.assert_called_once_with(content = self.content, output_path = self.default_output_path)
        vinf_verifier.try_verify.assert_not_called()
        print_function.assert_not_called()

        self.assertEqual(context.exception.code, 0)

    def test_parse_shouldexitwithcodezero_wheninitializeparserandtrydispatchsucceed(self) -> None:

        # Arrange
        argument_parser : Mock = Mock(spec = ArgumentParser)
        argument_parser.parse_args.return_value = self.namespace_all
        
        cli_manager : CLIManager = CLIManager(argument_parser = argument_parser)

        # Act
        with patch.object(cli_manager, "_CLIManager__initialize_parser") as mocked_initialize_parser, \
             patch.object(cli_manager, "_CLIManager__try_dispatch", side_effect = lambda x : sys.exit(0)) as mocked_try_dispatch, \
             self.assertRaises(SystemExit) as context:
                cli_manager.parse(args = self.args_all)

        # Assert
        argument_parser.parse_args.assert_called_once_with(self.args_all)
        mocked_initialize_parser.assert_called_once()
        mocked_try_dispatch.assert_called_once_with(self.namespace_all)
        self.assertEqual(context.exception.code, 0)
    def test_parse_shouldexitwithcodeone_wheninitializeparserraisesexception(self) -> None:

        # Arrange
        argument_parser : Mock = Mock(spec = ArgumentParser)
        print_function : Mock = Mock()
              
        cli_manager : CLIManager = CLIManager(
            argument_parser = argument_parser,
            print_function = print_function
        )

        exception : Exception = Exception("Failed to initialize parser")

        # Act
        with patch.object(cli_manager, "_CLIManager__initialize_parser", side_effect = exception):
            with self.assertRaises(SystemExit) as context:
                cli_manager.parse(args = self.args_all)

        # Assert
        argument_parser.parse_args.assert_not_called()
        print_function.assert_called_once_with("Failed to initialize parser")
        self.assertEqual(context.exception.code, 1)

# MAIN
if __name__ == "__main__":
    result = unittest.main(argv=[''], verbosity=3, exit=False)