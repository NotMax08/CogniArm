import LLM_Fetcher as llm

llm_fetcher = llm.LLMFetcher()
prompt = "what is 2 + 2? respond in 1 single integer"
response = llm_fetcher.fetch_response(prompt)
print("LLM Response:", response)