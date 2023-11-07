#!/usr/bin/python3
"""
Provides command-line interface to accessing the `TeX for the Impatient' PDF files.
"""

import sys
import argparse
from pathlib import Path
import re
import logging


SECTION_LIST = (
    "concepts",
    "genops",
    "math",
    "miscellany",
    "modes",
    "pages",
    "paras",
    )

def texdict(pattern=None, sections=None):
    """
    Allows user to look up TeX commands by patterns and section.
    """
    if (pattern, section) == (None, None):
        logging.warning(
            "Uh-oh. The 'texdict' function ran by mistake.\n"
            "Ideally, it should not run if both the pattern and section are blank."
            )
        # return help message
        return None
    if pattern == None:
        pattern = ".*"
    elif sections == None:
        sections = SECTION_LIST
    # search by section, then by pattern, if any.
    search_results = []
    logging.info("Now searching 'output'/* for sections that are in '%s'.", sections)
    for outdir in Path("output").iterdir():
        if outdir.name not in sections:
            logging.info("'%s' is not in 'sections' parameter. Skipping..", outdir.name)
            continue
        logging.info("'%s' is in 'sections' parameter. Searching.", outdir.name)
        for outfile in outdir.iterdir():
            if re.search(pattern, outfile.name) is None:
                logging.info("'%s' is not matched by specified 'pattern', '%s'. Skipping.", outdir.name)
                continue
            logging.info("'%s' is matched by specified 'pattern', '%s'. Appending.", outdir.name)
            search_results.append("/".join([outdir.name, outfile.name]))
    logging.info("%d results found with pattern='%s', sections='%s'", len(search_results),  pattern, sections)
    if search_results:
        # print result-set
        result_report = f"Your search for the pattern: {pattern}\nin the sections: {','.join(sections)}\nyielded the following results:"
        print(result_report)
        # print border
        print("=" * max([len(line) for line in result_report.splitlines()]))
        for index, sresult in enumerate(search_results):
            print(f"{index}: {sresults}")
        # receive user input
        user_input = ""
        while user_input not in [str(index) for index in range(len(search_results))]:
            user_input = input("Please make a selection: ")
        # open PDF: f"output/{search_results[int(user_input)]}"
        logging.info("Now opening PDF file: 'output/%s'.", search_results[int(user_input)])
    else:
        result_report = f"Your search for the pattern: {pattern}\nin the sections: {','.join(sections)}\nyielded no results."
        print(result_report)

parser = argparse.ArgumentParser(
        prog="texdict",
        description="Search for a command to look up by pattern, by section, or by both.",
        epilog="Have a question?\nhttps://github.com/gchang12",
    )

def texdict(pattern=None, sections=None):
    print("pattern:", pattern)
    print("sections:", sections)

parser.set_defaults(func=texdict)

parser.add_argument("-sections",
        metavar="sections",
        type=str,
        nargs="*",
        choices = SECTION_LIST,
        required=False,
        action="extend",
        help="specify which sections to search (default: <all>)",
    )

parser.add_argument("pattern",
        metavar="pattern",
        type=str,
        nargs="?",
        action="store",
        help="specify the pattern to search for in the list of control sequences (default: .*)",
    )

if __name__ == '__main__':
    parsed_args = parser.parse_args()
    td_args = (parsed_args.pattern, parsed_args.sections)
    if td_args == (None, None):
        parser.parse_args(["-h"])
    else:
        texdict(*td_args)