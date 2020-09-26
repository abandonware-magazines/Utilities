from PIL import Image
import pytesseract
import os, re, sys
import argparse

# Some replacements aren't always true,
#  but they fix more issues than they cause.
# Order matters.
heuristic_text_replacements = [
    (re.compile(r"\*"),                             r'י'), # Needs to come before transforming YudYud
    (re.compile(r"'י"),                             r'"',),
    (re.compile(r"\|"),                             r'ן'),
    (re.compile(r'(\bו?[הבשכלמ])יי(?!(תה|תי))'),   r'\1"'),
    (re.compile(r'(\b)יי'),                         r'"'),
    (re.compile(r'יי(?=\b|$)'),                     r'"'),
    (re.compile(r'יס(?=[^א-ת])'),                   r"ים"),
    (re.compile(r"(\w)ם(\w)"),                      r'\1ס\2'),
    (re.compile(r'(\n\s*)+'),                       r'\n'),
    (re.compile(r'\x0c'),                           r''),
    # Need to come after transforming Samech to Mem-Sofit at the end of a word
    (re.compile(r'טטרים'),                          r'טטריס'),
    (re.compile(r'בסים\b'),                         r'בסיס'),
    (re.compile(r'יוס\b'),                          r'יום'),

    (re.compile(r'\b([א-ת])ס\b'),                   r'\1ם'),
    (re.compile(r'חם וחלילה'),                      r'חס וחלילה'),

    (re.compile(r'הנייל'),                          r'הנ"ל')
]


def apply_heuristic_autocorrect(txt):
    for pattern, replacement in heuristic_text_replacements:
        txt = pattern.sub(replacement, txt)
    return txt


def perform_ocr(input_img_path, heuristic_autocorrect = False):
    output = pytesseract.image_to_string(Image.open(input_img_path), lang = 'heb+eng', config = '--psm 1')
    output = output.strip(' \t\n\r\u05b0\x0c\u200e')
    if heuristic_autocorrect:
        output = apply_heuristic_autocorrect(output)
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='English/Hebrew OCR Wrapper with heuristic autocorrect')
    parser.add_argument('-i', '--input_img', action='store', required = True, help='Path to input image')
    parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout, help='Path to output text (defaults to standard output if empty)')
    parser.add_argument('-a', '--autocorrect', action = 'store_true', default = False, help = 'Perform heuristic autocorrect on output')
    args = parser.parse_args()

    output = perform_ocr(args.input_img, args.autocorrect)
    args.outfile.write(output)
