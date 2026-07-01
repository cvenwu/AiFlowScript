# Python Tokenizer Demo Design

## Goal

Create a small beginner-friendly Python tokenizer demo under a parent demo directory. The project should show the full round trip:

- accept an input string
- build a vocabulary from that input
- encode the string into token IDs
- decode the token IDs back into text

The demo must avoid third-party dependencies and stay readable for Python beginners.

## Directory

```text
project-demos/
└── python-tokenizer/
    ├── README.md
    ├── tokenizer.py
    └── tests/
        └── test_tokenizer.py
```

`project-demos/` is the parent folder for demo projects. `python-tokenizer/` is the concrete tokenizer demo.

## Approach

Use a character-level tokenizer. Each distinct character receives one integer ID. ID `0` is reserved for `<UNK>`, which represents unknown characters during encoding.

This approach is recommended because it is simple, deterministic, and easy to explain without external libraries. Word-level tokenization would require more edge-case handling around punctuation, whitespace, and mixed-language input.

## Components

`tokenizer.py` contains:

- `SimpleCharTokenizer`: stores `token_to_id` and `id_to_token`
- `from_text(text)`: builds a tokenizer from input text
- `encode(text)`: converts text to integer IDs
- `decode(ids)`: converts integer IDs back to text
- `main()`: command-line entry point that prints input text, vocabulary, encoded IDs, and decoded text

`tests/test_tokenizer.py` covers:

- vocabulary construction
- encode output for known characters
- decode output for known token IDs
- unknown character handling
- empty text handling

`README.md` explains:

- what tokenization means
- how this beginner demo works
- how to run the script
- how to run the tests

## Data Flow

```text
input text
  -> SimpleCharTokenizer.from_text(input text)
  -> encode(input text)
  -> encoded token ID list
  -> decode(encoded token ID list)
  -> restored text
```

## Error Handling

- Encoding unknown characters returns ID `0`.
- Decoding unknown IDs returns `<UNK>`.
- Empty input builds a vocabulary with only `<UNK>` and round-trips to an empty list/string.
- The CLI uses a default sample input when no argument is provided.

## Testing

Use Python standard-library `unittest` so the demo does not need dependencies. Tests can run with:

```bash
python -m unittest discover -s project-demos/python-tokenizer/tests
```

## Out Of Scope

- Byte Pair Encoding
- model-compatible tokenization
- Chinese word segmentation
- external NLP libraries
- package publishing
