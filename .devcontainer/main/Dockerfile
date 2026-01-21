FROM python:3.12.5-bookworm

# OTHERS
RUN pip install --upgrade pip==25.3

# MAKEFILE
RUN pip install mypy==1.13.0
RUN pip install pandas-stubs==2.2.3.241009
RUN pip install types-requests==2.32.0.20241016
RUN pip install radon==6.0.1
RUN pip install pylint==3.3.3
RUN pip install 'git+https://github.com/numbworks/nwpackageversions.git@v1.8.1#egg=nwpackageversions&subdirectory=src'
RUN pip install 'git+https://github.com/numbworks/nwcommitaverages.git@v1.0.0#egg=nwcommitaverages&subdirectory=src'
RUN pip install 'git+https://github.com/numbworks/nwdocstringchecking.git@v1.0.0#egg=nwdocstringchecking&subdirectory=src'

# UNIT TESTING
RUN pip install coverage==7.6.4
RUN pip install parameterized==0.9.0
RUN wget https://github.com/jgm/pandoc/releases/download/3.4/pandoc-3.4-1-amd64.deb \
    && dpkg -i pandoc-3.4-1-amd64.deb \
    && rm -f pandoc-3.4-1-amd64.deb

# LIBRARY DEPENDENCIES
RUN pip install pyinstaller==6.11.1