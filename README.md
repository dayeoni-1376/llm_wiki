# LLM Wiki

Obsidian의 Clippings(스크랩)를 로컬 LLM으로 분석해서 주제(topics)·개체(entities) 중심의 지식 위키(`AI Wiki`)로 자동 구축하고, Streamlit 챗봇으로 그 위키에 질의응답할 수 있게 해주는 개인용 프로젝트입니다.

## 사용된 도구

이 프로젝트의 코드 작성 및 유지보수에는 다음 AI 코딩 도구가 사용되었습니다.

- **Codex(코덱스)**
- **GPT-5.6**
- **Codex Fable5**

## 폴더 구조

- `Clippings/` — 원본 스크랩(입력 소스)
- `AI Wiki/` — 자동 생성된 위키 (`sources/`, `topics/`, `entities/`, `index.md`)
- `llm-wiki/` — 위키 빌더·메인테이너·앱 실행 스크립트
  - `llm_wiki_builder.py` — Clippings를 분석해 위키를 생성
  - `llm_wiki_maintainer.py` — Streamlit 기반 위키 Q&A 앱
  - `launch_wiki_app.py`, `start_wiki_app.command`, `LLM Wiki.app` — 앱 실행용 런처

## 실행

```bash
cd llm-wiki
./start_wiki_app.command
```
