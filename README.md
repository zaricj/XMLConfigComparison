# XML Config Comparison Tool
## Overview
The XML Config Comparison Tool is a graphical user interface (GUI) application designed to compare two XML configuration files and display their differences. It uses the FreeSimpleGUI library for the interface and pywinstyles for applying a modern look. The tool reads and parses XML files, converting them to string format and then comparing them line by line. Differences are highlighted in the interface for easy identification.

## Features
**GUI Interface:** Simple and intuitive interface built with FreeSimpleGUI.

**XML Comparison:** Compare two XML files and display the differences.

**File Browsing:** Easily select XML files using the file browser.

**Theming:** Custom dark theme for the interface.

**Highlighting Differences:** Differences are color-coded for clarity.

## Installation

#### Clone the repository:

```bash
git clone https://github.com/zaricj/XMLConfigComparison
cd XMLConfigComparison
```

#### Install dependencies:

```bash
pip install FreeSimpleGUI
pip install pywinstyles
```
## Usage

#### Run the application:
```bash
python app.py
```
or
```bash
python XMLConfigComparisonGUI.py
# for the GUI Interface
```

#### Select XML files:
Click on the Browse button to select the first XML file.
Click on the Browse button to select the second XML file.

#### Compare XML files:

Click on the Compare button to see the differences.

Differences will be displayed in the "Difference Output" section, with deletions in red and additions in green.

## Code Overview

#### Imports
```python

import FreeSimpleGUI as sg
import pywinstyles
import xml.etree.ElementTree as ET
from difflib import unified_diff
```
#### Constants
```python
PROGRAM_ICON = "./_internal/icon/programing.ico"
FILE_TYPES = (("XML (Extensible Markup Language)", ".xml"),)
TITLE_COLOR = "#ff793f"
FONT = ("Calibri", 13)
```

#### Functions
**read_xml(file_path)**

Reads an XML file and returns its root element.

```python
def read_xml(file_path):
    try:
        tree = ET.parse(file_path)
        return tree.getroot()
    except FileNotFoundError:
        pass
    except AttributeError:
        pass
```
**xml_to_string(element)**

Converts an XML element to a string.

```python
def xml_to_string(element):
    try:
        return ET.tostring(element, encoding='unicode')
    except AttributeError:
        pass
    except FileNotFoundError:
        pass
```

**compare_xml(file1, file2)**

Compares two XML files and displays the differences in the GUI.

```python
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
```

**GUI Layout**

Defines the layout of the GUI using FreeSimpleGUI.

```python

multiline_one_layout = [
    [sg.Multiline(size=(60, 20), key="-OUTPUT_XML_ONE-", horizontal_scroll=True)],
    [sg.Input(default_text="path/to/xml_config_file", key="-XML_ONE_INPUT-", expand_x=True, enable_events=True), sg.FileBrowse(target="-XML_ONE_INPUT-", file_types=FILE_TYPES)]
]

multiline_two_layout = [
    [sg.Multiline(size=(60, 20), key="-OUTPUT_XML_TWO-", horizontal_scroll=True)],
    [sg.Input(default_text="path/to/xml_config_file", key="-XML_TWO_INPUT-", expand_x=True, enable_events=True), sg.FileBrowse(target="-XML_TWO_INPUT-", file_types=FILE_TYPES)]
]

multiline_difference_output_layout = [
    [sg.Multiline(size=(128, 16), key="-OUTPUT_DIFFERENCE-", disabled=True, horizontal_scroll=True)],
    [sg.Button(button_text="Compare", font="Calibri 13 bold", expand_x=True, button_color=("#191e26", "#449d48"), mouseover_colors=("#191e26", "#367d39"))]
]

# Define frames
multiline_one_frame = sg.Frame("XML Output", multiline_one_layout, title_color=TITLE_COLOR, font=("Calibri 14 bold"))
multiline_two_frame = sg.Frame("XML Output", multiline_two_layout, title_color=TITLE_COLOR, font=("Calibri 14 bold"))
multiline_difference_output_frame = sg.Frame("Difference Output", multiline_difference_output_layout, title_color=TITLE_COLOR, font=("Calibri 14 bold"))

# Define the main layout
layout = [
    [sg.Column([[multiline_one_frame]]), sg.VSeparator(), sg.Column([[multiline_two_frame]], expand_x=True, expand_y=True)],
    [sg.HSep()],
    [sg.Column([[multiline_difference_output_frame]], expand_x=True, expand_y=True)]
]
```

**Event Loop**

Handles events and updates the GUI based on user actions.

```python
while True:
    event, values = window.read()

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
```
## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss your changes.

## License
This project is licensed under the MIT License.

