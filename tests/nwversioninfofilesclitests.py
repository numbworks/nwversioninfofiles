# GLOBAL MODULES
import unittest
from argparse import ArgumentParser, Namespace
from io import StringIO
from parameterized import parameterized
from typing import Any, Optional
from unittest.mock import MagicMock, Mock, patch

# LOCAL MODULES
import sys, os
sys.path.append(os.path.dirname(__file__).replace('tests', 'src'))
from nwversioninfofiles import VersionInfoFileCreator, VersionInfoFileWriter, VersionInfoFileVerifier
from nwversioninfofilescli import APFactory, CLIManager, CLISTRING, AsciiBannerManager, _MessageCollection

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
class APFactoryTestCase(unittest.TestCase):

    @parameterized.expand([
        CLISTRING.OPTION_COMPANYNAME_FLAGS[0],
        CLISTRING.OPTION_FILEDESCRIPTION_FLAGS[0],
        CLISTRING.OPTION_FILEVERSION_FLAGS[0],
        CLISTRING.OPTION_LEGALCOPYRIGHT_FLAGS[0],
        CLISTRING.OPTION_ORIGINALFILENAME_FLAGS[0],
        CLISTRING.OPTION_PRODUCTNAME_FLAGS[0],
        CLISTRING.OPTION_OUTPUTPATH_FLAGS[0],
        CLISTRING.OPTION_VERIFY_FLAGS[0]
    ])
    def test_create_shouldreturnexpectedargumentparser_wheninvoked(self, flag : str) -> None:

        # Arrange
        # Act
        argument_parser : ArgumentParser = APFactory().create()

        # Assert
        self.assertIsInstance(argument_parser, ArgumentParser)

        arguments : list[str] = []
        for action in argument_parser._actions:
            arguments.extend(action.option_strings)

        self.assertIn(flag, arguments)
    
    def test_create_shouldraiseerror_whenrequiredruntimeargumentismissing(self):

        # Arrange
        args_list : list[str] = CLISTRING.OPTION_OUTPUTPATH_FLAGS
        argument_parser : ArgumentParser = APFactory().create()

        # Act, Assert
        with patch("sys.stderr", new_callable = StringIO):
            with self.assertRaises(SystemExit):
                argument_parser.parse_args(args_list)
class CLIManagerTestCase(unittest.TestCase):

    def test_lognamespace_shouldlogallarguments_wheninvoked(self) -> None:

        # Arrange
        namespace : Namespace = Namespace(file_path = "test.py", exclude = ["test_"])
        logging_function : Mock = Mock()
        cli_manager : CLIManager = CLIManager(logging_function = logging_function)

        # Act
        cli_manager._CLIManager__log_namespace(namespace = namespace) # type: ignore

        # Assert
        self.assertEqual(logging_function.call_count, 3)
        logging_function.assert_any_call("file_path: 'test.py'")
        logging_function.assert_any_call("exclude: '['test_']'")
        logging_function.assert_any_call("")
    def test_logmessages_shouldprintmessagetuple_wheninvoked(self) -> None:

        # Arrange
        logging_function : Mock = Mock()      
        messages : tuple[str, ...] = tuple(["Message 1", "Message 2", "Message 3"])

        # Act
        cli_manager : CLIManager = CLIManager(logging_function = logging_function)        
        cli_manager._CLIManager__log_messages(messages = messages)  # type: ignore

        # Assert
        self.assertEqual(logging_function.call_count, 3)
        logging_function.assert_any_call(messages[0])
        logging_function.assert_any_call(messages[1])
        logging_function.assert_any_call(messages[2])

    def test_getdefaultoutputpath_shouldreturnexpectedstring_wheninvoked(self) -> None:

        # Arrange
        original_filename : str = "myapp.exe"
        expected : str = "/current/directory/myapp.txt"
        
        with patch("os.getcwd", return_value = "/current/directory"), \
             patch("os.path.splitext", return_value = ("myapp", ".exe")):
            
            # Act
            actual : str = CLIManager()._CLIManager__get_default_output_path(original_filename = original_filename)  # type: ignore

            # Assert
            self.assertEqual(expected, actual)    

    def test_runandlog_shouldlogexceptionmessage_whenexceptionisraised(self):

        # Arrange
        expected : str = "Unexpected Error"
        ap_factory : MagicMock = MagicMock(spec = APFactory)
        ap_factory.create.side_effect = Exception(expected)
        
        logging_function : MagicMock = MagicMock()
        
        cli_manager : CLIManager = CLIManager(
            ap_factory = ap_factory,
            logging_function = logging_function
        )

        # Act
        cli_manager.run_and_log()

        # Assert
        logging_function.assert_any_call(expected)
    def test_runandlog_shoulddonothing_whensystemexitoccurs(self):

        # Arrange
        ap_factory : MagicMock = MagicMock(spec = APFactory)
        ap_factory.create.side_effect = SystemExit()
        
        logging_function : MagicMock = MagicMock()
        
        cli_manager : CLIManager = CLIManager(
            ap_factory = ap_factory,
            logging_function = logging_function
        )

        # Act
        cli_manager.run_and_log()

        # Assert
        calls : list[Any] = logging_function.call_args_list

        for call in calls:
            self.assertNotIsInstance(call.args[0], SystemExit)

    @parameterized.expand([
        ("numbworks", "An app that does something.", "1.0.0", "numbworks", "app.exe", "app", None, None),
        ("numbworks", "An app that does something.", "1.0.0", "numbworks", "app.exe", "app", "test_folder/version_info_file.txt", None),
        ("numbworks", "An app that does something.", "1.0.0", "numbworks", "app.exe", "app", "test_folder/version_info_file.txt", True)
    ])
    def test_runandlog_shouldcallexpectedmethods_wheninvoked(
        self, 
        company_name : str,
        file_description : str,
        file_version : str,
        legal_copyright : str,
        original_filename : str,
        product_name : str,
        output_path : Optional[str],
        verify : Optional[bool]) -> None:

        # Arrange
        namespace : Namespace = Namespace(
            company_name = company_name,
            file_description = file_description,
            file_version = file_version,
            legal_copyright = legal_copyright,
            original_filename = original_filename,
            product_name = product_name,
            output_path = output_path,
            verify = verify
        )

        argument_parser : MagicMock = MagicMock(spec = ArgumentParser)
        argument_parser.parse_args.return_value = namespace

        ap_factory : MagicMock = MagicMock(spec = APFactory)
        ap_factory.create.return_value = argument_parser

        vinf_creator : MagicMock = MagicMock(spec = VersionInfoFileCreator)
        vinf_writer : MagicMock = MagicMock(spec = VersionInfoFileWriter)
        vinf_verifier : MagicMock = MagicMock(spec = VersionInfoFileVerifier)

        cli_manager : CLIManager = CLIManager(
            ap_factory = ap_factory,
            vinf_creator = vinf_creator,
            vinf_writer = vinf_writer,
            vinf_verifier = vinf_verifier
        )

        # Act
        with patch.object(cli_manager, "_CLIManager__log_ascii_banner") as log_ascii_banner, \
             patch.object(cli_manager, "_CLIManager__log_namespace") as log_namespace, \
             patch.object(cli_manager, "_CLIManager__get_default_output_path") as get_default_output_path:

            cli_manager.run_and_log()

            # Assert
            log_ascii_banner.assert_called_once()
            ap_factory.create.assert_called_once()
            argument_parser.parse_args.assert_called_once()
            log_namespace.assert_called_once_with(namespace)

            vinf_creator.create.assert_called_once_with(
                company_name = company_name, 
                file_description = file_description, 
                file_version = file_version, 
                legal_copyright = legal_copyright, 
                original_filename = original_filename, 
                product_name = product_name
            )

            if output_path:
                get_default_output_path.assert_called_once_with(original_filename)

            vinf_writer.write.assert_called_once()

            if verify:
                vinf_verifier.try_verify.assert_called_once_with(output_path)

# MAIN
if __name__ == "__main__":
    result = unittest.main(argv=[''], verbosity=3, exit=False)