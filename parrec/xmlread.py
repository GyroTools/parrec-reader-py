import os
import re
import xml.etree.ElementTree as ET


class Xmlread:
    INTEGER_TYPES = {'Int8', 'Int16', 'Int32', 'Int64', 'UInt8', 'UInt16', 'UInt32', 'UInt64'}
    FLOAT_TYPES = {'Float', 'Double'}

    def __init__(self, filename):
        self.xmlfile = filename

    def read(self):
        tree = ET.parse(self.xmlfile)
        root = tree.getroot()

        pars = self._read_series_info(root)
        pars['ImageInformation'] = self._read_image_array(root)

        return pars

    @staticmethod
    def get_xmlfile(filename):
        basename, file_extension = os.path.splitext(filename)
        if file_extension.lower() == '.rec':
            xmlfile = basename + '.xml'
            if not os.path.exists(xmlfile):
                xmlfile = basename + '.XML'
                if not os.path.exists(xmlfile):
                    raise FileNotFoundError('Cannot find the corresponding XML file')
            return xmlfile
        elif file_extension.lower() == '.xml':
            return filename

    def _read_series_info(self, root):
        pars = {}
        series_info = root.find('Series_Info')
        if series_info is None:
            return pars

        for attr in series_info.findall('Attribute'):
            key = self._to_valid_key_name(attr.get('Name', ''))
            pars[key] = self._parse_attribute(attr)

        return pars

    def _read_image_array(self, root):
        images = []
        image_array = root.find('Image_Array')
        if image_array is None:
            return images

        for image_info in image_array.findall('Image_Info'):
            image = {}

            key_elem = image_info.find('Key')
            if key_elem is not None:
                for attr in key_elem.findall('Attribute'):
                    key = self._to_valid_key_name(attr.get('Name', ''))
                    image[key] = self._parse_attribute(attr)

            for attr in image_info.findall('Attribute'):
                key = self._to_valid_key_name(attr.get('Name', ''))
                image[key] = self._parse_attribute(attr)

            images.append(image)

        return images

    def _parse_attribute(self, attr):
        type_str = attr.get('Type', 'String')
        text = (attr.text or '').strip()

        if attr.get('ArraySize') is not None:
            return [self._convert_value(v, type_str) for v in text.split()]

        return self._convert_value(text, type_str)

    def _convert_value(self, value_str, type_str):
        if type_str in self.INTEGER_TYPES:
            try:
                return int(value_str)
            except ValueError:
                return value_str
        elif type_str in self.FLOAT_TYPES:
            try:
                return float(value_str)
            except ValueError:
                return value_str
        else:
            return value_str

    @staticmethod
    def _to_valid_key_name(name):
        name = name.split('(')[0].split('[')[0].split('<')[0]
        name = re.sub('[^0-9a-zA-Z ]+', ' ', name)
        name = name.title()
        name = name.replace(' ', '')
        return name
