from gitsource import GithubRepositoryDataReader, chunk_documents
from minsearch import Index

def load_documents_from_github() -> list[dict[str, any]]:
    reader = GithubRepositoryDataReader(
        repo_owner="DataTalksClub",
        repo_name="llm-zoomcamp",
        commit_id="8c1834d",
        allowed_extensions={"md"},
        filename_filter=lambda path: "/lessons/" in path,
    )

    files = reader.read()

    documents: list[dict[str, any]] = []

    for file in files:
        documents.append(file.parse())

    return documents

def chunk_loaded_documents(documents: list[dict[str, any]]) -> list[dict[str, any]]:
    return chunk_documents(documents)

def build_index(documents: list[dict[str, any]]) -> Index:
    index = Index(
        text_fields=["content"],
        keyword_fields=["filename"]
    )

    index.fit(documents)

    return index