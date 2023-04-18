import argparse
import os
from splitting import split_pdf
from parallel_coordinate_finder import run_pdfs_in_parallel
from pdf_to_csv_extracter import extracting_to_csvs
from csv_combiner import combines_csvs

def main(input_pdf, output_prefix, num_files):
    # STEP 1
    split_pdf(input_pdf, output_prefix, num_files)

    # STEP 2
    run_pdfs_in_parallel()

    # STEP 3
    extracting_to_csvs()

    # STEP 4
    combines_csvs(input_pdf)

    # Set the directory path where the files are located
    directory = "./"

    # Get all files in the directory
    files = os.listdir(directory)

    # Loop through each file and delete if the filename starts with "coordinatessmall_", "outputsmall_", or "small_"
    for file in files:
        if file.startswith("coordinatessmall_") or file.startswith("outputsmall_") or file.startswith("small_"):
            os.remove(os.path.join(directory, file))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a PDF file")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument("output_prefix", help="Prefix for output files")
    parser.add_argument("num_files", type=int, help="Number of files to split the input PDF into")

    args = parser.parse_args()
    main(args.input_pdf, args.output_prefix, args.num_files)
