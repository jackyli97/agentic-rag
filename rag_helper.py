INSTRUCTIONS = """
You're a course teaching assistant.
You're given a question from a course student and your task is to answer it.

If you want to look up information, use the search function. 
Use as many keywords from the user question as possible when making first requests.

Make multiple searches. First perform search, analyze the results 
and then perform more searches if need be. 

The question has to be about the course's technical contents or its logistics, offtopic questions 
shouldn't be answered. If the search returns nothing, it's likely an off-topic question.
If you can't answer the question using FAQ, don't do it yourself. Only use the 
facts from the FAQ database.

At the end, ask if there are other areas that the user wants to explore.
"""

PROMPT_TEMPLATE = """
Question:
{question}

Context:
{context}
"""

class RAGBase:
    def __init__(
        self,
        index,
        llm_client,
        instructions=INSTRUCTIONS,
        prompt_template=PROMPT_TEMPLATE,
        model="gpt-5.4-mini",
        num_results_for_search=5,
    ):
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions.strip()
        self.prompt_template = prompt_template.strip()
        self.model = model
        self.num_results_for_search = num_results_for_search

    def search(self, question):
        return self.index.search(
            question,
            num_results=self.num_results_for_search
        )

    def build_context(self, search_results):
        lines = []

        for doc in search_results:
            lines.append(doc["content"])
            lines.append("filename: " + doc["filename"])
            lines.append("")

        return "\n".join(lines).strip()


    def build_prompt(self,question, search_results):
        context = self.build_context(search_results)
        prompt = self.prompt_template.format(
            question=question,
            context=context
        )
        return prompt.strip()


    def llm(self, user_prompt):
        message_history = [
            {"role": "developer", "content": self.instructions},
            {"role": "user", "content": user_prompt}
        ]

        response = self.llm_client.responses.create(
            model=self.model,
            input=message_history
        )

        return response

    def rag(self, question):
        search_results = self.search(question)
        user_prompt = self.build_prompt(question, search_results)

        answer = self.llm(user_prompt)

        return answer