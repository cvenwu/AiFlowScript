import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "tokenizer.py"
SPEC = importlib.util.spec_from_file_location("tokenizer", MODULE_PATH)
tokenizer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(tokenizer)

SimpleCharTokenizer = tokenizer.SimpleCharTokenizer


class SimpleCharTokenizerTest(unittest.TestCase):
    def test_builds_vocabulary_with_unknown_token_first(self):
        tok = SimpleCharTokenizer.from_text("aba")

        self.assertEqual(tok.token_to_id["<UNK>"], 0)
        self.assertEqual(tok.token_to_id, {"<UNK>": 0, "a": 1, "b": 2})
        self.assertEqual(tok.id_to_token, {0: "<UNK>", 1: "a", 2: "b"})

    def test_encodes_known_characters(self):
        tok = SimpleCharTokenizer.from_text("hello")

        self.assertEqual(tok.encode("hello"), [1, 2, 3, 3, 4])

    def test_decodes_known_token_ids(self):
        tok = SimpleCharTokenizer.from_text("hello")

        self.assertEqual(tok.decode([1, 2, 3, 3, 4]), "hello")

    def test_unknown_characters_and_ids_use_unknown_token(self):
        tok = SimpleCharTokenizer.from_text("ab")

        self.assertEqual(tok.encode("abc"), [1, 2, 0])
        self.assertEqual(tok.decode([1, 99, 2]), "a<UNK>b")

    def test_empty_text_round_trip(self):
        tok = SimpleCharTokenizer.from_text("")

        self.assertEqual(tok.token_to_id, {"<UNK>": 0})
        self.assertEqual(tok.id_to_token, {0: "<UNK>"})
        self.assertEqual(tok.encode(""), [])
        self.assertEqual(tok.decode([]), "")


if __name__ == "__main__":
    unittest.main()
