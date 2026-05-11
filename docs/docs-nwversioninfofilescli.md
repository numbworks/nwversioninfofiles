# nwversioninfofilescli
Contact: numbworks@gmail.com

## Revision History

| Date | Author | Description |
|---|---|---|
| 2026-05-11 | numbworks | Created. |
| 2026-05-11 | numbworks | Last update (2.0.0). |

## Introduction

`nwversioninfofilescli` is a command-line application built on the top of `nwversioninfofiles`.

## CLI Reference

| Option | Default |
|---|---|
|--company_name     | - |
|--file_description | - |
|--file_version     | - |
|--legal_copyright  | - |
|--original_filename| - |
|--product_name     | - |
|*--output_path*    | `<current_folder>/<original_filename.txt>` |
|*--verify*         | `False` |

## Examples

Run it with only mandatory arguments:

```sh
root@e584fefc57f0:/# alias nwvinf="python src/nwversioninfofilescli.py"
root@e584fefc57f0:/# nwvinf \
	--company_name "numbworks" \
	--legal_copyright "numbworks" \
	--file_description "An app that does something." \
	--file_version "1.0.0" \
	--product_name "numbworks" \
	--original_filename "app.exe"
```

Run it with `output_path`:

```sh
root@e584fefc57f0:/# alias nwvinf="python src/nwversioninfofilescli.py"
root@e584fefc57f0:/# nwvinf \
	--company_name "numbworks" \
	--legal_copyright "numbworks" \
	--file_description "An app that does something." \
	--file_version "1.0.0" \
	--product_name "numbworks" \
	--original_filename "app.exe" \
	--output_path "version_info_file.txt"
```

Run it with `verify`:

```sh
root@e584fefc57f0:/# alias nwvinf="python src/nwversioninfofilescli.py"
root@e584fefc57f0:/# nwvinf \
	--company_name "numbworks" \
	--legal_copyright "numbworks" \
	--file_description "An app that does something." \
	--file_version "1.0.0" \
	--product_name "numbworks" \
	--original_filename "app.exe" \
	--verify
```


## Markdown Toolset

Suggested toolset to view and edit this Markdown file:

- [Visual Studio Code](https://code.visualstudio.com/)
- [Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)
- [Markdown PDF](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf)