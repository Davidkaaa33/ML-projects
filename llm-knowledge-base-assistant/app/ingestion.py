from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "sample_docs"


@dataclass
class Document:
    text: str
    source: str


def load_txt(path: Path) -> Document:
    text = path.read_text(encoding="utf-8")

    return Document(
        text=text,
        source=path.name,
    )


def load_pdf(path: Path) -> Document:
    reader = PdfReader(path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return Document(
        text="\n".join(pages),
        source=path.name,
    )


def load_document(path: Path) -> Document:
    suffix = path.suffix.lower()

    if suffix == ".txt":
        return load_txt(path)

    if suffix == ".pdf":
        return load_pdf(path)

    raise ValueError(f"Unsupported file type: {suffix}")


def load_documents(directory: Path) -> list[Document]:
    documents = []

    for path in directory.iterdir():
        if path.suffix.lower() not in {".txt", ".pdf"}:
            continue

        documents.append(load_document(path))

    return documents


if __name__ == "__main__":
    documents = load_documents(DATA_DIR)

    print(f"Loaded documents: {len(documents)}")

    for document in documents:
        print("\n" + "=" * 60)
        print(f"Source: {document.source}")
        print("=" * 60)
        print(document.text)
