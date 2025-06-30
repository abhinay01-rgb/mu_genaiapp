import requests
from langchain.chat_models import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 🛠️ Tavily API tool
def tavily_competitor_review_tool(query: str) -> dict:
    api_key = "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"
    url = "https://api.tavily.com/search"
    response = requests.post(
        url,
        json={"query": query, "search_depth": "advanced"},
        headers={"Authorization": f"Bearer {api_key}"}
    )
    return response.json()

# 🔍 Fetch reviews
query = "Find detailed product reviews for Mamaearth shampoo from blogs"
tavily_results = tavily_competitor_review_tool(query)

# 🔎 Extract top review content
top_results = tavily_results["results"][:5]  # top 5 only
sources = []
for r in top_results:
    sources.append(f"- **Title**: {r['title']}\n  **URL**: {r['url']}\n  **Extract**: {r['content'][:300]}...")

joined_sources = "\n\n".join(sources)

# 🧠 LLM setup
llm = AzureChatOpenAI(
    deployment_name="gpt-4o-2",
    api_version="2024-12-01-preview",
    api_key="ad31085a728c400cb51886b9906951e4",
    azure_endpoint="https://chatgpt-key.openai.azure.com/",
    model_name="gpt-4o",
    temperature=0.6,
    max_tokens=800
)

# 📄 Prompt
template = PromptTemplate.from_template("""
You are a product review analyst. Based on the extracted data below, write a structured and neutral summary of Mamaearth Onion Shampoo, including:

1. General Overview
2. Key Strengths
3. Potential Weaknesses
4. Conclusion

Avoid quoting user reviews directly. Focus on summarizing the overall opinion of blogs and review platforms.
Please mention the url as well 
Extracted content:
{source_text}
""")

# 🧠 Generate summary
chain = template | llm | StrOutputParser()
final_summary = chain.invoke({"source_text": joined_sources})

# ✅ Output
print("\n🧠 Summarized Review:\n")
print(final_summary)
