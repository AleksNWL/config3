import sys
import xml.etree.ElementTree as ET
from config_parser import parse_config

def main():
    output_file = "output.xml"

    if len(sys.argv) >= 2:
        output_file = sys.argv[1]
    
    print("Введите конфигурацию (нажмите Ctrl+Z, чтобы закончить ввод):")
    config = sys.stdin.read()

    parsed_config = parse_config(config)

    root = ET.Element("config")

    def dict_to_xml(d, parent):
        for key, value in d.items():
            element = ET.SubElement(parent, key)
            if isinstance(value, dict):
                dict_to_xml(value, element)
            else:
                element.text = str(value)

    dict_to_xml(parsed_config, root)

    tree = ET.ElementTree(root)

    xml_str = ET.tostring(root, encoding="utf-8", xml_declaration=True).decode()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_str)

    print(f"Config has been successfully written to {output_file}")

if __name__ == "__main__":
    main()
