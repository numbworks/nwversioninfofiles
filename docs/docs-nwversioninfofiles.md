# nwversioninfofiles
Contact: numbworks@gmail.com

## Revision History

| Date | Author | Description |
|---|---|---|
| 2026-01-21 | numbworks | Created. |
| 2026-01-24 | numbworks | Last update. |

## Introduction

`nwversioninfofiles` is an application that facilitates the creation of Version Info Files for PyInstaller.

## Getting Started (as a user)

To run this application as a user, open your terminal application and run one of these commands:

- `pip install --extra-index-url https://numbworks.github.io nwversioninfofiles==1.0.0`
- `pip install "https://github.com/numbworks/nwversioninfofiles/archive/refs/tags/v1.0.0.zip#subdirectory=src"`
- `pip install 'git+https://github.com/numbworks/nwversioninfofiles.git@v1.0.0#egg=nwversioninfofiles&subdirectory=src'`

## Getting Started (as a developer)

To run this application as a developer:

1. Download and install [Visual Studio Code](https://code.visualstudio.com/Download);
2. Download and install [Docker](https://www.docker.com/products/docker-desktop/);
3. Download and install [Git](https://git-scm.com/downloads);
4. Open your terminal application of choice and type the following commands:

    ```
    mkdir nwversioninfofiles
    cd nwversioninfofiles
    git clone https://github.com/numbworks/nwversioninfofiles.git
    ```

5. Launch Visual Studio Code and install the following extensions:

    - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    - [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
    - [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)
    - [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
    - [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)

6. In order for the Jupyter Notebook to automatically detect changes in the underlying library, click on <ins>File</ins> > <ins>Preferences</ins> > <ins>Settings</ins> and change the following setting as below:

    ```
    "jupyter.runStartupCommands": [
        "%load_ext autoreload", "%autoreload 2"
    ]
    ```

7. In order for Pylance to perform type checking, set the `python.analysis.typeCheckingMode` setting to `basic`;
8. Click on <ins>File</ins> > <ins>Open folder</ins> > `nwversioninfofiles`;
9. Click on <ins>View</ins> > <ins>Command Palette</ins> and type:

    ```
    > Dev Container: Reopen in Container
    ```

10. Wait some minutes for the container defined in the <ins>.devcointainer</ins> folder to be built;
11. Done!

## CLI Arguments

| Argument | Mandatory | Default | Example Value |
|---|---|---|---|
| company_name		| Yes | | "some company name" |
| file_description	| Yes | | "some description" |
| file_version		| Yes | | "1.0.0.0" or "1.0.0" |
| legal_copyright	| Yes | | "numbworks" |
| original_filename	| Yes | | "some filename.exe" |
| product_name		| Yes | | "some product name" |
| output_path		| No | <current_folder>/<original_filename.txt> | "/mnt/c/versioninfofile.txt" |
| verify			| No | False | |

Examples:

```cmd
python.exe -m nwversioninfofiles.py \
	--company_name "numbworks" \
	--legal_copyright "numbworks" \
	--file_description "An app that does something." \
	--file_version "1.0.0" \
	--product_name "numbworks" \
	--original_filename "app.exe" \
```

```cmd
python.exe -m nwversioninfofiles.py \
	--company_name "numbworks" \
	--legal_copyright "numbworks" \
	--file_description "An app that does something." \
	--file_version "1.0.0" \
	--product_name "numbworks" \
	--original_filename "app.exe" \
	--output_path "version_info_file.txt" \
```

```cmd
python.exe -m nwversioninfofiles.py \
	--company_name "numbworks" \
	--legal_copyright "numbworks" \
	--file_description "An app that does something." \
	--file_version "1.0.0" \
	--product_name "numbworks" \
	--original_filename "app.exe" \
	--output_path "version_info_file.txt" \
	--verify
```

## Appendix - Architecture

A primary difference between `pyinstaller` and `nuitka` is how they handle metadata: `pyinstaller` relies on Version Info Files, which are difficult to modify on-the-fly, whereas `nuitka` uses high-level command-line flags. Furthermore, `pyinstaller` provides no way to verify these files before the build begins.

`nwversioninfofiles` fills the gap between both by simplifying metadata management/validation, which provides even more value when the user needs to integrate both tools in the same CI/CD pipeline.

![Architectural-Overview](Diagrams/Architectural-Overview.png)

## Appendix - Example files

Here three examples of Version Info Files and the template used by this library:

1. [versioninfofile_example1.txt](ExampleFiles/versioninfofile_example1.txt)
2. [versioninfofile_example2.txt](ExampleFiles/versioninfofile_example2.txt)
3. [versioninfofile_example3.txt](ExampleFiles/versioninfofile_example3.txt)
4. [versioninfofile_template.txt](ExampleFiles/versioninfofile_template.txt)

## Markdown Toolset

Suggested toolset to view and edit this Markdown file:

- [Visual Studio Code](https://code.visualstudio.com/)
- [Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)
- [Markdown PDF](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf)