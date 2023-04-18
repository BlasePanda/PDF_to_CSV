# PDF_to_CSV
Currently, it has a very specific use for my personal needs - extracting horizontally oriented data from PDFs.
PDF_to_CSV

This is a Python-based project that provides a pipeline to extract horizontally-oriented data from a PDF file and export it to CSV files. Currently, it has a very specific use for my personal needs.
Prerequisites

    Python 3.6 or above
    Required Python packages listed in requirements.txt

Getting Started

    - Clone the repository or download the source code as a zip file and extract it to your local machine.
    - Install the required packages by running pip install -r requirements.txt.
    - Place the PDF file you want to extract data from in the project directory.
    - Run the following command in the terminal to execute the code:

`python main.py input_pdf output_prefix num_files`

    input_pdf: Path to the input PDF file.
    output_prefix: Prefix for output files. (Curently "small" is hardcoded)
    num_files: Number of files to split the input PDF into.

Workflow

This project implements a 4-step pipeline to extract data from a PDF file:

**Step 1: Split PDF into smaller files**

    The split_pdf() function in splitting.py splits the input PDF file into a specified number of smaller files.

**Step 2: Run PDFs in parallel**

    The run_pdfs_in_parallel() function in parallel_coordinate_finder.py processes the smaller PDF files in parallel to extract coordinate data.

**Step 3: Extract data to CSVs**

    The extracting_to_csvs() function in pdf_to_csv_extracter.py extracts the coordinate data from the smaller PDF files and exports it to CSV files.

**Step 4: Combine CSV files**

    The combines_csvs() function in csv_combiner.py combines the CSV files into a single file.

Finally, the main function in main.py executes the pipeline and deletes any temporary files generated during the process.
