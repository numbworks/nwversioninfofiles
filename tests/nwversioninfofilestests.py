# GLOBAL MODULES
import unittest
from argparse import ArgumentParser, Namespace
from datetime import datetime, timezone
from parameterized import parameterized
from typing import Any, Callable, Literal, Optional, Tuple
from unittest.mock import Mock, mock_open, patch

# LOCAL MODULES
import sys, os
sys.path.append(os.path.dirname(__file__).replace('tests', 'src'))
from nwversioninfofiles import VersionInfoFileCreator, VersionInfoFileWriter, VersionInfoFileVerifier, CLIManager, CLISTRING

# SUPPORT METHODS
# TEST CLASSES
class VersionInfoFileCreatorTestCase(unittest.TestCase):

    def setUp(self):
        self.vinf_creator : VersionInfoFileCreator = VersionInfoFileCreator()
    def test_createtemplate_shouldreturnexpectedstring_wheninvoked(self) -> None:

        # Arrange
        expected : str = (
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

        # Act
        actual : str = self.vinf_creator._VersionInfoFileCreator__create_template() # type: ignore

        # Assert
        self.assertEqual(expected, actual)
    
    @parameterized.expand([
        ("2.3.14.4355", (2, 3, 14, 4355)),
        ("1.0.0.0", (1, 0, 0, 0)),
        ("10.20.30.40", (10, 20, 30, 40)),
        ("2.3.14", (2, 3, 14, 0)),
        ("1.0.0", (1, 0, 0, 0)),
        ("10.20.30", (10, 20, 30, 0))
    ])
    def test_tokenize_shouldreturnexpectedtuple_wheninvoked(self, file_version : str, expected : Tuple[int, int, int, int]) -> None:

        # Arrange
        # Act
        actual : Tuple[int, int, int, int] = self.vinf_creator._VersionInfoFileCreator__tokenize(file_version = file_version)  # type: ignore

        # Assert
        self.assertEqual(expected, actual)    
    
    @parameterized.expand([
        ("2.3", "The provided 'file_version' ('2.3') is invalid. Supported formats: '2.3.14' or '2.3.14.4355'."),
        ("1", "The provided 'file_version' ('1') is invalid. Supported formats: '2.3.14' or '2.3.14.4355'."),
        ("", "The provided 'file_version' ('') is invalid. Supported formats: '2.3.14' or '2.3.14.4355'."),
        ("1.2.3.4.5", "The provided 'file_version' ('1.2.3.4.5') is invalid. Supported formats: '2.3.14' or '2.3.14.4355'."),
    ])
    def test_tokenize_shouldraiseexception_wheninvalidfileversion(self, file_version : str, expected : str) -> None:

        with self.assertRaises(ValueError) as context:

            # Act
            self.vinf_creator._VersionInfoFileCreator__tokenize(file_version = file_version)  # type: ignore

            # Assert
            self.assertEqual(expected, str(context.exception))
    
    def test_create_shouldreturnexpectedstring_wheninvoked(self) -> None:

        # Arrange
        company_name : str = "numbworks"
        file_description : str = "An app that does something."
        file_version : str = "1.0.0"
        legal_copyright : str = "numbworks"
        original_filename : str = "app.exe"
        product_name : str = "app"

        expected_strings : list[str] = [
            "filevers=(1, 0, 0, 0)",
            "prodvers=(1, 0, 0, 0)",
            "'CompanyName', 'numbworks'",
            "'FileDescription', 'An app that does something.'",
            "'FileVersion', '1.0.0'",
            "'LegalCopyright', 'numbworks'",
            "'OriginalFilename', 'app.exe'",
            "'ProductName', 'app'"
        ]

        # Act
        actual : str = self.vinf_creator.create(
            company_name = company_name,
            file_description = file_description,
            file_version = file_version,
            legal_copyright = legal_copyright,
            original_filename = original_filename,
            product_name = product_name
        )

        # Assert
        for expected_string in expected_strings:
            self.assertIn(expected_string, actual)
class VersionInfoFileWriterTestCase(unittest.TestCase):

    def test_write_shouldreturntrueandaddsuccessmessage_whensuccessful(self) -> None:

        # Arrange
        content : str = "VSVersionInfo(...)"
        output_path : str = "test_folder/version_info_file.txt"
        expected_status : bool = True
        expected_message : str = "The provided Version Info File ('test_folder/version_info_file.txt') has been successfully written to disk."

        with patch("os.makedirs") as mocked_makedirs, \
             patch("builtins.open", mock_open()) as mocked_open:

            # Act            
            vinf_writer : VersionInfoFileWriter = VersionInfoFileWriter()
            actual : bool = vinf_writer.write(content = content, output_path = output_path)

            # Assert
            self.assertEqual(expected_status, actual)
            self.assertEqual(expected_message, vinf_writer.messages[0])
            mocked_makedirs.assert_called_once_with(os.path.dirname(os.path.abspath(output_path)), exist_ok = True)
            mocked_open.assert_called_once_with(output_path, 'w', encoding = 'utf-8')
            mocked_open().write.assert_called_once_with(content)
    def test_write_shouldreturnfalseandadderrormessage_whenoserroroccurs(self) -> None:

        # Arrange
        content : str = "Test content"
        output_path : str = "test_folder/version_info_file.txt"
        exception : OSError = OSError("Permission denied")
        expected_status : bool = False
        expected_message : str = "The provided Version Info File ('test_folder/version_info_file.txt') has not been written to disk ('Permission denied')."

        with patch("os.makedirs", side_effect = exception):

            # Act            
            vinf_writer : VersionInfoFileWriter = VersionInfoFileWriter()
            actual : bool = vinf_writer.write(content = content, output_path = output_path)

            # Assert
            self.assertEqual(expected_status, actual)
            self.assertEqual(expected_message, vinf_writer.messages[0])
class VersionInfoFileVerifierTestCase(unittest.TestCase):

    @parameterized.expand([
        ("Windows", True),
        ("Linux", False),
        ("Darwin", False)
    ])
    def test_iswindows_shouldreturnexpectedboolean_wheninvoked(self, system_name : str, expected : bool) -> None:

        # Arrange
        vinf_verifier : VersionInfoFileVerifier = VersionInfoFileVerifier()

        with patch("platform.system", return_value = system_name):

            # Act
            actual : bool = vinf_verifier._VersionInfoFileVerifier__is_windows()  # type: ignore

            # Assert
            self.assertEqual(expected, actual)

    def test_tryverify_shouldreturntrueandaddsuccessmessage_whenonwindowsandfilecompliant(self) -> None:

        # Arrange
        file_path : str = "test_folder/version_info_file.txt"      
        vinf_verifier : VersionInfoFileVerifier = VersionInfoFileVerifier()
        mocked_lvi : Mock = Mock()

        expected_status : bool = True
        expected_message : str = "The provided Version Info File ('test_folder/version_info_file.txt') is compliant with PyInstaller."

        with patch.object(vinf_verifier, "_VersionInfoFileVerifier__is_windows", return_value = True), \
             patch.dict('sys.modules', {'PyInstaller.utils.win32.versioninfo': Mock(load_version_info_from_text_file = mocked_lvi)}):

            # Act            
            actual : bool = vinf_verifier.try_verify(file_path = file_path)

            # Assert
            self.assertEqual(expected_status, actual)
            self.assertEqual(vinf_verifier.messages[0], expected_message)
            mocked_lvi.assert_called_once_with(file_path)
    def test_tryverify_shouldreturnfalseandadderrormessage_whenonwindowsandfilenotcompliant(self) -> None:

        # Arrange
        file_path : str = "test_folder/version_info_file.txt"      
        vinf_verifier : VersionInfoFileVerifier = VersionInfoFileVerifier()
        exception : Exception = Exception("Invalid format")
        mocked_lvi : Mock = Mock(side_effect = exception)

        expected_status : bool = False
        expected_message : str = "The provided Version Info File ('test_folder/version_info_file.txt') is not compliant with PyInstaller ('Invalid format')."

        with patch.object(vinf_verifier, "_VersionInfoFileVerifier__is_windows", return_value = True), \
             patch.dict('sys.modules', {'PyInstaller.utils.win32.versioninfo': Mock(load_version_info_from_text_file = mocked_lvi)}):

            # Act
            actual : bool = vinf_verifier.try_verify(file_path = file_path)

            # Assert
            self.assertEqual(expected_status, actual)
            self.assertEqual(vinf_verifier.messages[0], expected_message)
            mocked_lvi.assert_called_once_with(file_path)
    def test_tryverify_shouldreturnfalseandaddmessage_whennotonwindows(self) -> None:

        # Arrange
        file_path : str = "test/version_info.txt"      
        vinf_verifier : VersionInfoFileVerifier = VersionInfoFileVerifier()

        expected_status : bool = False
        expected_message : str = "This library is not running on Windows, the verification is not possible."

        with patch.object(vinf_verifier, "_VersionInfoFileVerifier__is_windows", return_value = False):

            # Act
            actual : bool = vinf_verifier.try_verify(file_path = file_path)

            # Assert
            self.assertEqual(expected_status, actual)
            self.assertEqual(vinf_verifier.messages[0], expected_message)
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