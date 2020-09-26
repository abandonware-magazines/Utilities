from PIL import Image
import pytesseract
import sys
import argparse

def perform_ocr(input_img_path):
    output = pytesseract.image_to_string(Image.open(input_img_path), 
                                        lang = 'heb+eng',  # Order of languages matters
                                        config = '--psm 1' # PSM1 == Automatic page segmentation with OSD.
    )
    output = output.strip(' \t\n\r\u05b0\x0c\u200e') # Cleanup some common characters which are added for some reason by tesseract
    
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='English/Hebrew OCR Wrapper with heuristic autocorrect')
    parser.add_argument('-i', '--input_img', action='store', required = True, help='Path to input image')
    parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout, help='Path to output text (defaults to standard output if empty)')
    args = parser.parse_args()

    output = perform_ocr(args.input_img)
    args.outfile.write(output)
