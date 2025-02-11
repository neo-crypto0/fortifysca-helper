# fortifysca-helper
# fortifysca-helper

## Description

A Python script that extracts issue paths from Fortify SCA SAST PDF reports and exports them to a text file, streamlining the review process.

## Features

- Parses Fortify SCA SAST PDF reports.
- Extracts issue paths.
- Exports paths to a text file.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/neo-crypto0/fortifysca-helper.git

## Requirements

1. Python >=3.1
2. PyPDF2==3.0.1 library

Use the below command to install library

pip install -r requirements.txt

## Usage

usage: sast_file_path_extracter.py [-h] pdf_path output_path

A tool to process Fortify SCA SAST PDF reports.

positional arguments:
  pdf_path     Path to the PDF file
  output_path  Output file to save processed data

options:
  -h, --help   show this help message and exit