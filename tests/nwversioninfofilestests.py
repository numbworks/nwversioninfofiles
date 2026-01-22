# GLOBAL MODULES
import unittest
from argparse import ArgumentParser, Namespace
from datetime import datetime, timezone
from parameterized import parameterized
from subprocess import CompletedProcess
from tabulate import tabulate
from typing import Callable, Literal, Optional, Tuple
from unittest.mock import Mock, patch

# LOCAL MODULES
import sys, os
sys.path.append(os.path.dirname(__file__).replace('tests', 'src'))
from nwversioninfofiles import VersionInfoFileCreator

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

# MAIN
if __name__ == "__main__":
    result = unittest.main(argv=[''], verbosity=3, exit=False)