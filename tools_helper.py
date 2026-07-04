class ToolsBase:
    def __init__(
        self,
        index
    ):
        self.index = index

    def search(self, query: str, num_results: int=5):
        """
        Search the course knowledge base for entries matching the given query.
        """
        return self.index.search(
            query=query,
            num_results=num_results
        )