# GLOBAL MODULES
import unittest
from argparse import ArgumentParser, Namespace
from datetime import datetime, timezone
from parameterized import parameterized
from typing import Callable, Literal, Optional, Tuple
from unittest.mock import Mock, mock_open, patch

# LOCAL MODULES
import sys, os
sys.path.append(os.path.dirname(__file__).replace('tests', 'src'))
from nwversioninfofiles import VersionInfoFileCreator, VersionInfoFileWriter, VersionInfoFileVerifier

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

        # Arrange
        # Act, Assert
        with self.assertRaises(ValueError) as context:
            self.vinf_creator._VersionInfoFileCreator__tokenize(file_version = file_version)  # type: ignore

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

        # Act
        with patch("os.makedirs") as mocked_makedirs, \
             patch("builtins.open", mock_open()) as mocked_open:
            
            vinf_writer : VersionInfoFileWriter = VersionInfoFileWriter()
            print("test_write_shouldreturntrue")
            print(len(vinf_writer.messages))

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
        mocked_exception : OSError = OSError("Permission denied")
        expected_status : bool = False
        expected_message : str = "The provided Version Info File ('test_folder/version_info_file.txt') has not been written to disk ('Permission denied')."

        # Act
        with patch("os.makedirs", side_effect = mocked_exception):
            
            vinf_writer : VersionInfoFileWriter = VersionInfoFileWriter()
            print("test_write_shouldreturnfalse")
            print(len(vinf_writer.messages))
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

        # Act
        with patch("platform.system", return_value = system_name):
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

        # Act
        with patch.object(vinf_verifier, "_VersionInfoFileVerifier__is_windows", return_value = True), \
                patch.dict('sys.modules', {'PyInstaller.utils.win32.versioninfo': Mock(load_version_info_from_text_file = mocked_lvi)}):
            
            actual : bool = vinf_verifier.try_verify(file_path = file_path)

        # Assert
        self.assertEqual(expected_status, actual)
        self.assertEqual(vinf_verifier.messages[0], expected_message)
        mocked_lvi.assert_called_once_with(file_path)
    def test_tryverify_shouldreturnfalseandadderrormessage_whenonwindowsandfilenotcompliant(self) -> None:

        # Arrange
        file_path : str = "test_folder/version_info_file.txt"      
        vinf_verifier : VersionInfoFileVerifier = VersionInfoFileVerifier()
        mocked_exception : Exception = Exception("Invalid format")
        mocked_lvi : Mock = Mock(side_effect = mocked_exception)

        expected_status : bool = False
        expected_message : str = "The provided Version Info File ('test_folder/version_info_file.txt') is not compliant with PyInstaller ('Invalid format')."

        # Act
        with patch.object(vinf_verifier, "_VersionInfoFileVerifier__is_windows", return_value = True), \
                patch.dict('sys.modules', {'PyInstaller.utils.win32.versioninfo': Mock(load_version_info_from_text_file = mocked_lvi)}):
            
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

        # Act
        with patch.object(vinf_verifier, "_VersionInfoFileVerifier__is_windows", return_value = False):
            actual : bool = vinf_verifier.try_verify(file_path = file_path)

        # Assert
        self.assertEqual(expected_status, actual)
        self.assertEqual(vinf_verifier.messages[0], expected_message)

# MAIN
if __name__ == "__main__":
    result = unittest.main(argv=[''], verbosity=3, exit=False)