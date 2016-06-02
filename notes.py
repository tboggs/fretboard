import numpy as np

NTONES = 12

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
    return notess[i % NTONES]

def i2nb(i):
    '''Returns name of note (using flat), given number of semitones above C.'''
    return notesb[i % NTONES]

def n2i(note_name):
    '''Return numeric index of note, given note string.'''
    if 'b' in note_name:
        return notesb.index(note_name)
    else:
        return notess.index(note_name)
    
class Note:
    display_sharp = True
    def __init__(self, tone):
        if type(tone) == str:
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
