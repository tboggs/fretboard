
class Fret(object):
    '''Represents an individual fret on a fretboard.'''
    def __init__(self, string, fret, note):
        self.string = string
        self.number = fret
        self.note = note
        self.text = None
        
class FretboardDisplay(object):
    '''Base class for fretboard displays.'''
    def __init__(self, tuning='E A D G B E', nfrets=19):
        '''
        ARGUMENTS:
        
            tuning (str):

                The string tuning for the display. Should be a space-separated
                string of note names.

            nfrets (int):

                Number of frets in the display.
        '''
        self.nfrets = nfrets
        self.create_tuning(tuning)
        self.create_strings()

    def create_tuning(self, tuning_str):
        from ..notes import Note
        names = tuning_str.split()
        tuning = [Note(n) for n in names]
        # Adjust tone across octaves
        for i in range(1, len(tuning)):
            tuning[i] = tuning[i - 1] + tuning[i - 1].interval(tuning[i])
        self.tuning = tuning

    def create_strings(self):
        tuning = list(reversed(self.tuning))
        self.strings = [[Fret(i + 1, j, tuning[i] + j) for j in range(self.nfrets + 1)]
                        for i in range(len(tuning))]

        
        
