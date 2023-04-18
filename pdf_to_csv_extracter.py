import fitz
import csv
import re
from ast import literal_eval
from multiprocessing import Pool
import glob
from parallel_coordinate_finder import key_sorting


X_COORDS = [17.67969, 36.201269999999994, 96.81735, 157.43343, 255.09267, 309.81552, 388.95318000000003, 468.09084,
            530.6432669999999, 599.4256799999999, 667.61877, 700.4524799999999, 758.54289, 820.00086]


def cutting_both_axes(pdf, xs, ys, page_number):
    # open input pdf
    inputpdf = fitz.open(pdf)

    # open a new CSV file to write the extracted text
    with open(f"output{pdf}.csv", "a", newline="", encoding="utf-8") as csvfile:
        # csv_writer = csv.writer(csvfile)

        # check if the specified page number is valid
        if 0 <= page_number < len(inputpdf):
            page = inputpdf[page_number]

            # loop through the y-axis coordinates
            for j in range(len(ys) - 1):
                y1 = ys[j]
                y2 = ys[j + 1]

                # loop through the x-axis coordinates
                for k in range(len(xs) - 1):
                    x1 = xs[k]
                    x2 = xs[k + 1]

                    # define the rectangle using the coordinates
                    rect = fitz.Rect(x1, y1, x2, y2)
                    extracted_text = page.get_textbox(rect)
                    extracted_text = extracted_text.replace(",", "%&")  # Replace commas with '%&'
                    extracted_text = extracted_text.replace("\n", "")

                    # save extracted text to a CSV file, separated by commas
                    csvfile.write(extracted_text)

                    # write a comma after every cell except the last one
                    if k < len(xs) - 2:
                        csvfile.write(",")

                # start a new row after processing all x-axis coordinates for the current y-axis coordinate
                csvfile.write("\n")
        else:
            print("Invalid page number.")


def cleaner(txt_file, pdf_file):
    with open(txt_file, 'r') as f:
        all_ys = []
        for line in f:
            line = re.sub(r'^\d+\s*:\s*\[', '[', line)
            print(line)
            # line = re.sub(r'^\d+\[', '[', line)
            line = line.replace("],", "]")
            print(line)
            line = literal_eval(line)
            line = line[::-1]
            all_ys.append(line)

    n = 0
    for ys in all_ys:
        print(n)
        print(ys)
        cutting_both_axes(pdf_file, X_COORDS, ys=ys, page_number=n)
        n += 1


def process_pdf_txt(txt_file, pdf_file):
    """
    This function takes a file path as input and processes the PDF file.
    """
    cleaner(txt_file=txt_file, pdf_file=pdf_file)


def extracting_to_csvs():
    prefix = "coordinatessmall_"
    txts = glob.glob("coordinatessmall*")
    txts = sorted(txts, key=lambda x: key_sorting(x, prefix))
    prefix = "small_"
    pdfs = glob.glob("small*")
    pdfs = sorted(pdfs, key=lambda x: key_sorting(x, prefix))
    file_pairs = zip(txts, pdfs)
    pool = Pool(processes=len(txts))
    pool.starmap(process_pdf_txt, file_pairs)
