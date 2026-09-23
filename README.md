# filepacker

ディレクトリを再帰的に走査し、ディレクトリ構造とファイルの内容を1つのJSONファイルにまとめるPythonツールです。

作成したJSONファイルから、元のディレクトリ構造とファイルを復元することもできます。

## 特徴

- ディレクトリを再帰的に走査
- ディレクトリ構造をJSONとして保存
- ファイルの内容をJSONとして保存
- JSONからディレクトリとファイルを復元
- Python標準ライブラリのみで動作
- UTF-8で読み書き
- 隠しファイル・隠しディレクトリを自動的に除外
- 非UTF-8ファイルは警告を表示してスキップ

## 必要環境

- Python 3.9以上
- 外部ライブラリ不要

## ディレクトリ構成

    filepacker/
    ├── README.md
    ├── packed.json
    ├── apps/
    │   ├── packer/
    │   │   └── __main__.py
    │   └── unpacker/
    │       └── __main__.py
    └── demo/
        ├── command.txt
        ├── 1_original/
        │   ├── a.txt
        │   └── b/
        │       └── b.json
        ├── 2_packed/
        │   └── packed.json
        └── 3_unpacked/
            ├── a.txt
            └── b/
                └── b.json

## 使い方

### Pack

ディレクトリを再帰的に走査し、すべての対象ファイルを1つのJSONファイルにまとめます。

    python3 ./apps/packer ./project archive.json

例えば、次のようなディレクトリがあるとします。

    project/
    ├── a.txt
    └── b/
        └── b.json

以下を実行します。

    python3 ./apps/packer ./project archive.json

すると、`archive.json` が作成されます。

### Unpack

Packで作成したJSONファイルから、ディレクトリ構造とファイルを復元します。

    python3 ./apps/unpacker ./archive.json ./restored

`./restored` が存在しない場合は自動的に作成されます。

## デモ

`demo/` ディレクトリには、PackとUnpackの実行例が用意されています。

    demo/
    ├── 1_original/     # Packする前のファイル
    ├── 2_packed/       # Pack後のJSON
    └── 3_unpacked/     # Unpackによって復元されたファイル

プロジェクトのルートディレクトリから、以下を実行できます。

    python3 ./apps/packer ./demo/1_original ./demo/2_packed/packed.json

    python3 ./apps/unpacker ./demo/2_packed/packed.json ./demo/3_unpacked

Pack前とUnpack後を比較すると、ファイルの内容とディレクトリ構造が復元されていることを確認できます。

## JSON形式

Packによって生成されるJSONは、以下の2つの情報を持ちます。

- `directories`: ディレクトリ構造と各ディレクトリに含まれるファイル名
- `files`: 各ファイルのパス、ファイル名、内容

例えば、次のようなファイル構成をPackしたとします。

    project/
    ├── general.txt
    └── details/
        └── detail.txt

生成されるJSONは次のような形式になります。

    {
        "directories": {
            "./": {
                "files": [
                    "general.txt"
                ],
                "details/": {
                    "files": [
                        "detail.txt"
                    ]
                }
            }
        },
        "files": [
            {
                "path": "./",
                "name": "general.txt",
                "body": "Hello\nDo you hear me?"
            },
            {
                "path": "./details",
                "name": "detail.txt",
                "body": "Hello..."
            }
        ]
    }

### `directories`

ディレクトリ構造を表します。

    {
        "./": {
            "files": [
                "general.txt"
            ],
            "details/": {
                "files": [
                    "detail.txt"
                ]
            }
        }
    }

各ディレクトリはキーとして表現され、その中の `files` にファイル名が格納されます。

サブディレクトリはさらにネストして表現されます。

### `files`

各ファイルの情報を配列として保存します。

    {
        "path": "./details",
        "name": "detail.txt",
        "body": "Hello..."
    }

各フィールドの意味は次のとおりです。

| フィールド | 説明 |
|---|---|
| `path` | ファイルが含まれるディレクトリ |
| `name` | ファイル名 |
| `body` | ファイルの内容 |

`body` はUTF-8のテキストとして保存されます。

## 対象ファイル

現在の実装では、ファイルをUTF-8テキストとして読み込みます。

そのため、バイナリファイルやUTF-8として読み込めないファイルはPackの対象外です。

非UTF-8ファイルが見つかった場合は、次のような警告を表示してスキップします。

    Warning: skipped non-UTF-8 file: example.bin

## 隠しファイル・隠しディレクトリ

名前が `.` で始まるファイルおよびディレクトリはPack時に除外されます。

例えば、

    project/
    ├── a.txt
    ├── .gitignore
    └── .git/

の場合、`a.txt` はPackされますが、`.gitignore` と `.git/` はPackされません。

## 注意事項

### テキストファイルを対象としています

ファイルの内容を文字列としてJSONに保存するため、画像・音声・動画・PDFなどのバイナリファイルをそのままPackする用途には対応していません。

### ファイルのパーミッションなどは保存されません

現在保存されるのは主に以下の情報です。

- ディレクトリ構造
- ファイル名
- ファイル内容

ファイルのパーミッション、所有者、更新日時などのメタデータは保存されません。

### Unpack先の既存ファイル

Unpack時、同じ名前のファイルがすでに存在する場合は、そのファイルを上書きします。

## コマンドリファレンス

### Pack

    python3 ./apps/packer <directory> <output>

| 引数 | 説明 |
|---|---|
| `<directory>` | Packするディレクトリ |
| `<output>` | 出力するJSONファイル |

例:

    python3 ./apps/packer ./project ./archive.json

### Unpack

    python3 ./apps/unpacker <input> <directory>

| 引数 | 説明 |
|---|---|
| `<input>` | Pack済みJSONファイル |
| `<directory>` | 復元先ディレクトリ |

例:

    python3 ./apps/unpacker ./archive.json ./restored

## ライセンス

Copyright (c) 2026 Usui Ryuichiro

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
