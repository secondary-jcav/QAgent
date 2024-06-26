from llama_index.core import (
    Document,
    SimpleDirectoryReader,
    VectorStoreIndex,
)
from base.base_class import BaseClass

prompt = f"In test_report you'll find one or more failing tests" \
         f"First, identify what elements are involved in the assertion error that makes the test fail" \
         f"Then look at git_changes and identify which changes dealt with those elements" \
         f"Report back with: the commit id of those changes and why you think they broke the tests"


class ReportChecker(BaseClass):
    def __init__(self):
        super().__init__()

    @staticmethod
    def build_document(content) -> Document:
        return Document(text=content)

    @staticmethod
    def read_documents(path) -> list[Document]:
        return SimpleDirectoryReader(path).load_data()

    def test_result_analysis(self, report, commits) -> str:
        changes = self.build_document(commits)
        changes.metadata = {"filename": "git_changes"}
        report = self.build_document(report)
        report.metadata = {"filename": "test_report"}
        print("Looking for breaking changes")
        index = VectorStoreIndex.from_documents([changes, report])
        query_engine = index.as_query_engine()
        response = query_engine.query(prompt)
        return str(response)
