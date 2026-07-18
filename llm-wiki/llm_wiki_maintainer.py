import re
from pathlib import Path
from urllib.parse import quote

import streamlit as st
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

MODEL_NAME = "gemma4:e4b"
OBSIDIAN_DIR = Path(__file__).resolve().parent.parent
WIKI_DIR = OBSIDIAN_DIR / "AI Wiki"
INDEX_FILE = WIKI_DIR / "index.md"
VAULT_NAME = OBSIDIAN_DIR.name

AGENT_PROMPT = """
You answer questions from a local Obsidian wiki.

You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought:
{agent_scratchpad}
"""

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def build_wiki_path(path: Path) -> str:
    return str(path.relative_to(WIKI_DIR).with_suffix("")).replace("\\", "/")


def build_wiki_link(wiki_path: str) -> str:
    return f"[[{wiki_path}]]"


def build_obsidian_uri(file_path: Path) -> str:
    vault_name = quote(VAULT_NAME)
    vault_relative_path = quote(str(file_path.relative_to(OBSIDIAN_DIR)).replace("\\", "/"))
    return f"obsidian://open?vault={vault_name}&file={vault_relative_path}"


def build_markdown_link(label: str, file_path: Path) -> str:
    return f"[{label}]({build_obsidian_uri(file_path)})"


def get_page_path(wiki_path: str) -> Path:
    return WIKI_DIR / f"{wiki_path}.md"


def get_wiki_paths() -> list[str]:
    return sorted(
        build_wiki_path(path)
        for path in WIKI_DIR.rglob("*.md")
        if path != INDEX_FILE
    )


@tool
def read_index() -> str:
    """Read the wiki index. Use this first for every question."""
    return "\n".join(
        [
            f"Citation: {build_markdown_link('index', INDEX_FILE)}",
            read_text(INDEX_FILE)
        ]
    )



@tool
def list_pages() -> str:
    """List available wiki page paths excluding index."""
    return "\n".join(get_wiki_paths())


@tool
def read_page(wiki_path: str) -> str:
    """Read a wiki page by path like `topics/learning` or `sources/example`."""
    page_path = get_page_path(wiki_path)
    return "\n".join(
        [
            f"Page: {build_wiki_link(wiki_path)}",
            f"Citation: {build_markdown_link(wiki_path, page_path)}",
            read_text(page_path)
        ]
    )


model = ChatOllama(model=MODEL_NAME, temperature=0)
prompt = PromptTemplate.from_template(AGENT_PROMPT)
agent = create_react_agent(
    llm=model,
    tools=[read_index, list_pages, read_page],
    prompt=prompt,
)
wiki_agent = AgentExecutor(agent=agent, tools=[read_index, list_pages, read_page], verbose=True)

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

    result = wiki_agent.invoke({"input": question})

    answer = result.get("output", "")
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)