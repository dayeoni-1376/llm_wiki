import re
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

import streamlit as st
from langchain_ollama import ChatOllama

MODEL_NAME = "gemma4:e4b"
OBSIDIAN_DIR = Path(__file__).resolve().parent.parent
WIKI_DIR = OBSIDIAN_DIR / "AI Wiki"
INDEX_FILE = WIKI_DIR / "index.md"
VAULT_NAME = OBSIDIAN_DIR.name

ANSWER_PROMPT = """
당신은 로컬 옵시디언 위키를 바탕으로 질문에 답하는 비서입니다.
다음 컨텍스트만 사용해서 질문에 간단하고 정확하게 답하세요.
답변은 한국어로 하고, 관련 문서 이름을 함께 적어주세요.
컨텍스트가 부족하면 그 사실을 명확히 말하세요.

컨텍스트:
{context}

질문:
{question}

답변:
"""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def build_wiki_path(path: Path) -> str:
    return str(path.relative_to(WIKI_DIR).with_suffix("")).replace("\\", "/")


def build_obsidian_uri(file_path: Path) -> str:
    vault_name = quote(VAULT_NAME)
    vault_relative_path = quote(str(file_path.relative_to(OBSIDIAN_DIR)).replace("\\", "/"))
    return f"obsidian://open?vault={vault_name}&file={vault_relative_path}"


def build_markdown_link(label: str, file_path: Path) -> str:
    return f"[{label}]({build_obsidian_uri(file_path)})"


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


@lru_cache(maxsize=1)
def load_wiki_documents() -> list[tuple[str, str]]:
    docs: list[tuple[str, str]] = []
    for path in sorted(WIKI_DIR.rglob("*.md")):
        rel_path = "index" if path == INDEX_FILE else build_wiki_path(path)
        docs.append((rel_path, read_text(path)))
    return docs


def find_relevant_documents(question: str, top_k: int = 4) -> list[tuple[str, str]]:
    docs = load_wiki_documents()
    question_terms = set(re.findall(r"[가-힣a-zA-Z0-9]+", question.lower()))
    if not question_terms:
        return docs[:top_k]

    scored_docs: list[tuple[int, str, str]] = []
    for rel_path, content in docs:
        document_text = f"{rel_path} {content}".lower()
        document_terms = set(re.findall(r"[가-힣a-zA-Z0-9]+", document_text))
        overlap = len(question_terms & document_terms)
        scored_docs.append((overlap, rel_path, content))

    scored_docs.sort(key=lambda item: item[0], reverse=True)
    return [(rel_path, content) for _, rel_path, content in scored_docs[:top_k]]


def build_context(question: str) -> str:
    sections: list[str] = []
    for rel_path, content in find_relevant_documents(question):
        snippet = normalize_text(content)
        if len(snippet) > 2200:
            snippet = snippet[:2200] + "..."
        sections.append(f"[{rel_path}]\n{snippet}")
    return "\n\n".join(sections)


def answer_question(question: str) -> str:
    context = build_context(question)
    prompt = ANSWER_PROMPT.format(context=context, question=question)
    response = model.invoke(prompt)
    return response.content.strip()


model = ChatOllama(model=MODEL_NAME, temperature=0)

st.title("LLM Wiki Agent")
st.caption("옵시디언 지식베이스에 쿼리하기")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "질문하세요?"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

question = st.chat_input("당신의 wiki에게 질문하세요")

if question:
    st.session_state["messages"].append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.spinner("답변 생성 중..."):
        answer = answer_question(question)

    st.session_state["messages"].append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
