from collections import namedtuple

import music21
from music21.chord import Chord
from music21.note import Note
from music21.duration import Duration
from music21.interval import notesToChromatic

# Cannot use name 'Chord', already taken
HarmonyChord = namedtuple('HarmonyChord', ['name', 'notes'])

WHOLE_NOTE = Duration(4.0)

# How bad a interval sounds (given number of semitones)
CHROMATIC_PENALTY = {
  0: 0,
  1: 3,
  2: 1,
  3: 1,
  4: 1,
  5: 0,
  6: 0,
}

C_MAJ = HarmonyChord(name='C', notes=['c3', 'e3', 'g3', 'c4'])
G_MAJ = HarmonyChord(name='G', notes=["g2", "b2", "d3", "g3"])
A_MIN = HarmonyChord(name='Am', notes=["a2", "c3", "e3", "a3"])
B_MIN = HarmonyChord(name='Bm', notes=["b2", "d3", "f#3", "b3"])
D_MAJ = HarmonyChord(name='D', notes=["d3", "f#3", "a3", "d4"])
E_MIN = HarmonyChord(name='Em', notes=["e3", "g3", "b3", "e4"])
F_MAJ = HarmonyChord(name='F', notes=["f2", "a2", "c3", "f3"])
F_SHARP_MIN = HarmonyChord(name='F#m', notes=["f#2", "a2", "c#3", "f#3"])

C_MAJ7_9 = HarmonyChord(name='Cmaj7/9', notes=['c3', 'e3', 'b3', 'd4'])
D_7_9    = HarmonyChord(name='D7/9', notes=["d3", "f#3", "c4", "e4"])
E_SUS2   = HarmonyChord(name='Esus2', notes=["e3", "f#3", "b3", "e4"])
E_SUS4   = HarmonyChord(name='Esus4', notes=["e3", "a3", "b3", "e4"])
B_MIN7   = HarmonyChord(name='Bm7', notes=["d3", "a3", "b3", "d4"])
F_SHARP_MIN_7 = HarmonyChord(name='F#m7', notes=["e2", "f#2", "a3", "e3"])

ALL_CHORDS = [
  C_MAJ, G_MAJ, A_MIN, B_MIN, D_MAJ, E_MIN,
]

STANK_CHORDS = [
  D_MAJ,
  C_MAJ7_9, D_7_9, E_SUS2, B_MIN7, F_SHARP_MIN_7
]

def chord_search(notes, candidates):
  """Attempt to find the best chord to match a set of notes"""
  best_chord, best_score = C_MAJ, 1000

  for chord in candidates:
    chord_score = 0
    for note1 in chord.notes:
      note1 = Note(note1)
      for note2 in notes:
        chromatic_distance = notesToChromatic(note1, note2).semitones

        # Normalize distance to be between 0 and 6
        chromatic_distance = chromatic_distance % 12
        if chromatic_distance > 6:
          chromatic_distance = 12 - chromatic_distance

        chord_score += CHROMATIC_PENALTY[chromatic_distance]

    if chord_score < best_score:
      best_score = chord_score
      best_chord = chord

  print(best_chord.name)
  return best_chord


def run(chords, melody, series):
  if series == 'major':
      candidates = ALL_CHORDS
  if series == 'stank':
      candidates = STANK_CHORDS 
  # Insert a chord for each measure
  for measure in filter(lambda x: isinstance(x, music21.stream.Measure), melody.elements):
    measure_notes = []
    for note in filter(lambda x: isinstance(x, music21.note.Note), measure.elements):
      measure_notes.append(note)
    chords.append(Chord(chord_search(measure_notes, candidates).notes, duration=WHOLE_NOTE))
