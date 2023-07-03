# importing libs
from bs4 import BeautifulSoup
import pandas as pd
from colorama import Fore, Back, Style
from pyfiglet import figlet_format

# global variables
excel_path = 'input.xlsx'
svg_path = 'input.svg'

# basic functions


def convert_string(string):
    # Convert string to lowercase
    converted_string = str(string)
    lower_string = converted_string.lower()

    # Remove spaces from the string
    no_space_string = lower_string.replace(" ", "")

    return no_space_string


def get_excel_array(sheet, n):
    row_array = sheet.iloc[:, n].values
    return row_array


def convert_string_array(arr):
    converted = list(map(convert_string, arr))
    return converted

# making element names


def get_label_id(input_string):
    split_string = input_string.split("-")
    split_string[-1] = "label"
    modified_string = "-".join(split_string)
    return modified_string


def get_group_id(input_string):
    split_string = input_string.split("-")
    split_string[-1] = "group"
    modified_string = "-".join(split_string)
    return modified_string


def get_section_id(input_string):
    split_string = input_string.split("-")
    split_string[-1] = "section"
    modified_string = "-".join(split_string)
    return modified_string


# to main functions

def find_inner_text(text_element):
    inner_text = ""
    for child in text_element.children:
        if child.name == "tspan":
            inner_text += child.get_text()
        else:
            inner_text += child.get_text()
    return inner_text


def get_map_text_converted_array(sheet):
    map_text = get_excel_array(sheet, 0)
    converted = convert_string_array(map_text)
    return converted

def get_map_id_converted_array(sheet):
    map_id = get_excel_array(sheet, 2)
    converted = convert_string_array(map_id)
    return converted


# main functions
def handel_suites(element):

    suites_text_array = element.find_all("text")
    for suite in suites_text_array:
        inner_text = find_inner_text(suite)
        suite_text_converted = convert_string(inner_text)
        name = f"suites-{suite_text_converted}-label"
        suite["id"] = name
    suite_path_element = element.find("path")
    if suite_path_element == None:
        print(Fore.RED + f"err --> <path> element not found in suites group")        
    else:
        suite_path_element["id"] = "suites-section"
    print(Fore.BLUE + f"Suites Group renamed successfully")


def manipulate_svg(map_text_list, map_id_list):
    # return soup
    error_count = 0
    try:

        with open(svg_path, "r") as f:
            soup = BeautifulSoup(f, "lxml-xml")
    except:
        print(Fore.RED + "Error with loading SVG file")
        print(Style.RESET_ALL + '---')

    section = soup.find(id="sections")
    all_group_elements = section.find_all("g", recursive=False)
    for element in all_group_elements:
        element_id = element.get("id")
        if element_id == "suites-group" :
            handel_suites(element)
        else:    
            text_element = element.find("text")
            inner_text = find_inner_text(text_element)
            inner_text_modified = convert_string(inner_text)
            try:
                search_index = map_text_list.index(inner_text_modified)
            except ValueError as e:
                error_count += 1
                print(Fore.RED + f"The --> {inner_text} <text> element is not in the excel file")
            map_id = map_id_list[search_index]
            group_name = get_group_id(map_id)
            section_name = get_section_id(map_id)
            label_name = get_label_id(map_id)

            # renaming process
            element["id"] = group_name
            text_element["id"] = label_name
            next_sibling = text_element.find_next_sibling()
            previous_sibling = text_element.find_previous_sibling()
            # renaming
            if next_sibling:
                next_sibling["id"] = section_name
                print(Fore.GREEN + f"Rename process success {section_name}")
            elif previous_sibling:
                previous_sibling["id"] = section_name
                print(Fore.GREEN + f"Rename process success {section_name}")

            else:
                error_count += 1
                print(Fore.RED + f"<Path> | <Polygon> element for {inner_text} not found in svg")
                print(Style.RESET_ALL + '---')

    if error_count == 0:
        print(Back.GREEN + f"Operation completed successfully")
        print(Style.RESET_ALL + '- Done -')
    else:
        print(Back.RED + f"{error_count} errors found! try again with fixing bugs")
        print(Style.RESET_ALL + '---')
    return soup

def ui_art ():
    asci1 = figlet_format("ReNaMeR.pY")
    print(asci1)
    asci2 = figlet_format("@sajan-Nethsara GitHub", font = "digital" )
    print(asci2)


# the ultimate Main


def main():
    ui_art()
    start = input("Press Enter to continue...")
    try:
        sheet = pd.read_excel(excel_path)
        map_text_list = get_map_text_converted_array(sheet)
        map_id_list = get_map_id_converted_array(sheet)
    except:
        print(Back.RED + "Error with loading EXCEL file")
        print(Style.RESET_ALL + '---')
    new_soup = manipulate_svg(map_text_list, map_id_list)
    modified_svg_content = str(new_soup)
    with open("output.svg", "w") as output_file:
        output_file.write(modified_svg_content)
        print("output.svg file created")
main()
