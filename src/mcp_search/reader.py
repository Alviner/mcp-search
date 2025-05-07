from pathlib import Path
import glob
from dataclasses import dataclass
import logging

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import TextSplitter

log = logging.getLogger(__name__)


@dataclass
class Reader:
    splitter: TextSplitter

    async def read(self, folder: Path) -> list[Document]:
        md_files = glob.glob(str(folder / "**/*.md"), recursive=True)
        alldocs = []
        for file in md_files:
            file = Path(file)
            relative_file = file.relative_to(folder)
            log.info("reading file: %s", relative_file)
            loader = TextLoader(file)
            docs = await loader.aload()
            for doc in docs:
                doc.metadata["source"] = str(relative_file)
            alldocs.extend(docs)

        return self.splitter.split_documents(alldocs)
