from aiomisc_dependency import dependency
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import LanceDB
from langchain_core.runnables import Runnable
from langchain.chains import create_retrieval_chain
from lancedb import connect_async
from lancedb.rerankers import LinearCombinationReranker
from pydantic.types import SecretStr

from mcp_search.reader import Reader
from mcp_search.args import Args

def configure_dependecies(args: Args):
    async def read_docs() -> list[Document]:
        splitter = RecursiveCharacterTextSplitter.from_language(
            Language.MARKDOWN,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
        )
        reader = Reader(splitter=splitter)
        return await reader.read(args.docs_path)

    @dependency
    async def vectorstore() -> VectorStore:
        embedding = HuggingFaceEmbeddings(
            model_name=args.embedding_model,
            cache_folder=str(args.cache_folder / "hf"),
        )
        dburi = str(args.cache_folder / "lancedb")
        reranker = LinearCombinationReranker(weight=0.3)
        store = LanceDB(
            uri=dburi,
            embedding=embedding,
            table_name="docs",
            reranker=reranker,
        )
        ldb = await connect_async(dburi)
        try:
            await ldb.open_table("docs")
        except Exception:
            docs = await read_docs()
            await store.aadd_documents(docs)
        return store

    @dependency
    async def chain(vectorstore: VectorStore) -> Runnable:
        openai = args.openai
        system_prompt = (
            "Use only the following pieces of context"
            "to answer the question at the end."
            "If you don't know the answer, just say that you don't know."
            "Don't try to make up an answer."
            "Context: {context}"
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )
        llm=ChatOpenAI(
            model=openai.model,
            base_url=openai.base_url,
            api_key=SecretStr(openai.api_key),
        )
        combine_docs_chain = create_stuff_documents_chain(llm, prompt)
        return create_retrieval_chain(vectorstore.as_retriever(search_kwargs={"k": 10, "fetch_k": 30}), combine_docs_chain)
