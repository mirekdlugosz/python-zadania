#!/usr/bin/env python3

import argparse
import os.path

import process_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='+', help="path to file with PESEL numbers to process")
    parser.add_argument("--verbose", help="print invalid PESEL numbers",
            action="store_true")
    args = parser.parse_args()

    report = {
            "files_number": len(args.file),
            "processed": 0,
            "valid": 0,
            "invalid": 0
            }
    report_message = "Processed {files_number} file(s), {processed} PESEL numbers ({valid} valid, {invalid} invalid)"
    invalid_message = "{file}: invalid PESEL found at line {line_number}: {line}"

    for file_arg in args.file:
        file_arg = os.path.abspath(file_arg)
        try:
            single_file_report = process_file.pesel(file_arg)
        except OSError as e:
            print(e)
            continue

        report["processed"] += single_file_report["processed"]
        report["valid"] += single_file_report["valid"]
        report["invalid"] += single_file_report["invalid"]

        if args.verbose:
            for line_number, line in single_file_report["invalid_list"]:
                print(invalid_message.format(**{
                    "file": file_arg,
                    "line_number": line_number,
                    "line": line
                    }))

    print(report_message.format(**report))
