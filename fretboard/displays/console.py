from .common import FretboardDisplay

class Console(FretboardDisplay):
    '''A class for displaying fretboards in ASCII text.'''
    fret_fill_char = '-'
    fret_empty_fill_char = '-'
    fret_sep = '|'
    fret_width = 3
    neck_edge_char = '='
    
    def display_scale(self, scale, fmt='note'):
        '''Display output for each fret belonging to `scale`.

        ARGUMENTS:

            scale (`Scale` object):

                The scale for which to display frets.

            fmt (`str` or callable):

                Format specifier. One of the following:

                - "note" to display note name
                - "interval" to display interval for the note within the scale
                - <single char> to display the same char for each scale note
                - <callable> displays the output of the supplied function
                  when applied to the corresponding `Fret` object. Each `Fret`
                  has the following attributes:

                      - `string` (int): the string number (starting at 1)
                      - `number` (int): the fret number
                      - `note` (`Note`): the note corresponding to the fret
        '''
        if isinstance(fmt, str):
            if fmt.lower() == 'note':
                f = lambda fret: str(fret.note)
            elif fmt.lower() == 'interval':
                f = lambda fret: scale.get_interval_name(fret.note)
            else:
                f = lambda fret: fmt
        else:
            f = fmt
        for string in self.strings:
            for fret in string:
                if fret.note in scale:
                    fret.text = f(fret)

    def display_fret(self, string, fret, fmt='note'):
        '''Display output for the indicated fret.

        ARGUMENTS:

            string (int):

                The string (starting at 1 for highest string) for which to
                display the fret.

            fret (int):

                The number of the fret (0 for open string)

            fmt (`str` or callable):

                Format specifier. One of the following:

                - "note" to display note name
                - <single char> to display the same char for each scale note
                - <callable> displays the output of the supplied function
                  when applied to the corresponding `Fret` object. Each `Fret`
                  has the following attributes:

                      - `string` (int): the string number (starting at 1)
                      - `number` (int): the fret number
                      - `note` (`Note`): the note corresponding to the fret
        '''
        if isinstance(fmt, str):
            if fmt.lower() == 'note':
                f = lambda fret: str(fret.note)
            else:
                f = lambda fret: fmt
        else:
            f = fmt
        fret = self.strings[string - 1][fret]
        fret.text = f(fret)

    def get_fret_string(self, fret, unformatted=False):
        '''Returns the formatted text to be displayed for the given fret.'''
        if unformatted is True:
            # Return raw fret text without background formatting
            if fret.text is None:
                return ''
            else:
                 return fret.text
        if fret.text is None:
            return self.fret_empty_fill_char * self.fret_width
        else:
            spec = '{:%s^%ss}' % (self.fret_fill_char, self.fret_width)
            return spec.format(fret.text)

    def show(self, tuning=True, fmin=None, fmax=None, invert=False,
             fret_numbers='bottom'):
        '''Prints the current display to stdout.
        ARGUMENTS:

            tuning (boolean):

                True if string tuning should be displayed

            fmin (int or None):

                Index of the lowest fret to show. Value of 0 or None will
                start at open string.

            fmax (int or None):

                Index of highst fret to show. Value of None will display all
                frets.

            invert (bool, default False):

                If True, lowest string will be shown at top of display.

            fret_numbers (str):

                Indicates where fret number labels shold be shown.
        '''
        print self.get_display(tuning=tuning, fmin=fmin, fmax=fmax,
                               invert=invert, fret_numbers=fret_numbers)

    def get_display(self, tuning=True, fmin=None, fmax=None, invert=False,
             fret_numbers='bottom'):
        '''Prints the current display to stdout.
        ARGUMENTS:

            tuning (boolean):

                True if string tuning should be displayed

            fmin (int or None):

                Index of the lowest fret to show. Value of 0 or None will
                start at open string.

            fmax (int or None):

                Index of highst fret to show. Value of None will display all
                frets.

            invert (bool, default False):

                If True, lowest string will be shown at top of display.

            fret_numbers (str):

                Indicates where fret number labels shold be shown.
        '''
        if fmin is None:
            fmin = 0
        if fmax is None:
            fmax = self.nfrets + 1

        fret_strings = [[self.get_fret_string(f) for f in s]
                        for s in self.strings]

        if tuning is True:
            # Display string tuning on left side of output
            pre_frets = ['{:<3s}  '.format(n) for n in reversed(self.tuning)]
        else:
            pre_frets = ['' for n in self.tuning]

        if fmin == 0:
            # Display open string notes
            for i in range(len(self.strings)):
                pre_frets[i] = \
                  '%s%2s%s' % (pre_frets[i],
                               self.get_fret_string(self.strings[i][0],
                                                    unformatted=True),
                                                    self.fret_sep)

        # Text for all frets to be displayed
        imin = max(1, fmin)
        fret_lines = [self.fret_sep.join([''] + s[imin : fmax + 1] + [''])
                      for s in fret_strings]
        lines = [pre_frets[i] + fret_lines[i] for i in range(len(fret_lines))]

        if invert is True:
            lines = list(reversed(lines))

        # Text for neck edges (before first string and after last).
        neck_edge = ' ' * len(pre_frets[0]) + \
          self.neck_edge_char * len(fret_lines[0])
        lines = [neck_edge] + lines + [neck_edge]

        if not (fret_numbers is None or fret_numbers.lower() == 'none'):
            # Labels to indicate fret number
            labels = self.get_fret_number_labels()[imin:fmax + 1]
            fmt = '{:^%ds}' % self.fret_width
            fret_number_str = ' ' * (len(pre_frets[0]) + 1) + ' '.join(
                [fmt.format(s) for s in labels])
            loc = fret_numbers.lower()
            if loc == 'bottom':
                lines.append(fret_number_str)
            elif loc == 'top':
                lines = [fret_number_str] + lines
            else:
                raise ValueError('Invalid value for `fret_numbers arg.')
        return '\n'.join(lines)

    def get_fret_number_labels(self):
        '''Returns list of strings for standard guitar fret labels.'''
        from ..notes import NTONES
        labels = [str(i) if i % NTONES in (0, 3, 5, 7, 9) else ''
                  for i in range(self.nfrets + 1)]
        return labels

def show_scale(scale, tuning='E A D G B E', nfrets=19, fmt='note', fmin=None,
               fmax=None, invert=False, fret_numbers='bottom'):
    '''Prints a scale to stdout.
    
        ARGUMENTS:

            scale (`Scale`):

                Scale to be shown
                
            tuning (str):

                The string tuning for the display. Should be a space-separated
                string of note names.

            nfrets (int):

                Number of frets in the display.

            fmin (int or None):

                Index of the lowest fret to show. Value of 0 or None will
                start at open string.

            fmax (int or None):

                Index of highst fret to show. Value of None will display all
                frets.

            invert (bool, default False):

                If True, lowest string will be shown at top of display.

            fret_numbers (str):

                Indicates where fret number labels shold be shown.

            fmt (`str` or callable):

                Format specifier. One of the following:

                - "note" to display note name
                - "interval" to display interval for the note within the scale
                - <single char> to display the same char for each scale note
                - <callable> displays the output of the supplied function
                  when applied to the corresponding `Fret` object. Each `Fret`
                  has the following attributes:

                      - `string` (int): the string number (starting at 1)
                      - `number` (int): the fret number
                      - `note` (`Note`): the note corresponding to the fret
    '''
    c = Console(tuning=tuning, nfrets=nfrets)
    c.display_scale(scale, fmt=fmt)
    c.show(fmin=fmin, fmax=fmax, invert=invert, fret_numbers=fret_numbers)
    
