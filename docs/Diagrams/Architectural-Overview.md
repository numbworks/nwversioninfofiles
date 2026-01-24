```cmd
python.exe -m nuitka \
    --company-name="numbworks" \
    --copyright="numbworks" \
    --file-description="An app that does something." \
    --file-version="1.0.0" \
    --product-name="app" \
    --product-version="1.0.0" \
    --trademark="numbworks" \
    --windows-icon-from-ico="app.ico" \
    ... \
    app.py
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

```cmd
python.exe -m PyInstaller \
    --version-file="version_info_file.txt" \
    --icon="app.ico" \
    ... \
    app.py
```