from abc import ABC, abstractmethod


class SvgPathCommandException(BaseException):
    pass


class SvgPathCommandInsufficientParametersException(SvgPathCommandException):
    pass


class SvgPathCommandTooManyParametersException(SvgPathCommandException):
    pass


class SvgPathDoesntBeginWithMException(SvgPathCommandException):
    pass


class SvgPathCommandNotImplementedException(SvgPathCommandException):
    pass


class SvgPathCommandFactory:
    required_num_of_parameters = {
        'M': 2,
        'm': 2,
        'V': 1,
        'v': 1,
        'L': 2,
        'l': 2,
        'H': 1,
        'h': 1,
        'Z': 0,
        'z': 0,
        'C': 6,
        'c': 6,
    }

    subsequent_command = {
        'M': 'L',
        'm': 'l',
        'V': 'V',
        'v': 'v',
        'L': 'L',
        'l': 'l',
        'H': 'H',
        'h': 'h',
        'Z': 'Z',
        'z': 'z',
        'C': 'C',
        'c': 'c',
    }

    def __init__(self):
        self.KNOWN_COMMANDS = self.required_num_of_parameters.keys()
        self._pathstart = []
        self._subpath_index = -1

    def get_required_num_of_parameters(self, type):
        if type not in self.KNOWN_COMMANDS:
            raise NotImplementedError
        return self.required_num_of_parameters[type]

    def get_command(self, type, parameters, isFirst: bool = False):
        if type not in self.KNOWN_COMMANDS:
            raise SvgPathCommandNotImplementedException()

        if len(parameters) < self.required_num_of_parameters[type]:
            raise SvgPathCommandInsufficientParametersException()
        elif len(parameters) > self.required_num_of_parameters[type]:
            raise SvgPathCommandTooManyParametersException()

        if type == 'M':
            command = MSvgPathCommand(parameters)
            self._subpath_index += 1
            self._pathstart.append(command.get_pathstart())
        elif type == 'L':
            command = LSvgPathCommand(parameters)
        elif type == 'H':
            command = HSvgPathCommand(parameters)
        elif type == 'V':
            command = VSvgPathCommand(parameters)
        elif type == 'm':
            if isFirst:
                command = MSvgPathCommand(parameters)
            else:
                command = mSvgPathCommand(parameters)
            self._subpath_index += 1
            self._pathstart.append(command.get_pathstart())
        elif type == 'l':
            command = lSvgPathCommand(parameters)
        elif type == 'h':
            command = hSvgPathCommand(parameters)
        elif type == 'v':
            command = vSvgPathCommand(parameters)
        elif type.lower() == 'z':
            command = ZSvgPathCommand(parameters, pathstart=self._pathstart[self._subpath_index])
        else:
            raise SvgPathCommandNotImplementedException

        return command

    def tokenize_pathdata(self, pathdata):

        # attempt to put a space in between all parameters and commands
        for command in self.KNOWN_COMMANDS:
            pathdata = pathdata.replace(command, ' ' + command + ' ')
        pathdata = pathdata.replace('-', ' -')
        pathdata = pathdata.replace(',', ' ')

        while '  ' in pathdata:
            pathdata = pathdata.replace('  ', ' ')

        pathdata = pathdata.strip()

        # find the corner case where 50.1.45 should be 50.1 0.45
        need_space_here = []
        looking_for_space = False
        for index, character in enumerate(pathdata):
            if character == '.' and not looking_for_space:
                looking_for_space = True
            elif character == '.' and looking_for_space:
                looking_for_space = True
                need_space_here.append(index)
            elif character == ' ':
                looking_for_space = False

        offset = 0
        for index in need_space_here:
            pathdata = pathdata[:index + offset] + ' 0' + pathdata[index + offset:]
            offset += 2

        tokens = pathdata.split(' ')
        if not tokens[0].lower() == 'm':
            raise SvgPathDoesntBeginWithMException()

        return tokens

    def append_types_and_parameter_lists(self, types, parameters, current_command, current_parameters):
        assert current_command in self.KNOWN_COMMANDS
        n_params = self.required_num_of_parameters[current_command]
        n_found = len(current_parameters)

        if n_found == n_params:
            types.append(current_command)
            parameters.append(current_parameters)
        elif n_found > n_params > 0:
            # add one command of the prescribed type
            types.append(current_command)
            parameters.append(current_parameters[:n_params])
            current_parameters = current_parameters[n_params:]
            # following parameters belong to the implied subsequent types, as per the standard
            while len(current_parameters) > n_params:
                if current_command == 'M':
                    next_command = 'L'
                if current_command == 'm':
                    next_command = 'l'
                else:
                    next_command = current_command

                types.append(next_command)
                n_needed = self.required_num_of_parameters[next_command]
                parameters.append(current_parameters[:n_needed])
                current_parameters = current_parameters[n_needed:]

        elif len(current_parameters) > n_params == 0:
            raise SvgPathCommandTooManyParametersException()
        elif len(current_parameters) < n_params:
            raise SvgPathCommandInsufficientParametersException()

        return types, parameters

    def extract_commands_from_pathdata(self, pathdata):
        tokens = self.tokenize_pathdata(pathdata)

        types = []
        parameters = []

        current_command = None
        current_parameters = []
        for token in tokens:
            if token.isalpha():
                assert token in self.KNOWN_COMMANDS
                if current_command is not None:
                    types, parameters = self.append_types_and_parameter_lists(
                        types,
                        parameters,
                        current_command,
                        current_parameters,
                    )
                current_command = token
                current_parameters = []
            elif current_command is not None:
                current_parameters.append(float(token))
            elif token == '':
                continue
            else:
                raise BaseException()

        types, parameters = self.append_types_and_parameter_lists(
            types,
            parameters,
            current_command,
            current_parameters,
        )

        # the first M command will always be expressed in absolute terms
        # it's in the spec like that!
        if types[0] == 'm':
            types[0] = 'M'

        return (types, parameters)


class SvgPathCommand(ABC):
    def __init__(self, type, parameters):
        self.type = type
        self.parameters = parameters

    @abstractmethod
    def get_next_vertex(self, current_vertex):
        pass


class MSvgPathCommand(SvgPathCommand):
    def __init__(self, parameters):
        super().__init__('M', parameters)

    def get_next_vertex(self, current_vertex):
        next_vertex = (self.parameters[0], self.parameters[1])
        return next_vertex

    def get_pathstart(self):
        return (self.parameters[0], self.parameters[1])


class mSvgPathCommand(SvgPathCommand):
    def __init__(self, parameters):
        super().__init__('m', parameters)

    def get_next_vertex(self, current_vertex):
        next_vertex = (current_vertex[0] + self.parameters[0], current_vertex[1] + self.parameters[1])
        return next_vertex

    def get_pathstart(self):
        return (self.parameters[0], self.parameters[1])


class VSvgPathCommand(SvgPathCommand):
    def __init__(self, parameters):
        super().__init__('V', parameters)

    def get_next_vertex(self, current_vertex):
        next_vertex = (current_vertex[0], self.parameters[0])
        return next_vertex


class vSvgPathCommand(SvgPathCommand):
    def __init__(self, parameters):
        super().__init__('v', parameters)

    def get_next_vertex(self, current_vertex):
        next_vertex = (current_vertex[0], self.parameters[0] + current_vertex[1])
        return next_vertex


class LSvgPathCommand(SvgPathCommand):
    def __init__(self, parameters):
        super().__init__('L', parameters)

    def get_next_vertex(self, current_vertex):
        next_vertex = (self.parameters[0], self.parameters[1])
        return next_vertex


class lSvgPathCommand(SvgPathCommand):
    def __init__(self, parameters):
        super().__init__('l', parameters)

    def get_next_vertex(self, current_vertex):
        next_vertex = (self.parameters[0] + current_vertex[0], self.parameters[1] + current_vertex[1])
        return next_vertex


class HSvgPathCommand(SvgPathCommand):
    def __init__(self, parameters):
        super().__init__('H', parameters)

    def get_next_vertex(self, current_vertex):
        next_vertex = (self.parameters[0], current_vertex[1])
        return next_vertex


class hSvgPathCommand(SvgPathCommand):
    def __init__(self, parameters):
        super().__init__('h', parameters)

    def get_next_vertex(self, current_vertex):
        next_vertex = (self.parameters[0] + current_vertex[0], current_vertex[1])
        return next_vertex


class ZSvgPathCommand(SvgPathCommand):
    def __init__(self, parameters, pathstart=None):
        super().__init__('Z', parameters)
        self._pathstart = pathstart

    def get_next_vertex(self, current_vertex):
        if self._pathstart is not None:
            next_vertex = self._pathstart
        else:
            raise Exception(msg='No path start to go to!')
        return next_vertex
