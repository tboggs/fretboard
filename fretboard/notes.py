from __future__ import division, print_function, unicode_literals
from .utils import IS_PYTHON3

if IS_PYTHON3:
    import functools
    reduce = functools.reduce

NTONES = 12
CREF = 10000

whole_notes = [n for n in 'CDEFGAB']
sharps = [n + '#' for n in whole_notes]
flats = [n + 'b' for n in whole_notes]

# Names of all notes using sharp notation
notess = list(reduce(lambda a, b: a + b, zip(whole_notes, sharps)))
notess.remove('E#')
notess.remove('B#')

# Names of all notes using float notation
notesb = list(reduce(lambda a, b: a + b, zip(flats, whole_notes)))
notesb.remove('Fb')
notesb.remove('Cb')

def i2ns(i):
    '''Returns name of note (using sharp), given number of semitones above C.'''
    return notess[(i - CREF) % NTONES]

def i2nb(i):
    '''Returns name of note (using flat), given number of semitones above C.'''
    return notesb[(i - CREF) % NTONES]

def n2i(note_name):
    '''Return numeric index of note, given note string.'''
    if note_name[-1] == 'b':
        return n2i(note_name[:-1]) - 1
    elif note_name[-1] == '#':
        return n2i(note_name[:-1]) + 1
    else:
        return CREF + notess.index(note_name)
    
class Note:
    '''Class to represent a musical note.'''
    display_sharp = True

    def __init__(self, tone):
        from .utils import is_string
        if is_string(tone):
            if len(tone) == 2 and tone[-1] == 'b':
                self.display_sharp = False
            tone = n2i(tone)
        while tone < 0:
            tone += NTONES
        self.tone = tone
        self.value = tone % NTONES

    def __str__(self):
        if self.display_sharp:
            return i2ns(self.value % NTONES)
        else:
            return i2nb(self.value % NTONES)

    def __eq__(self, note):
        if type(note) in (int, str):
            note = Note(note)
        return self.value == note.value

    def __ne__(self, note):
        return not (self == note)

    def __repr__(self):
        return str(self)

    def __add__(self, semitones):
        return Note(self.tone + semitones)

    def __sub__(self, lower):
        if isinstance(lower, int):
            # Return the note `lower` tones below this one.
            return Note(self.tone - lower)
        else:
            # Return the number of semitones between the two notes.
            return self.tone - lower.tone

    def interval(self, note):
        '''Return number of semitones up to next instance of `note`.'''
        return interval(self, note)

def interval(note1, note2):
    '''Return number of semitones from `note1` to next instance of `note2`.'''
    (t1, t2) = (note1.tone, note2.tone)
    if t2 >= t1:
        return (t2 - t1) % NTONES
    else:
        return NTONES - (t1 - t2) % NTONES
