import argparse
import sys

import music21
from music21 import converter
from music21.tempo import MetronomeMark
from music21.stream import Stream

import chord_search
import viterbi

# Halo
HALO_MELODY = """
tinynotation: 4/4

g8 g8 g8 g8 g4 g8 a2 r2 r8
a8 a8 a8 a8 b4 a8 a8 r4 e4 r2
g8 g8 g8 g8 g4 g8 g8 r8 e8 d8 B2 r8
g8 g8 g4 g4 f#4 g4 r2 r4

d4 d8 d8 e4 e2 r2 r4
e4 e8 e8 e4 g4 b8 a8 e4 r2
d4 d8 d8 e4 e2 r2 r4
e8 e8 e8 e8 e4 g8 g4 a8 b4 r2

g8 g8 g8 g8 g4 g8 a2 r2 r8
a8 a8 a8 a8 b4 a8 a8 r4 e4 r2
g8 g8 g8 g8 g4 g8 g8 r8 e8 d8 B2 r8
g8 g8 g4 g4 f#4 g4 r4 g8 g8 g8 a8

b4 a4 b4 a4 b4 a4 r2
b4 a4 b4 a4 c'4 b4 r2
b4 a4 b4 a4 b4 a4 r2
b4 a4 b4 a4 a4 g4 r2
r8 d'8 b4 r2
r1
"""

chords = converter.parse("""tinynotation: 4/4""")
"""
chords.append(Rest(duration=WHOLE_NOTE))
chds.append(Chd(C_MAJ, duration=WHOLE_NOTE))
chds.append(Chd(G_MAJ, duration=WHOLE_NOTE))
chds.append(Chd(A_MIN, duration=WHOLE_NOTE))
chds.append(Chd(G_MAJ, duration=WHOLE_NOTE))
chds.append(Chd(F_MAJ, duration=WHOLE_NOTE))
chds.append(Chd(E_MIN, duration=WHOLE_NOTE))
chds.append(Chd(F_MAJ, duration=WHOLE_NOTE))
chds.append(Chd(G_MAJ, duration=WHOLE_NOTE))
"""

# Parse command line arguments
parser = argparse.ArgumentParser(description='Find sequence of harmonizing chord progression.')
parser.add_argument('--algorithm', type=str, default='markov', help='algorithm to use: basic or hmm')
parser.add_argument('--melody', type=str, default='halo', help='halo')
parser.add_argument('--series', type=str, default='major', help='major or stank')
args = parser.parse_args()

print('Algorithm: {}, Melody: {}, Series: {}'.format(args.algorithm, args.melody, args.series))

# Pick melody
if args.melody == 'halo':
    melody = converter.parse(HALO_MELODY)
else:
    print('Unrecognized melody: should be halo')
    sys.exit(1)

if args.series not in ('major', 'stank'):
    print('Unrecognized series: should be major or stank')
    sys.exit(1)

melody.insert(0, MetronomeMark(number=95))

# Pick algorithm
if args.algorithm == 'basic':
    chord_search.run(chords, melody, args.series)
elif args.algorithm == 'markov':
    viterbi.run(chords, melody, args.series)
else:
    print('Unrecognized algorithm: should be basic or markov')
    sys.exit(1)

# Combine two parts
song = Stream()
song.insert(0, melody)
song.insert(0, chords)

# song.show('midi')
song.show()
