% nwvinf

# NAME
nwvinf - creates Version Info Files for PyInstaller

# SYNOPSIS
**nwvinf** [options]

# DESCRIPTION
**nwvinf** is a CLI application that facilitates the creation of Version Info Files for PyInstaller.

# OPTIONS

**--company_name**
Includes the company name in the Version Info File.

**--file_description**
Includes the file description in the Version Info File.

**--file_version**
Includes the file version in the Version Info File. Supported formats: '1.0.0.0' or '1.0.0'.

**--legal_copyright**
Includes the legal copyright in the Version Info File.

**--original_filename**
Includes the original filename in the Version Info File.

**--product_name**
Includes the product name in the Version Info File.

*--output_path*
Defines the path for the Version Info File. If not provided: './<original_filename>.txt'.

*--verify*
Verifies the Version Info File (Windows-only).

*--help, -h*
Shows help and usage information.

# EXAMPLES

**Run it with only mandatory arguments:**

```text
nwvinf \
	--company_name "numbworks" \
	--legal_copyright "numbworks" \
	--file_description "An app that does something." \
	--file_version "1.0.0" \
	--product_name "numbworks" \
	--original_filename "app.exe"
```

**Run it with `output_path`:**

```text
nwvinf \
	--company_name "numbworks" \
	--legal_copyright "numbworks" \
	--file_description "An app that does something." \
	--file_version "1.0.0" \
	--product_name "numbworks" \
	--original_filename "app.exe" \
	--output_path "version_info_file.txt"
```

**Run it with `verify`:**

```text
nwvinf \
	--company_name "numbworks" \
	--legal_copyright "numbworks" \
	--file_description "An app that does something." \
	--file_version "1.0.0" \
	--product_name "numbworks" \
	--original_filename "app.exe" \
	--verify
```

# AUTHOR
numbworks (numbworks@gmail.com)