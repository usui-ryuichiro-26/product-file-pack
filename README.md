# filepacker

ディレクトリを再帰的に走査し、すべてのファイルを1つのJSONファイルにまとめるPythonツールです。
作成したJSONファイルから、ディレクトリ構造とファイルを復元することもできます。

## 使い方

### Pack

ディレクトリを再帰的に走査して、1つのJSONファイルにまとめます。

    python apps/packer ./project archive.json

### Unpack

JSONファイルからディレクトリ構造とファイルを復元します。

    python apps/unpacker.py archive.json ./restored

## JSON形式

生成されるJSONファイルは次の形式です。

    {
        "files": [
            {
                "path": "./",
                "name": "general.txt",
                "body": "Hello\nDo you here me?"
            },
            {
                "path": "./details/",
                "name": "detail.txt",
                "body": "Hello..."
            }
        ]
    }

- `path`: ファイルが含まれるディレクトリ
- `name`: ファイル名
- `body`: ファイルの内容

ディレクトリは再帰的に走査されます。

## 必要環境

- Python 3.9以上
- 外部ライブラリ不要
