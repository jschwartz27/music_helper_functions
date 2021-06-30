import os
from typing import Dict, List, Tuple
from music21 import stream, tempo, note, key, pitch, meter, clef, chord


time_signature_type = Tuple[int, int]  # e.g. (4, 4) - common time
note = Tuple(int, List[int])
chromosome = List[note]
# voices_type = Dict[str: List]
# example_music = {
#        "voice1": [(4, [60]), (4, [62]), (4, [63])],
#        "voice2": [(4, [55]), (4, [56]), (4, [51])]
# }


class MusikFile:

    tempo = 80

    def __init__(
        self, voices: Dict[str, chromosome],
        key_signature: str,
        time_signature: time_signature_type,
        filename: str,
        save: bool,
        open_music: bool
    ):
        self.voices = voices
        self.key_signature = key_signature
        self.time_signature = f"{time_signature[0]}/{time_signature[1]}"
        self.save = save
        self.filename = filename
        self.open_music_file = open_music
        self.create_flow()
    
    def create_flow(self):
        flow = stream.Score()
        flow.append(tempo.MetronomeMark(number=self.tempo))
        for voice in self.voices:
            notes = list()
            for i in self.voices[voice]:
                if i[1][0] == 0:
                    r = note.Rest()
                    r.duration.quarterLength = i[0]
                    notes.append(r)
                elif len(i[1]) == 1:
                    k = pitch.simplifyMultipleEnharmonics(
                        i[1], keyContext=key.Key(self.key_signature)
                    )
                    for j in k:
                        notes.append(note.Note(j, quarterLength=i[0]))
                else:
                    k = pitch.simplifyMultipleEnharmonics(
                        i[1], keyContext=key.Key(self.key_signature)
                    )
                    notes.append(chord.Chord(k, quarterLength=i[0]))

            part = stream.Part()
            part.insert(meter.TimeSignature(self.time_signature))
            if "3" in voice:
                part.insert(0, clef.AltoClef())

            part.keySignature = key.Key(self.key_signature)
            part.append([note for note in notes])
            flow.insert(0, part)

        if self.save:
            try:
                if not os.path.exists("MIDI"):
                    os.mkdir("MIDI")
                flow.write('midi', fp= f"MIDI/{self.filename}.mid")
                print("\tSAVED!")
            except:
                print("FAILED SAVING")  # TODO create better exception

        if self.open_music_file:
            flow.show("musicxml")


def main():
    example_music = {
        "voice1": [(4, [60]), (4, [62]), (4, [63])],
        "voice2": [(4, [55]), (4, [56]), (4, [51])]
    }

    musik = MusikFile(example_music, "c", (4, 4), "test_file", True, False)


if __name__ == "__main__":
    main()
