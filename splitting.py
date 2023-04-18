import math
import PyPDF2


def split_pdf(input_pdf, output_prefix, num_files):
    with open(input_pdf, 'rb') as pdf_file:
        reader = PyPDF2.PdfFileReader(pdf_file)
        total_pages = reader.getNumPages()
        pages_per_file = math.ceil(total_pages / num_files)

        for i in range(num_files):
            output_pdf = f"{output_prefix}_{i+1}.pdf"
            with open(output_pdf, 'wb') as output_file:
                writer = PyPDF2.PdfFileWriter()

                start_page = i * pages_per_file
                end_page = min(start_page + pages_per_file, total_pages)

                for page_num in range(start_page, end_page):
                    writer.addPage(reader.getPage(page_num))

                writer.write(output_file)
                print(f"Created {output_pdf} with pages {start_page} to {end_page-1}")
