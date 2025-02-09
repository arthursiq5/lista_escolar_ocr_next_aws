import json
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_textract.type_defs import DetectDocumentTextResponseTypeDef


def detect_file_text() -> None:
    client = boto3.client("textract")

    # pega o path do arquivo
    file_path = str(Path(__file__) / "images" / "lista-material-escolar.jpeg")
    with open(file_path, "rb") as file:
        document_bytes = file.read()
    try:
        # envia arquivo para a IA
        response = client.detect_document_text(Document={"Bytes": document_bytes})
        with open("response.json", "w") as response_file:
            response_file.write(json.dumps(response))
    except ClientError as error:
        print(f"Erro processando documento: {error}")


def get_lines() -> list[str]:
    try:
        with open("response.json", "r") as file:
            data: DetectDocumentTextResponseTypeDef = json.loads(file.read())
            blocks = data["Blocks"]
        return [block["Text"] for block in blocks if block["BlockType"] == "LINE"]  # type: ignore
    except IOError:
        detect_file_text()
    return []


if __name__ == "__main__":
    for line in get_lines():
        print(line)