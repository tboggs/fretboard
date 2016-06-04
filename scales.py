import numpy as np
from .notes import Note

__all__ = ['Scale', 'Major', 'Minor', 'HarmonicMinor', 'Pentatonic',
           'MinorPentatonic', 'Blues']

MAJOR = [2, 2, 1, 2, 2, 2, 1]
PENTATONIC = [2, 2, None, 3, 2, None, 3]
INTERVAL_NAMES = ['R', 'm2', 'M2', 'm3', 'M3', '4', '5b', '5', 'm6', 'M6',
                  'm7', 'M7']

class Scale(object):
    '''Base class for scales.'''
    def __init__(self, key):
        self.key = key
        self.root = Note(key)
        self.create_notes()
        self.interval_names = INTERVAL_NAMES[:]

    def level(self, i):
        return self.notes[level - 1]

    def create_notes(self):
        raise NotImplementedError('Class Scale must be subclassed.')

    def get_scale_degree(self, note):
        if note not in self.notes:
            raise ValueError('Note is not in scale')
        return str(self.notes.index(note) + 1)

    def get_interval_name(self, note):
        '''Returns the interval associated with `note` for the scale.'''
        from .notes import Note
        if isinstance(note, str):
            return self.get_interval_name(Note(note))
        return self.interval_names[self.root.interval(note)]

    def __iter__(self):
        for t in self.notes:
            yield t

    def __getitem__(self, i):
        if i < 1 or i > len(self.notes):
            raise ValueError(str(i))
        return self.notes[i - 1]

    def __str__(self):
        return '[{}]'.format(', '.join([str(n) for n in self.notes]))

class Major(Scale):
    '''Major Diatonic Scale.'''
    def __init__(self, key, mode=1):
        '''Creates the major diatonic scale.

        ARGUMENTS:

            key (str):

                Name of the key note for the scale

            mode (int, default 1):

                Mode associated with the diatonic scale (e.g., mode=6
                corresponds to the minor diatonic scale).
        '''
        self.mode = mode
        super(Major, self).__init__(key)

    def create_notes(self):
        intervals = np.roll(MAJOR, -(self.mode - 1))[:-1]
        self.notes = [Note(self.key)]    
        for i in intervals:
            self.notes.append(self.notes[-1] + i)

class Minor(Major):
    '''Minor Diatonic Scale.'''
    def __init__(self, key):
        '''Creates the minor diatonic scale.

        ARGUMENTS:

            key (str):

                Name of the key note for the scale
        '''
        super(Minor, self).__init__(key, 6)

class HarmonicMinor(Minor):
    def create_notes(self):
        super(HarmonicMinor, self).create_notes()
        self.notes[-1] = self.notes[-1] + 1

class Pentatonic(Scale):
    def __init__(self, key, mode=1):
        '''Creates the pentatonic scale.

        ARGUMENTS:

            key (str):

                Name of the key note for the scale

            mode (int, default 1):

                Mode associated with the pentatonic scale. The default value
                of 1 corresponds to the major pentatonic scale.
        '''
        self.mode = mode
        super(Pentatonic, self).__init__(key)

    def create_notes(self):
        intervals = np.roll(PENTATONIC, -(self.mode - 1))
        intervals = [i for i in intervals if i is not None][:-1]
        self.notes = [Note(self.key)]    
        for i in intervals:
            self.notes.append(self.notes[-1] + i)

class MinorPentatonic(Pentatonic):
    def __init__(self, key):
        '''Creates the pentatonic scale.

        ARGUMENTS:

            key (str):

                Name of the key note for the scale
        '''
        super(MinorPentatonic, self).__init__(key, mode=6)

class Blues(Scale):
    def __init__(self, key):
        '''Creates the blues scale.

        ARGUMENTS:

            key (str):

                Name of the key note for the scale
        '''
        super(Blues, self).__init__(key)

    def create_notes(self):
        pm = MinorPentatonic(self.key)
        self.notes = [note for note in pm]
        flat5 = self.notes[3] - 1
        flat5.display_sharp = False
        self.notes.insert(3, flat5)
        self.degrees = ['1', '3', '4', '5b', '5', '7']

    def get_scale_degree(self, note):
        if note not in self.notes:
            raise ValueError('Note is not in scale')
        return self.degrees[self.notes.index(note)]

