import lxml.etree as ET
import math
import os
# Load the SVG file
print("")
print("[$] convert <Rect> and <Polygon> element to <Path> elements")
print("-      -     -    -   -  - -->")
print("[$] @sajan-Nethsara GitHub -")
print("")
svg_path = ''
current_directory = os.getcwd()
files = os.listdir(current_directory)
for file in files:
    if file.endswith(('.svg')):
        svg_path = file
if svg_path == '':
    print(".svg file not found")
else:
    print(f"targeted .svg file --> {svg_path}")
    print("")
    abc = input("[*] Press Enter to Continue ... ")

    tree = ET.parse(svg_path)
    root = tree.getroot()

    # Define the namespace for SVG elements
    namespace = {'svg': 'http://www.w3.org/2000/svg'}
    group_id = 'sections'

    # Find the specified group
    group = root.find(f".//svg:g[@id='{group_id}']", namespace)
    # Find and convert polygon elements to path elements
    polygons = group.findall('.//svg:polygon', namespace)
    for polygon in polygons:
        points = polygon.get('points')
        class_attr = polygon.get('class')
        id_attr = polygon.get('id')
        # Create a new path element
        path_element = ET.Element('path', d=f"M{points} Z" )
        path_element.set('class', class_attr )
        if id_attr is not None:
            path_element.set('id', id_attr)

        # Insert the new path element before the polygon element
        parent = polygon.getparent()
        parent.insert(parent.index(polygon), path_element)

        # Remove the polygon element
        parent.remove(polygon)
        print("<polygon> element --> <path> element")

    # Find and convert rect elements to path elements
    rects = root.findall('.//svg:rect', namespace)
    for rect in rects:
        x = float(rect.get('x'))
        y = float(rect.get('y'))
        width = float(rect.get('width'))
        height = float(rect.get('height'))
        class_attr = rect.get('class')
        id_attr = rect.get('id')
        transform = rect.get('transform')
        # Create a new path element
        # path_d = f"M{x},{y}H{x + width}V{y + height}H{x}Z"
        # path_element = ET.Element('path', d=path_d )
        if transform and transform.startswith('matrix'):
            matrix = transform.split('(')[1].split(')')[0].split(' ')
            a = float(matrix[0])
            b = float(matrix[1])
            c = float(matrix[2])
            d = float(matrix[3])
            e = float(matrix[4])
            f = float(matrix[5])
            # Apply transformation matrix to each point
            def transform_point(x, y):
                return (
                    a * x + c * y + e,
                    b * x + d * y + f
                )
            x1, y1 = transform_point(x, y)
            x2, y2 = transform_point(x + width, y)
            x3, y3 = transform_point(x + width, y + height)
            x4, y4 = transform_point(x, y + height)
            # Create the path element with transformed points
            path_element = ET.Element('{http://www.w3.org/2000/svg}path')
            path_element.set('d', f'M{x1},{y1} L{x2},{y2} L{x3},{y3} L{x4},{y4} Z')

        else:
            path_element = ET.Element('{http://www.w3.org/2000/svg}path')
            path_element.set('d', f'M{x},{y} H{x + width} V{y + height} H{x} Z')





        path_element.set('class', class_attr)
        if id_attr is not None:
            path_element.set('id', id_attr)
        # Insert the new path element before the rect element
        parent = rect.getparent()
        parent.insert(parent.index(rect), path_element)
        # Remove the rect element
        parent.remove(rect)
        print("<rect> element --> <path> element")
    # Save the modified SVG file
    new_svg = f"converted-{svg_path}"
    tree.write(new_svg , encoding="UTF-8" , xml_declaration=True)