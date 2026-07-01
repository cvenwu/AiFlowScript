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
