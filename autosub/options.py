#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Defines autosub's command line options.
"""

from __future__ import absolute_import, print_function, unicode_literals

# Import built-in modules
import argparse

# Import third-party modules


# Any changes to the path and your own modules
from autosub import metadata
from autosub import constants


def get_cmd_args():
    """
    Get command-line arguments.
    """
    parser = argparse.ArgumentParser(
        prog=metadata.NAME,
        usage='\n  %(prog)s <input> [options]',
        description=metadata.DESCRIPTION,
        epilog="""Make sure the argument with space is in quotes.
The default value is used 
when the option is not present at the command line.
\"(arg_num)\" means if the option is input,
the number of the arguments is required.\n
Author: {author}
Email: {email}
Bug report: https://github.com/agermanidis/autosub\n
""".format(author=metadata.AUTHOR, email=metadata.AUTHOR_EMAIL),
        add_help=False,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    input_group = parser.add_argument_group(
        'Input Options',
        'Args to control input.')
    speech_group = parser.add_argument_group(
        'Speech Options',
        'Args to control speech-to-text. '
        'If Speech Options not given, it will only generate the times.')
    output_group = parser.add_argument_group(
        'Output Options',
        'Args to control output.')
    options_group = parser.add_argument_group(
        'Other Options',
        'Other options to control.')
    trans_group = parser.add_argument_group(
        'Translation Options',
        'Args to control translation. '
        'If Translation Options not given, '
        'it will only generate the source language subtitles.')
    auditok_group = parser.add_argument_group(
        'Auditok Options',
        'Args to control Auditok '
        'when not using external speech regions control.')
    list_group = parser.add_argument_group(
        'List Options',
        'List all available arguments.')

    input_group.add_argument(
        '-i', '--input',
        nargs='?', metavar='path',
        help="The path to the video/audio/subtitles file "
             "needs to generate subtitles. "
             "When it is a subtitles file, "
             "the program will only translate it. "
             "(arg_num = 1)"
    )

    input_group.add_argument(
        '-sty', '--styles',
        nargs='?', metavar='path',
        const=' ',
        help="""Valid when your output format is \"ass\"/\"ssa\".
                Path to the subtitles file
                which provides \"ass\"/\"ssa\" styles for your output.
                If the arg_num is 0,
                it will use the styles from the
                \"-esr\"/\"--external-speech-regions\".
                More info in \"-sn\"/\"--styles-name\".
                (arg_num = 0 or 1)"""
    )

    input_group.add_argument(
        '-sn', '--styles-name',
        nargs='*', metavar='style-name',
        help="""Valid when your output format is \"ass\"/\"ssa\"
                and \"-sty\"/\"--styles\" is given.
                Adds \"ass\"/\"ssa\" styles to your events.
                If not provided, events will use the first one
                from the file.
                If the arg_num is 1, events will use the 
                specific style from the arg of \"-sty\"/\"--styles\".
                If the arg_num is 2, src language events use the first.
                Dst language events use the second.               
                (arg_num = 1 or 2)"""
    )

    input_group.add_argument(
        '-er', '--ext-regions',
        nargs='?', metavar='path',
        help="""Path to the subtitles file
                which provides external speech regions,
                which is one of the formats that pysubs2 supports
                and overrides the auditok method to find speech regions.
                (arg_num = 0 or 1)"""
    )

    speech_group.add_argument(
        '-gsv2', '--gspeechv2',
        metavar='key',
        help="The Google Speech V2 API key to be used. "
             "If not provided, use free API key instead."
             "(arg_num = 1)"
    )

    speech_group.add_argument(
        '-S', '--src-language',
        metavar='lang code',
        help="Lang code of language spoken in input file. "
             "(arg_num = 1) (default: %(default)s)"
    )

    speech_group.add_argument(
        '-mnc', '--min-confidence',
        metavar='float',
        type=float,
        default=0.0,
        help="Google Speech V2 API response for text confidence. "
             "A float value between 0 and 1. "
             "Confidence bigger means the result is better. "
             "Input this argument will drop any result below it. "
             "Ref: https://github.com/BingLingGroup/google-speech-v2#response "
             "(arg_num = 1) (default: %(default)s)"
    )

    speech_group.add_argument(
        '-sc', '--speech-concurrency',
        metavar='integer',
        type=int,
        default=constants.DEFAULT_CONCURRENCY,
        help="Number of concurrent Google Speech V2 requests to make. "
             "(arg_num = 1) (default: %(default)s)"
    )

    trans_group.add_argument(
        '-D', '--dst-language',
        metavar='lang code',
        help="Lang code of desired language for the subtitles. "
             "(arg_num = 1) (default: %(default)s)"
    )

    trans_group.add_argument(
        '-gtv2', '--gtransv2',
        metavar='key',
        help="The Google Translate V2 API key to be used. "
             "If not provided, use free API instead. "
             "(arg_num = 1)"
    )

    trans_group.add_argument(
        '-lpt', '--lines-per-trans',
        metavar='integer',
        type=int,
        default=constants.DEFAULT_LINES_PER_TRANS,
        help="Number of lines per Google Translate V2 request. "
             "(arg_num = 1) (default: %(default)s)"
    )

    trans_group.add_argument(
        '-slp', '--sleep-seconds',
        metavar='second',
        type=int,
        default=constants.DEFAULT_SLEEP_SECONDS,
        help="Seconds to sleep between two translation requests. "
             "(arg_num = 1) (default: %(default)s)"
    )

    trans_group.add_argument(
        '-tc', '--trans-concurrency',
        metavar='integer',
        type=int,
        default=constants.DEFAULT_CONCURRENCY,
        help="Number of concurrent "
             "Google translate V2 API requests to make. "
             "(arg_num = 1) (default: %(default)s)"
    )

    output_group.add_argument(
        '-o', '--output',
        metavar='path',
        help="""The output path for subtitles file.
                (default: the \"input\" path combined 
                with the proper name tails) (arg_num = 1)"""
    )

    output_group.add_argument(
        '-y', '--yes',
        action='store_true',
        help="Avoid any pause and overwriting files. "
             "Stop the program when your args are wrong. (arg_num = 0)"
    )

    output_group.add_argument(
        '-of', '--output-files',
        metavar='type',
        nargs='*',
        default="dst",
        help="Output more files. "
             "Available types: "
             "regions, src, dst, bilingual, all. "
             "(4 ≥ arg_num ≥ 1 ) (default: %(default)s)"
    )

    output_group.add_argument(
        '-F', '--format',
        metavar='format',
        help="Destination subtitles format. "
             "If not provided, use the extension name "
             "in the \"-o\"/\"--output\" arg. "
             "If \"-o\"/\"--output\" arg doesn't provide "
             "the extension name, use \"{dft}\" instead. "
             "(arg_num = 1) (default: {dft})".format(
                 dft=constants.DEFAULT_SUBTITLES_FORMAT)
    )

    output_group.add_argument(
        '-fps', '--sub-fps',
        metavar='float',
        type=float,
        help="Valid when your output format is \"sub\". "
             "If input, it will override the fps check "
             "on the input file. "
             "Ref: https://pysubs2.readthedocs.io/en/latest/api-reference.html"
             "#supported-input-output-formats "
             "(arg_num = 1)"
    )

    output_group.add_argument(
        '-der', '--drop-empty-regions',
        action='store_true',
        help="Drop any regions without text. "
             "(arg_num = 0)"
    )

    options_group.add_argument(
        '-htp', '--http-speech-to-text-api',
        action='store_true',
        help="Change the Google Speech V2 API "
             "url into the http one. "
             "(arg_num = 0)"
    )

    options_group.add_argument(
        '-h', '--help',
        action='help',
        help="Show %(prog)s help message and exit. (arg_num = 0)"
    )

    options_group.add_argument(
        '-V', '--version',
        action='version',
        version='%(prog)s ' + metadata.VERSION
        + ' by ' + metadata.AUTHOR + ' <'
        + metadata.AUTHOR_EMAIL + '>',
        help="Show %(prog)s version and exit. (arg_num = 0)"
    )

    auditok_group.add_argument(
        '-et', '--energy-threshold',
        metavar='energy',
        type=int,
        default=constants.DEFAULT_ENERGY_THRESHOLD,
        help="The energy level which determines the region to be detected. "
             "Ref: https://auditok.readthedocs.io/en/latest/apitutorial.html"
             "#examples-using-real-audio-data "
             "(arg_num = 1) (default: %(default)s)"
    )

    auditok_group.add_argument(
        '-mnrs', '--min-region-size',
        metavar='second',
        type=float,
        default=constants.MIN_REGION_SIZE,
        help="Minimum region size. "
             "Same docs above. "
             "(arg_num = 1) (default: %(default)s)"
    )

    auditok_group.add_argument(
        '-mxrs', '--max-region-size',
        metavar='second',
        type=float,
        default=constants.MAX_REGION_SIZE,
        help="Maximum region size. "
             "Same docs above. "
             "(arg_num = 1) (default: %(default)s)"
    )

    auditok_group.add_argument(
        '-mxcs', '--max-continuous-silence',
        metavar='second',
        type=float,
        default=constants.DEFAULT_CONTINUOUS_SILENCE,
        help="Maximum length of a tolerated silence within a valid audio activity. "
             "Same docs above. "
             "(arg_num = 1) (default: %(default)s)"
    )

    auditok_group.add_argument(
        '-sml', '--strict-min-length',
        action='store_true',
        help="Ref: https://auditok.readthedocs.io/en/latest/core.html#class-summary "
             "(arg_num = 0)"
    )

    auditok_group.add_argument(
        '-dts', '--drop-trailing-silence',
        action='store_true',
        help="Ref: https://auditok.readthedocs.io/en/latest/core.html#class-summary "
             "(arg_num = 0)"
    )

    list_group.add_argument(
        '-lf', '--list-formats',
        action='store_true',
        help="""List all available output subtitles formats.
                If your format is not supported,
                you can use ffmpeg or SubtitleEdit to convert the formats. 
                [ATTENTION]: You need to offer fps option 
                when input is an audio file
                and output is \"sub\" format.
                (arg_num = 0)"""
    )

    list_group.add_argument(
        '-lsc', '--list-speech-to-text-codes',
        action='store_true',
        help="""List all available source language codes,
                which mean the available speech-to-text
                language codes.
                [ATTENTION]: Its name is different from 
                the destination language codes.
                Reference: https://cloud.google.com/speech-to-text/docs/languages
                https://tools.ietf.org/html/bcp47
                (arg_num = 0)"""
    )

    list_group.add_argument(
        '-ltc', '--list-translation-codes',
        action='store_true',
        help="""List all available destination language codes,
                which mean the available translation
                language codes.
                [ATTENTION]: Its name is different from 
                the destination language codes.
                Reference: https://cloud.google.com/speech-to-text/docs/languages
                https://tools.ietf.org/html/bcp47
                (arg_num = 0)"""
    )

    return parser.parse_args()
