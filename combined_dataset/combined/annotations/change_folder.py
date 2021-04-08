import glob
import os
import xml.etree.ElementTree as ET
from pathlib import Path

for xml_file in glob.glob("*.xml"):
    tree = ET.parse(xml_file)
    name = Path(xml_file).stem
    root = tree.getroot()
    folder_name = root.find('folder').text
    tree.find('folder').text = 'images'
    tree.find('filename').text = str(name) + '.jpg'
    tree.write(xml_file)
