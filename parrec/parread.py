import os
import re


class Parread:
    NONE = 0
    INTEGER = 1
    FLOAT = 2
    STRING = 3

    def __init__(self, filename):
        self.parfile = filename

    def read(self):
        with open(self.parfile) as file:
            pars = self._read_upper_part(file)
            pars['ImageInformation'] = self._read_lower_part(file)

        return pars

    @staticmethod
    def get_parfile(filename):
        basename, file_extension = os.path.splitext(filename)
        if file_extension.lower() == '.rec':
            parfile = basename + '.par'
            if not os.path.exists(parfile):
                parfile = basename + '.PAR'
                if not os.path.exists(parfile):
                    raise FileNotFoundError('Cannot find the corresponding PAR file')
            return parfile
        elif file_extension.lower() == '.par':
            return filename

    def _read_upper_part(self, file):
        pars = dict()
        found_start = False
        found_parameter = False
        for line in file:
            line = line.strip()
            if '# === GENERAL INFORMATION' in line:
                found_start = True

            if found_start:
                if (found_parameter and (not line or line[0] != '.')) or ('# === PIXEL VALUES =' in line):
                    break

                if not line or line[0] == '#':
                    continue

                name_value = line.split(':')
                if len(name_value) > 1 and len(name_value[0]) > 1:
                    key = self._to_valid_key_name(name_value[0][1:])
                    value = self.to_value(':'.join(name_value[1:]).strip())
                    pars[key] = value
                    found_parameter = True

        return pars

    def _read_lower_part(self, file):
        pars = []
        definitions = self._get_information_pars_definition(file)
        for line in file:
            line = line.strip()
            cur_par = dict()
            if not line or line[0] == '#':
                continue

            values = line.split()
            for definition in definitions:
                value = []
                if values and len(values) >= definition[2]:
                    if definition[1] == Parread.INTEGER:
                        for v in range(0, definition[2]):
                            value.append(int(values[0]))
                            values.pop(0)
                    elif definition[1] == Parread.FLOAT:
                        for v in range(0, definition[2]):
                            value.append(float(values[0]))
                            values.pop(0)
                    elif definition[1] == Parread.STRING:
                        for v in range(0, definition[2]):
                            value.append(values[0])
                            values.pop(0)

                    if len(value) == 1:
                        value = value[0]

                    cur_par[definition[0]] = value

            pars.append(cur_par)
        return pars

    def _to_valid_key_name(self, name):
        name = name.split('(')[0].split('[')[0].split('<')[0]
        name = re.sub('[^0-9a-zA-Z ]+', ' ', name)
        name = name.title()
        name = name.replace(' ', '')
        return name

    def to_value(self, value_str):
        v = value_str.split()
        try:
            va = [int(cur_v) for cur_v in v]
            final_value = va
            if len(final_value) == 1:
                final_value = final_value[0]
        except:
            try:
                va = [float(cur_v) for cur_v in v]
                final_value = va
                if len(final_value) == 1:
                    final_value = final_value[0]
            except:
                final_value = value_str

        return final_value

    def _get_information_pars_definition(self, file):
        definitions = []
        found_start = False
        pattern = '^#.*?\(.*?\)'
        for line in file:
            line = line.strip()
            if '# === IMAGE INFORMATION DEFINITION' in line:
                found_start = True

            if found_start:
                if '# === IMAGE INFORMATION ==' in line:
                    break

                if not re.match(pattern, line):
                    continue

                array_pattern = '\((\d+)\*\w+\)'
                m = re.search(array_pattern, line)
                if m:
                    array_length = int(m.group(1))
                else:
                    array_length = 1

                name = self._to_valid_key_name(line[1:])

                if 'integer' in line:
                    value_type = Parread.INTEGER
                elif 'float' in line:
                    value_type = Parread.FLOAT
                elif 'string' in line:
                    value_type = Parread.STRING
                else:
                    raise ValueError('Cannot determine the type of ' + name)

                definitions.append((name, value_type, array_length))

        return definitions
