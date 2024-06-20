import FreeSimpleGUI as sg
import pywinstyles
import xml.etree.ElementTree as ET
from difflib import unified_diff

PROGRAM_ICON = "./_internal/icon/programing.ico"

def read_xml(file_path):
    try:
        tree = ET.parse(file_path)
        return tree.getroot()
    except FileNotFoundError:
        pass
    except AttributeError:
        pass

def xml_to_string(element):
    try:
        return ET.tostring(element, encoding='unicode')
    except AttributeError:
        pass
    except FileNotFoundError:
        pass

def compare_xml(file1, file2):
    try:
        xml1 = read_xml(file1)
        xml2 = read_xml(file2)

        xml1_str = xml_to_string(xml1)
        xml2_str = xml_to_string(xml2)

        diff = unified_diff(
            xml1_str.splitlines(keepends=True),
            xml2_str.splitlines(keepends=True),
            fromfile=file1,
            tofile=file2
        )

        diff_output = ''.join(diff).strip()
        if not diff_output:
            window["-OUTPUT_DIFFERENCE-"].update("No differences found.")
        else:
            lines = diff_output.splitlines()

            for line in lines:
                if line.startswith('-'):
                    window["-OUTPUT_DIFFERENCE-"].print(line, text_color="#f44336") # Red
                elif line.startswith('+'):
                    window["-OUTPUT_DIFFERENCE-"].print(line, text_color="#4caf50") # Green
                else:
                    window["-OUTPUT_DIFFERENCE-"].print(line)
        
        return diff_output
    
    except FileNotFoundError as e:
        window['-OUTPUT_DIFFERENCE-'].update(f"File not found, check both inputs.\n {e}")
    except AttributeError as e:
        pass

custom_theme = {"BACKGROUND": "#191e26",
                "TEXT": "#fcfcfc",
                "INPUT": "#292a2e",
                "TEXT_INPUT": "#fcfcfc",
                "SCROLL": "#292a2e",
                "BUTTON": ("#ff793f", "#313641"),
                "PROGRESS": ("#ff793f", "#4a6ab3"),
                "BORDER": 2,
                "SLIDER_DEPTH": 0,
                "PROGRESS_DEPTH": 1}

# Add your dictionary to the PySimpleGUI themes
FILE_TYPES = (("XML (Extensible Markup Language)", ".xml"),)

TITLE_COLOR = "#ff793f"
sg.theme_add_new("MyTheme", custom_theme)
sg.theme("MyTheme")
FONT = ("Calibri", 13)


# Define the layout of the GUI
multiline_one_layout = [
    [sg.Multiline(size=(60, 20), key="-OUTPUT_XML_ONE-", horizontal_scroll=True)],
    [sg.Input(default_text="path/to/xml_config_file",key="-XML_ONE_INPUT-", expand_x=True, enable_events=True), sg.FileBrowse(target="-XML_ONE_INPUT-", file_types=FILE_TYPES)]
]

multiline_two_layout = [
    [sg.Multiline(size=(60, 20), key="-OUTPUT_XML_TWO-", horizontal_scroll=True)],
    [sg.Input(default_text="path/to/xml_config_file",key="-XML_TWO_INPUT-", expand_x=True, enable_events=True), sg.FileBrowse(target="-XML_TWO_INPUT-", file_types=FILE_TYPES)]
]

multiline_difference_output_layout = [
    [sg.Multiline(size=(128, 16), key="-OUTPUT_DIFFERENCE-", disabled=True, horizontal_scroll=True)],
    [sg.Button(button_text="Compare",font="Calibri 13 bold", expand_x=True, button_color=("#191e26", "#449d48"), mouseover_colors=("#191e26","#367d39"))]
]

# Define frames
multiline_one_frame = sg.Frame("XML Output", multiline_one_layout, title_color=TITLE_COLOR, font=("Calibri 14 bold"))
multiline_two_frame = sg.Frame("XML Output", multiline_two_layout, title_color=TITLE_COLOR, font=("Calibri 14 bold"))
multiline_difference_output_frame = sg.Frame("Difference Output", multiline_difference_output_layout, title_color=TITLE_COLOR, font=("Calibri 14 bold"))

# Define the main layout
layout = [
    [sg.Column([[multiline_one_frame]]), sg.VSeparator(), sg.Column([[multiline_two_frame]], expand_x=True, expand_y=True)],
    [sg.HSep()],
    [sg.Column([[multiline_difference_output_frame]], expand_x=True, expand_y=True)
]]

# Create the window
window = sg.Window('XML Config Comparison Tool v1.0 © 2024 by Jovan Zaric', layout, font=FONT, icon=PROGRAM_ICON, finalize=True)
pywinstyles.apply_style(window,"mica")

# Event loop to process events and get input values
while True:
    event, values = window.read()
    
    print(f"EVENT: {event}\nVALUE: {values}")
    if event == sg.WINDOW_CLOSED:
        break
    
    elif event == "-XML_ONE_INPUT-":
        file_path = values['-XML_ONE_INPUT-']
        xml_str = xml_to_string(read_xml(file_path))
        if xml_str is not None:
            window["-OUTPUT_XML_ONE-"].update(xml_str.strip())

    elif event == "-XML_TWO_INPUT-":
        file_path = values['-XML_TWO_INPUT-']
        xml_str = xml_to_string(read_xml(file_path))
        if xml_str is not None:
            window["-OUTPUT_XML_TWO-"].update(xml_str.strip())
        
    elif event == 'Compare':
        file1 = values['-XML_ONE_INPUT-']
        file2 = values['-XML_TWO_INPUT-']
        try:
            compare_xml(file1, file2)
        except ET.ParseError as e:
            window['-OUTPUT_DIFFERENCE-'].update(f"Error parsing XML: {e}")

# Close the window
window.close()
