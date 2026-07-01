# Python Tokenizer Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a beginner-friendly Python character tokenizer demo under `project-demos/python-tokenizer/`.

**Architecture:** The demo is a single-file tokenizer with a small command-line interface. It uses a `SimpleCharTokenizer` class to build a vocabulary, encode text into integer token IDs, and decode token IDs back into text. Tests use Python standard-library `unittest` so the project has no dependency setup.

**Tech Stack:** Python standard library, `unittest`, command-line execution with `python`.

## Global Constraints

- Create the project under `project-demos/python-tokenizer/`.
- Avoid third-party dependencies.
- Use character-level tokenization.
- Reserve ID `0` for `<UNK>`.
- Encoding unknown characters returns ID `0`.
- Decoding unknown IDs returns `<UNK>`.
- Empty input builds a vocabulary with only `<UNK>` and round-trips to an empty list/string.
- The CLI uses a default sample input when no argument is provided.

---

## File Structure

- Create `project-demos/python-tokenizer/tokenizer.py`: `SimpleCharTokenizer` implementation and CLI entry point.
- Create `project-demos/python-tokenizer/tests/test_tokenizer.py`: standard-library `unittest` tests for vocabulary, encode, decode, unknown handling, and empty text.
- Create `project-demos/python-tokenizer/README.md`: beginner explanation, run commands, and test commands.

### Task 1: Character Tokenizer Demo

**Files:**
- Create: `project-demos/python-tokenizer/tokenizer.py`
- Create: `project-demos/python-tokenizer/tests/test_tokenizer.py`
- Create: `project-demos/python-tokenizer/README.md`

**Interfaces:**
- Consumes: no earlier project code
- Produces:
  - `SimpleCharTokenizer.from_text(text: str) -> SimpleCharTokenizer`
  - `SimpleCharTokenizer.encode(text: str) -> list[int]`
  - `SimpleCharTokenizer.decode(token_ids: list[int]) -> str`
  - command: `python project-demos/python-tokenizer/tokenizer.py "hello tokenizer"`

- [ ] **Step 1: Write the failing test**

Create `project-demos/python-tokenizer/tests/test_tokenizer.py` with:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python -m unittest discover -s project-demos/python-tokenizer/tests
```

Expected: FAIL or ERROR because `project-demos/python-tokenizer/tokenizer.py` does not exist yet.

- [ ] **Step 3: Write minimal implementation**

Create `project-demos/python-tokenizer/tokenizer.py` with:

```python
import sys


UNKNOWN_TOKEN = "<UNK>"
UNKNOWN_ID = 0


class SimpleCharTokenizer:
    def __init__(self, token_to_id):
        self.token_to_id = token_to_id
        self.id_to_token = {token_id: token for token, token_id in token_to_id.items()}

    @classmethod
    def from_text(cls, text):
        token_to_id = {UNKNOWN_TOKEN: UNKNOWN_ID}
        for char in text:
            if char not in token_to_id:
                token_to_id[char] = len(token_to_id)
        return cls(token_to_id)

    def encode(self, text):
        return [self.token_to_id.get(char, UNKNOWN_ID) for char in text]

    def decode(self, token_ids):
        return "".join(self.id_to_token.get(token_id, UNKNOWN_TOKEN) for token_id in token_ids)


def main():
    text = "hello tokenizer" if len(sys.argv) == 1 else " ".join(sys.argv[1:])
    tokenizer = SimpleCharTokenizer.from_text(text)
    encoded = tokenizer.encode(text)
    decoded = tokenizer.decode(encoded)

    print(f"输入文本: {text}")
    print(f"词表: {tokenizer.token_to_id}")
    print(f"编码结果: {encoded}")
    print(f"解码结果: {decoded}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run:

```bash
python -m unittest discover -s project-demos/python-tokenizer/tests
```

Expected: all 5 tests pass.

- [ ] **Step 5: Add README**

Create `project-demos/python-tokenizer/README.md` with:

```markdown
# Python Tokenizer Demo

这是一个 Python 入门版 tokenizer 分词器 Demo。它不依赖第三方库，用最简单的字符级分词展示 tokenizer 的核心思想：

1. 把文本拆成 token。
2. 给每个 token 分配一个整数 ID。
3. 把文本编码成 ID 列表。
4. 再把 ID 列表解码回文本。

## 为什么用字符级分词

字符级分词适合入门理解。它不用处理复杂的英文单词、标点、中文分词或模型词表规则，每个不同字符就是一个 token。

这个 Demo 里，`<UNK>` 表示未知 token，固定使用 ID `0`。

## 运行

在仓库根目录执行：

```bash
python project-demos/python-tokenizer/tokenizer.py "hello tokenizer"
```

也可以不传参数，脚本会使用默认输入：

```bash
python project-demos/python-tokenizer/tokenizer.py
```

输出示例：

```text
输入文本: hello tokenizer
词表: {'<UNK>': 0, 'h': 1, 'e': 2, 'l': 3, 'o': 4, ' ': 5, 't': 6, 'k': 7, 'n': 8, 'i': 9, 'z': 10, 'r': 11}
编码结果: [1, 2, 3, 3, 4, 5, 6, 4, 7, 2, 8, 9, 10, 2, 11]
解码结果: hello tokenizer
```

## 运行测试

```bash
python -m unittest discover -s project-demos/python-tokenizer/tests
```

## 核心代码

`SimpleCharTokenizer.from_text(text)` 会根据输入文本构建词表。

`encode(text)` 会把文本转成整数 ID 列表。

`decode(token_ids)` 会把整数 ID 列表还原成文本。
```

- [ ] **Step 6: Run CLI manually**

Run:

```bash
python project-demos/python-tokenizer/tokenizer.py "hello tokenizer"
```

Expected output includes:

```text
输入文本: hello tokenizer
编码结果: [1, 2, 3, 3, 4, 5, 6, 4, 7, 2, 8, 9, 10, 2, 11]
解码结果: hello tokenizer
```

- [ ] **Step 7: Run full verification**

Run:

```bash
python -m unittest discover -s project-demos/python-tokenizer/tests
python project-demos/python-tokenizer/tokenizer.py "AI Agent"
git status --short
```

Expected:

```text
.....
----------------------------------------------------------------------
Ran 5 tests in ...

OK
输入文本: AI Agent
...
解码结果: AI Agent
```

`git status --short` should show the new `project-demos/python-tokenizer/` files, plus any pre-existing unrelated files.

- [ ] **Step 8: Commit**

Run:

```bash
git add project-demos/python-tokenizer
git commit -m "feat: add python tokenizer demo"
```

Expected: one commit containing `README.md`, `tokenizer.py`, and `tests/test_tokenizer.py`.

## Self-Review

- Spec coverage: The plan creates the parent demo folder, tokenizer implementation, tests, README, CLI output, unknown handling, and empty text behavior.
- Placeholder scan: No placeholders, no deferred edge cases, no undefined functions.
- Type consistency: The plan consistently uses `SimpleCharTokenizer.from_text(text)`, `encode(text)`, and `decode(token_ids)`.
