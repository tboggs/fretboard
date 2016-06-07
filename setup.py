from distutils.core import setup

setup(name='fretboard',
      version='0.1',
      description='A module for displaying guitar notes, chords, and scales.',
      author='Thomas Boggs',
      author_email='thomas.boggs@gmail.com',
      license='GPL',
      url='http://github.com/tboggs/fretboard',
      download_url='https://github.com/tboggs/fretboard/releases/latest',
      packages=['fretboard', 'fretboard.displays',],
      platforms=['Platform-Independent'],
      classifiers=[	'Development Status :: 4 - Beta',
                    'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python :: 2.6',
                    'Programming Language :: Python :: 2.7',
                    'Environment :: Console',
                    'Natural Language :: English',
                    'Topic :: Education',
      ]
)
