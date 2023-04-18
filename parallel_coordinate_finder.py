import glob
from multiprocessing import Pool
from horizontal_lines_finder import process_pdf


def key_sorting(file_name, prefix):
    # Extract the file index from the file name (assuming the index is a number)
    index_str = file_name.replace(prefix, '').split('.')[0]  # Get the filename without the extension
    index_int = int(index_str)
    print(index_int)
    return f"{index_int:02d}"


# RUNS IN PARALLEL AND USING CUTTED PDFS TO EXTRACT Y COORDINATES OF LINES
def process_page(file_path):
    """
    This function takes a file path as input and processes the PDF file.
    """
    process_pdf(file_path)


def run_pdfs_in_parallel():
    # Find all files in the current directory that start with "small"
    files = glob.glob("small*")
    files = sorted(files, key=lambda x: key_sorting(x, prefix="small_"))
    pool = Pool(processes=len(files))
    pool.map(process_page, files)



