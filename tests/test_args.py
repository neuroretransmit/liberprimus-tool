import unittest

from args import get_transcription_validations

# TO GET EXPECTED VALUES, THE FOLLOWING SHELL COMMAND WAS USED (replace the '-' for delims)
# echo $(cat data/transcription.txt | wc -c) - $(cat data/transcription.txt  | tr -d '-' | wc -c) | bc

EXPECTED_SECTION_COUNTS = {
    "words": 3644,
    "clauses": 262,
    "paragraphs": 33,
    "segments": 18,
    "lines": 797,
    "pages": 73
}

class TestArgs(unittest.TestCase):
    def test_get_transcription_validations(self):
        validations = get_transcription_validations()
        for k, v in EXPECTED_SECTION_COUNTS.items():
            self.assertEqual(validations[k]["num"], v)

if __name__ == '__main__':
    unittest.main()
