from tkinter import Tk, Text, Canvas, Menu, messagebox

PIXEL_SIZE = 14
CANVAS_HEIGHT = 32
WINDOW_WIDTH = 128
MENUBAR_HEIGHT = 10
HEX_TEXT_HEIGHT = 5
INFO_TEXT_HEIGHT = 1

pixel_set = set()
rect_set = {}


def get_pixel(x, y):
    pixel_x = x // PIXEL_SIZE
    pixel_y = y // PIXEL_SIZE
    return int(pixel_x), int(pixel_y)


def get_pixel_center(pixel):
    pixel_center_x = pixel[0] * PIXEL_SIZE + PIXEL_SIZE // 2
    pixel_center_y = pixel[1] * PIXEL_SIZE + PIXEL_SIZE // 2
    return int(pixel_center_x), int(pixel_center_y)


def mark_handler(event):
    x, y = event.x, event.y
    if 0 < y < CANVAS_HEIGHT * PIXEL_SIZE and 0 < x < WINDOW_WIDTH * PIXEL_SIZE:
        mark_position(x, y)


def clear_handler(event):
    x, y = event.x, event.y
    if 0 < y < CANVAS_HEIGHT * PIXEL_SIZE and 0 < x < WINDOW_WIDTH * PIXEL_SIZE:
        clear_position(x, y)


def mark_position(x, y):
    pixel = get_pixel(x, y)
    pixel_center_x, pixel_center_y = get_pixel_center(pixel)
    # print("x:" + str(x) + " y:" + str(y) + " pixel:" + str(pixel))
    info_textbox["state"] = "normal"
    info_textbox.replace(
        "1.98", "end", str(pixel)
    )  # updating only the pixel location marked
    info_textbox["state"] = "disable"
    if pixel not in pixel_set:
        pixel_set.add(pixel)
        rect_id = canvas.create_rectangle(
            pixel_center_x - PIXEL_SIZE // 2,
            pixel_center_y - PIXEL_SIZE // 2,
            pixel_center_x + PIXEL_SIZE // 2,
            pixel_center_y + PIXEL_SIZE // 2,
            fill="black",
            outline="red",
        )
        rect_set[pixel] = rect_id


def clear_position(x, y):
    pixel = get_pixel(x, y)
    if pixel in pixel_set:
        pixel_set.remove(pixel)
        canvas.delete(rect_set[pixel])


def import_hex():
    if not messagebox.askokcancel(
        "WARNING", "Importing clears all pixels. Are you sure you want to clear?"
    ):
        return
    # output_str = input("paste Uinthex format: ")
    output_str = hex_textbox.get(0.0, "end")
    output_str = output_str.replace("{", "")
    output_str = output_str.replace("}", "")
    output_str = output_str.replace("\t", "")
    output_str = output_str.replace("\n", "")
    output_str = output_str.replace(" ", "")
    hex_list = output_str.split(",")
    pixel_set.clear()
    canvas.delete("all")
    y_idx = 0
    x_idx = 0
    page = 0
    for hex_idx, output_str in enumerate(hex_list):
        uint_num = int(output_str, 0)
        while uint_num != 0:
            x, y = 0, 0
            if uint_num & 0x1 == 1:
                pixel = (x_idx, y_idx)
                x, y = get_pixel_center(pixel)
                mark_position(x, y)
                print("(" + str(x_idx) + ", " + str(y_idx) + ") ", end="")

            uint_num = uint_num >> 1
            y_idx += 1
        print(
            "idx: "
            + str(hex_idx)
            + " output_str: "
            + output_str
            + " uint_num: "
            + str(uint_num)
        )

        if x_idx < 127:
            x_idx += 1
        else:
            page += 1
            x_idx = 0
        y_idx = page * 8

    print("IMPORTED")


def export_hex():
    if not messagebox.askokcancel(
        "WARNING", "Exporting clears Text box. Are you sure you want?"
    ):
        return
    hex_pattern = [[0 for i in range(128)] for j in range(4)]
    output_str = ""

    for pixel in pixel_set:
        x, y = pixel
        page = y // 8
        hex_pattern[page][x] |= 1 << y - page * 8

    for page_idx in range(4):
        for uint_idx in range(128):
            if (uint_idx + (page_idx * 128)) % 16 == 0:
                output_str += "\n"
            output_str += "0x" + f"{hex_pattern[page_idx][uint_idx]:02X}" + ", "
    output_str = output_str[:-2]  # remove trailing comma and space

    print("EXPORTING:")
    print("pixel set: " + str(pixel_set))
    print("uint_pattern: ", end="")
    print(output_str, end="\n\n")
    hex_textbox.delete(0.0, "end")
    hex_textbox.insert("end", output_str)


def import_range_hex():
    if not messagebox.askokcancel(
        "WARNING", "Importing clears all pixels. Are you sure you want to clear?"
    ):
        return
    # output_str = input("paste Uinthex format: ")
    output_str = hex_textbox.get(0.0, "end")
    output_str = output_str.replace("{", "")
    output_str = output_str.replace("}", "")
    output_str = output_str.replace("\t", "")
    output_str = output_str.replace("\n", "")
    output_str = output_str.replace(" ", "")
    hex_list = output_str.split(",")
    pixel_set.clear()
    canvas.delete("all")
    y_idx = 0
    x_idx = 0
    page = 0
    column_end = len(hex_list) // 4
    if column_end > 128:
        column_end = 128
    for hex_idx, output_str in enumerate(hex_list):
        uint_num = int(output_str, 0)
        while uint_num != 0:
            x, y = 0, 0
            if uint_num & 0x1 == 1:
                pixel = (x_idx, y_idx)
                x, y = get_pixel_center(pixel)
                mark_position(x, y)
                print("(" + str(x_idx) + ", " + str(y_idx) + ") ", end="")

            uint_num = uint_num >> 1
            y_idx += 1
        print(
            "idx: "
            + str(hex_idx)
            + " output_str: "
            + output_str
            + " uint_num: "
            + str(uint_num)
        )

        if x_idx < column_end - 1:
            x_idx += 1
        else:
            page += 1
            x_idx = 0
        y_idx = page * 8

    print("IMPORTED")


def export_range_hex():
    if not messagebox.askokcancel(
        "WARNING", "Exporting clears Text box. Are you sure you want?"
    ):
        return
    hex_pattern = [[0 for i in range(128)] for j in range(4)]
    output_str = ""

    for pixel in pixel_set:
        x, y = pixel
        page = y // 8
        hex_pattern[page][x] |= 1 << y - page * 8

    column_end = 128

    while (
        column_end >= 0
        and hex_pattern[0][column_end - 1] == 0
        and hex_pattern[1][column_end - 1] == 0
        and hex_pattern[2][column_end - 1] == 0
        and hex_pattern[3][column_end - 1] == 0
    ):
        column_end -= 1

    for page_idx in range(4):
        for uint_idx in range(128):
            if uint_idx < column_end:
                if (uint_idx + (page_idx * column_end)) % column_end == 0:
                    output_str += "\n"
                output_str += "0x" + f"{hex_pattern[page_idx][uint_idx]:02X}" + ", "
    output_str = output_str[:-2]  # remove trailing comma and space

    print("EXPORTING:")
    print("pixel set: " + str(pixel_set))
    print("uint_pattern: ", end="")
    print(output_str, end="\n\n")
    hex_textbox.delete(0.0, "end")
    hex_textbox.insert("end", output_str)


def old_import_hex():
    if not messagebox.askokcancel(
        "WARNING",
        "Importing retains already drawn pixels. Are you sure you want to proceed?",
    ):
        return
    # output_str = input("paste Uinthex format: ")
    offset = get_offset()
    output_str = hex_textbox.get(0.0, "end")
    output_str = output_str.replace("{", "")
    output_str = output_str.replace("}", "")
    output_str = output_str.replace("\t", "")
    output_str = output_str.replace("\n", "")
    output_str = output_str.replace(" ", "")
    hex_list = output_str.split(",")
    # pixel_set.clear()
    # canvas.delete("all")
    for hex_idx, output_str in enumerate(hex_list):
        uint_num = int(output_str, 0)
        for y_idx in range(32):
            if (uint_num >> y_idx & 0x1) == 1:
                pixel = (hex_idx + offset, 31 - y_idx)
                x, y = get_pixel_center(pixel)
                mark_position(x, y)
    print("IMPORTED")


def old_export_hex():
    if not messagebox.askokcancel(
        "WARNING", "Exporting clears Text box. Are you sure you want?"
    ):
        return
    hex_pattern = [0x0] * 32
    offset = get_offset()
    output_str = "{"
    for pixel in pixel_set:
        if pixel[0] >= offset and pixel[0] < offset + 31:
            x_offset = pixel[0] - offset
            hex_pattern[x_offset] |= 1 << 31 - pixel[1]
    for uint_idx in range(len(hex_pattern) - 1):
        output_str += hex(hex_pattern[uint_idx]) + ", "
    output_str += hex(hex_pattern[-1]) + "}"
    print("EXPORTING:")
    print("pixel set: " + str(pixel_set))
    print("uint_pattern: ", end="")
    print(output_str, end="\n\n")
    hex_textbox.delete(0.0, "end")
    hex_textbox.insert("end", output_str)


def get_offset():
    offset = 0
    output_str = offset_textbox.get(0.0, "end")
    output_str = output_str.replace("\n", "")
    if output_str != "":
        offset = int(output_str)
    if offset > 96:
        offset = 96
    if offset < 0:
        offset = 0
    print("offset: " + str(offset))
    return offset


def clear_canvas():
    if not messagebox.askokcancel("WARNING", "Are you sure you want to clear?"):
        return
    for x in range(0, WINDOW_WIDTH * PIXEL_SIZE, PIXEL_SIZE):
        for y in range(0, CANVAS_HEIGHT * PIXEL_SIZE, PIXEL_SIZE):
            clear_position(x, y)


def fill_canvas():
    if not messagebox.askokcancel("WARNING", "Are you sure you want to fill?"):
        return
    for x in range(0, WINDOW_WIDTH * PIXEL_SIZE, PIXEL_SIZE):
        for y in range(0, CANVAS_HEIGHT * PIXEL_SIZE, PIXEL_SIZE):
            mark_position(x, y)


# window, textboxs, canvas setup
root = Tk()
root.geometry(
    str(PIXEL_SIZE * WINDOW_WIDTH)
    + "x"
    + str(PIXEL_SIZE * (CANVAS_HEIGHT + HEX_TEXT_HEIGHT + INFO_TEXT_HEIGHT * 2 + 2))
)
root.title("pixel placer")
canvas = Canvas(
    root, width=PIXEL_SIZE * WINDOW_WIDTH, height=PIXEL_SIZE * CANVAS_HEIGHT
)
hex_textbox = Text(
    root, state="normal", width=PIXEL_SIZE * WINDOW_WIDTH, height=HEX_TEXT_HEIGHT
)
info_textbox = Text(
    root, state="disable", width=PIXEL_SIZE * WINDOW_WIDTH // 2, height=INFO_TEXT_HEIGHT
)
offset_textbox = Text(
    root, state="normal", width=PIXEL_SIZE * WINDOW_WIDTH // 2, height=INFO_TEXT_HEIGHT
)
hex_textbox.pack()
info_textbox.pack()
offset_textbox.pack()
canvas.pack()
info_textbox["state"] = "normal"
info_textbox.insert(
    "end",
    "Insert hex codes above to import. Exported Hex codes will show above. enter offset below 0 to 96. ",
)
info_textbox["state"] = "disable"

# menubar setup
menubar = Menu(root)
menubar.add_command(label="Display_Export", command=export_hex)
menubar.add_command(label="Display_Range_Export", command=export_range_hex)
menubar.add_command(label="Display_Import", command=import_range_hex)
menubar.add_command(label="Character_Export", command=old_export_hex)
menubar.add_command(label="Character_Import", command=old_import_hex)
menubar.add_command(label="Clear", command=clear_canvas)
menubar.add_command(label="Fill", command=fill_canvas)
root.config(menu=menubar)

# action setup
canvas.bind("<Button-1>", mark_handler)
canvas.bind("<B1-Motion>", mark_handler)
canvas.bind("<Button-3>", clear_handler)
canvas.bind("<B3-Motion>", clear_handler)

# Keep the screen open
root.mainloop()
