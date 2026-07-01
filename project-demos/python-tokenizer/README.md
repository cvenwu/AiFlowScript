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
