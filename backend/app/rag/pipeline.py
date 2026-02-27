
import asyncio
import logging
from typing import Optional, List
from app.rag.retriever import retrieve_docs
from app.llm.loader import LLMManager
from app.rag.citation_builder import build_citations

logger = logging.getLogger(__name__)

async def run_rag(question, selected_files: Optional[List[str]] = None):
    try:
        logger.info(f"Running RAG for question: {question}")
        if selected_files:
            logger.info(f"Filtering by selected files: {selected_files}")
        docs = retrieve_docs(question)
        logger.info(f"Retrieved {len(docs) if docs else 0} documents")
        
        context = "\n".join([d.page_content for d in docs]) if docs else "No relevant documents found."

        prompt = f"""Use the context below to answer the question. If you cannot find the answer in the context, say so.

Context:
{context}

Question: {question}

Answer:"""

        # Run LLM invocation in thread pool with timeout
        loop = asyncio.get_event_loop()
        llm = LLMManager().get_llm()
        
        try:
            # Run the blocking LLM call in a thread pool with 30 second timeout
            answer = await asyncio.wait_for(
                loop.run_in_executor(None, llm.invoke, prompt),
                timeout=30.0
            )
            logger.info("LLM invocation successful")
        except asyncio.TimeoutError:
            logger.error("LLM invocation timed out after 30 seconds")
            answer = "The AI service is taking too long to respond. Please ensure Ollama is running and responsive."
        except Exception as e:
            logger.error(f"LLM invocation error: {str(e)}")
            answer = f"Failed to get AI response. Error: {str(e)}"

        return {
            "answer": str(answer),
            "citations": build_citations(docs) if docs else [],
            "success": True
        }
    except Exception as e:
        logger.error(f"RAG pipeline error: {str(e)}", exc_info=True)
        return {
            "answer": f"Error processing question: {str(e)}",
            "citations": [],
            "success": False
        }
