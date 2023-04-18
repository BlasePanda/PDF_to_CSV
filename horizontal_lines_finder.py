import fitz  # PyMuPDF
from PIL import Image, ImageDraw
import cv2
import numpy as np
import tempfile


def process_pdf(file_path, dpi=300):
    """
    Process a PDF document, extracting horizontal white lines and saving their Y-coordinate values to a text file.

    :param file_path: Path to the input PDF file.
    :param dpi: Desired DPI for the output images. Default is 300 DPI.
    """
    zoom = dpi / 72  # zoom factor, standard: 72 dpi
    magnify = fitz.Matrix(zoom, zoom)  # magnifies in x, resp. y direction
    doc = fitz.open(file_path)  # open document

    def apply_white_box(image, box):
        """
        Apply a white box to a specific area of an image.

        :param image: Input image as a PIL Image object.
        :param box: Tuple containing the coordinates of the box (x1, y1, x2, y2).
        :return: Image with the white box applied.
        """
        white_img = Image.new('RGBA', image.size, color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(white_img)
        draw.rectangle(box, fill=(255, 255, 255, 255))
        return Image.alpha_composite(image.convert('RGBA'), white_img)

    def change_color(image, color_old, color_new):
        """
        Change a specific color in the image to another color.

        :param image: Input image as a PIL Image object.
        :param color_old: Tuple containing the RGBA values of the old color.
        :param color_new: Tuple containing the RGBA values of the new color.
        :return: Image with the old color changed to the new color.
        """
        image = image.convert('RGBA')
        img_array = np.array(image)
        mask = np.all(img_array == color_old, axis=-1)
        img_array[mask] = color_new
        image = Image.fromarray(img_array)
        return image

    # def sort_contours(cnts, method="left-to-right"):
    #     reverse = False
    #     i = 0
    #
    #     if method == "right-to-left" or method == "bottom-to-top":
    #         reverse = True
    #
    #     if method == "top-to-bottom" or method == "bottom-to-top":
    #         i = 1
    #
    #     boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    #     (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
    #                                         key=lambda b: b[1][i], reverse=reverse))
    #
    #     return cnts, boundingBoxes

    def box_extraction(img_for_box_extraction):
        """
        Extract horizontal lines from an image.

        :param img_for_box_extraction: Input image as a PIL Image object.
        :return: Image with horizontal lines extracted.
        """
        image = np.array(img_for_box_extraction.convert('L'))
        (thresh, img_bin) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        img_bin = 255 - img_bin

        kernel_length = np.array(image).shape[1] // 40

        # verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
        hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
        horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
        horizontal_lines_img = cv2.cvtColor(horizontal_lines_img, cv2.COLOR_GRAY2RGB)

        return np.array(horizontal_lines_img)

    def find_horizontal_white_lines(image, page_number, name):
        """
        Find horizontal white lines in an image and save their Y-coordinate values to a text file.

        :param image: Input image as a NumPy array.
        :param page_number: Integer representing the current page number.
        :param name: String representing the name of the input PDF file.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_height = image.shape[0]
        lower_white = np.array([200])
        upper_white = np.array([255])
        mask = cv2.inRange(gray, lower_white, upper_white)
        contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        yyyy = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            if w > h and w > 50:
                y_percentage = (y / image_height) * 595.28
                print(f'Horizontal white line found at coordinates: ({x}, {y})')
                yyyy.append(y_percentage)

        yyyy.remove(yyyy[0])

        file_name = f"coordinates{name}.txt"
        with open(file_name, "a") as file:
            file.write(f"{page_number}: {yyyy},\n")

    num = 0
    for page in doc:
        num += 1
        print(num)
        pix = page.get_pixmap(matrix=magnify)

        with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
            pix.save(temp_file.name)
            img = Image.open(temp_file.name)

            output_img = apply_white_box(img, (0, 0, 3508, 775))
            output_img = apply_white_box(output_img, (0, 2310, 3508, 2481))

            old_color = (191, 208, 223, 255)
            new_color = (255, 0, 0, 255)
            output_img = change_color(output_img, old_color, new_color)
            output_img = box_extraction(output_img)
            find_horizontal_white_lines(output_img, page_number=num, name=file_path)
