import os
from random import SystemRandom
import ntpath
import PySimpleGUI as sg
from PIL import Image, ImageDraw

_random = SystemRandom()


def merge_images(img1, img2, output_path=os.getcwd()):
    img_A = Image.open(img1)
    img_B = Image.open(img2)
    head, tail = ntpath.split("Merge_res.png")
    file_name_AB = tail or ntpath.basename(head)
    img_A.paste(img_B, (0, 0), img_B)
    img_A.save(output_path + '\\' + file_name_AB, 'PNG')

    sg.popup('Done!')


def visual_crypto(file_path, output_path=os.getcwd()):
    img = Image.open(file_path)
    f, e = os.path.splitext(file_path)

    out_filename_A = f + "_A.png"
    out_filename_B = f + "_B.png"
    out_filename_AB = f + "_AB_res.png"

    img = img.convert('1')  # convert image to 1 bit

    # Prepare two empty slider images for drawing
    width = img.size[0] * 2
    height = img.size[1] * 2
    out_image_A = Image.new('1', (width, height))
    out_image_B = Image.new('1', (width, height))
    draw_A = ImageDraw.Draw(out_image_A)
    draw_B = ImageDraw.Draw(out_image_B)

    # There are 6(4 choose 2) possible patterns and it is too late for me to think in binary and do these efficiently
    patterns = ((1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1), (0, 1, 1, 0), (0, 1, 0, 1), (0, 0, 1, 1))
    # Cycle through pixels
    for x in range(0, int(width / 2)):
        for y in range(0, int(height / 2)):
            pixel = img.getpixel((x, y))
            pat = _random.choice(patterns)
            # A will always get the pattern
            draw_A.point((x * 2, y * 2), pat[0])
            draw_A.point((x * 2 + 1, y * 2), pat[1])
            draw_A.point((x * 2, y * 2 + 1), pat[2])
            draw_A.point((x * 2 + 1, y * 2 + 1), pat[3])
            if pixel == 0:  # Dark pixel so B gets the anti pattern
                draw_B.point((x * 2, y * 2), 1 - pat[0])
                draw_B.point((x * 2 + 1, y * 2), 1 - pat[1])
                draw_B.point((x * 2, y * 2 + 1), 1 - pat[2])
                draw_B.point((x * 2 + 1, y * 2 + 1), 1 - pat[3])
            else:
                draw_B.point((x * 2, y * 2), pat[0])
                draw_B.point((x * 2 + 1, y * 2), pat[1])
                draw_B.point((x * 2, y * 2 + 1), pat[2])
                draw_B.point((x * 2 + 1, y * 2 + 1), pat[3])

    head, tail = ntpath.split(out_filename_A)
    file_name_A = tail or ntpath.basename(head)
    head, tail = ntpath.split(out_filename_B)
    file_name_B = tail or ntpath.basename(head)
    head, tail = ntpath.split(out_filename_AB)
    file_name_AB = tail or ntpath.basename(head)

    out_image_A.save(output_path + '\\' + file_name_A, 'PNG')
    out_image_B.save(output_path + '\\' + file_name_B, 'PNG')

    # out_image_A.paste(out_image_B, (0, 0), out_image_B)
    # out_image_A.save(output_path + '\\' + file_name_AB, 'PNG')

    sg.popup('Done!')


def create_img_win():
    img_col_l = [
        [sg.Text('Share A')],
        [sg.Image(key='-SHARE_A-')],
        [sg.Text('Share B')],
        [sg.Image(key='-SHARE_B-')]
    ]

    img_col_r = [
        [sg.Text('Share A+B'), sg.Image(key='-SHARE_AB-')]
    ]

    img_layout = [
        [sg.Col(img_col_l), sg.VerticalSeparator(), sg.Col(img_col_r)],
        [sg.HorizontalSeparator(pad=None)],

    ]
    win = sg.Window('Images', img_layout)
    return win


def startapp():
    sg.theme('LightBlue6')

    buttons_col = [
        [sg.Button('Run', size=(15, 1))],
        [sg.Button('Merge images', size=(15, 1))]
    ]

    input_col = [
        [sg.Text('Image process', size=(15, 1))],
        [sg.Input(key='-IMAGE-', size=(20, 1), visible=True, enable_events=True),
         sg.FileBrowse()],
        [sg.HorizontalSeparator()],
        [sg.Text('Image merge')],
        [sg.Input(key='-IMAGE_xA-', size=(20, 1), visible=True, enable_events=True),
         sg.FileBrowse()],
        [sg.Input(key='-IMAGE_xB-', size=(20, 1), visible=True, enable_events=True),
         sg.FileBrowse()],
    ]

    layout = [[sg.Col(input_col), sg.VerticalSeparator(pad=None), sg.Col(buttons_col)],
              [sg.HorizontalSeparator(pad=None)],
              [sg.Button('Quit'), sg.Input(key='-OUTPUT-DIR-', visible=True, enable_events=True, size=(15, 1)),
               sg.FolderBrowse('Output directory')]
              ]

    # Create the Window
    window = sg.Window('VisualCrypto', layout)

    img_a = None
    img_b = None
    img_c = None
    processed = False

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Quit':  # if user closes window or clicks cancel
            break

        if event == 'Run':
            if values['-IMAGE-']:
                if '.png' in values['-IMAGE-']:
                    if values['-OUTPUT-DIR-']:
                        visual_crypto(values['-IMAGE-'], values['-OUTPUT-DIR-'])
                        processed = True
                    else:
                        visual_crypto(values['-IMAGE-'])
                        processed = True
                else:
                    sg.popup('Wrong file')
            else:
                sg.popup('No image imported')

        if event == 'Show images':
            try:
                img_a.show()
                img_b.show()
                img_c.show()
            except:
                sg.popup('No image processed')

    if event == 'Merge images':
        if values['-IMAGE_xA-'] and values['-IMAGE_xB-']:
            if '.png' in values['-IMAGE_xA-'] and '.png' in values['-IMAGE_xB-']:

                if values['-OUTPUT-DIR-']:
                    merge_images(values['-IMAGE_xA-'], values['-IMAGE_xB-'],
                                 values['-OUTPUT-DIR-'])
                else:
                    merge_images(values['-IMAGE_xA-'], values['-IMAGE_xB-'])
            else:
                sg.popup('Wrong file')
        else:
            sg.popup('No image imported')

    window.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startapp()
