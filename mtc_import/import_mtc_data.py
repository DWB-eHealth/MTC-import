import sys

from mtc_form_csv_parser import MTCFormCSVParser

def main():
    if not len(sys.argv) > 1:
        print "Usage: python mtc_import/import_mtc_data.py <filepath>"
        return

    filepath = sys.argv[1]
    parser = MTCFormCSVParser(filepath)
    parser.get_forms()

if __name__ == "__main__":
    main()
