
def build_citations(docs):
    citations = []
    for d in docs:
        citations.append({
            "source": d.metadata.get("source"),
            "snippet": d.page_content[:200]
        })
    return citations
