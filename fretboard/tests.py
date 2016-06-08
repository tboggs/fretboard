from __future__ import division, print_function, unicode_literals
import unittest
from . import scales

def notes_are_equal(a, b):
    from .utils import is_string
    from .notes import Note
    if is_string(b):
        b = [Note(n) for n in b.split()]
    if len(a) != len(b):
        return False
    for (n1, n2) in zip(a, b):
        if n1 != n2:
            return False
    return True

class FretboardTest(unittest.TestCase):
    pass

class ScaleTest():
    key = 'A'
    def setUp(self):
        self.scale = self.ScaleClass(self.key)
    def test_first_note_is_key(self):
        from .notes import Note
        s = self.ScaleClass(self.key)
        a = Note(self.key)
        assert(s.notes[0] == a)
        assert(s.root == a)
    def test_print_scale(self):
        print(self.scale)

class DiatonicScaleTest(ScaleTest, FretboardTest):
    ScaleClass = scales.Diatonic
    def test_diatonic_mode_6_is_minor(self):
        from .notes import Note
        aminor = self.ScaleClass('A', mode=6)
        assert(notes_are_equal(aminor.notes, 'A B C D E F G'))
        
class MajorScaleTest(ScaleTest, FretboardTest):
    ScaleClass = scales.Major
    def test_cmajor_notes_are_correct(self):
        from .notes import Note
        cmajor = self.ScaleClass('C')
        assert(notes_are_equal(cmajor.notes, 'C D E F G A B'))

class MinorScaleTest(ScaleTest, FretboardTest):
    ScaleClass = scales.Minor
    def test_aminor_notes_are_correct(self):
        from .notes import Note
        cminor = self.ScaleClass('A')
        assert(notes_are_equal(cminor.notes, 'A B C D E F G'))

class BluesScaleTest(ScaleTest, FretboardTest):
    ScaleClass = scales.Blues

class HarmonicScaleTest(ScaleTest, FretboardTest):
    ScaleClass = scales.HarmonicMinor

class ConsoleTest(FretboardTest):
    def setUp(self):
        from .scales import Minor
        self.scale = Minor('A')
    def test_show_scale_default(self):
        from .displays import console
        console.show_scale(self.scale)
    def test_show_scale_with_intervals(self):
        from .displays import console
        console.show_scale(self.scale, fmt='interval')
    def test_show_scale_with_fmin(self):
        from .displays import console
        console.show_scale(self.scale, fmin=3)
    def test_show_scale_with_fmax(self):
        from .displays import console
        console.show_scale(self.scale, fmax=5)
    def test_show_scale_with_callable(self):
        from .displays import console
        scale = self.scale
        console.show_scale(self.scale,
                           fmt=lambda f: 'R' if f.note == scale.root else '*')

