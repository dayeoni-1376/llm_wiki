# 헤드리스 서버 + AI 에이전트 환경에서 Obsidian을 GitLab으로 동기화하기 (삽질기 포함 완전 정리)

## Summary
이 가이드는 Git과 GitLab을 사용하여 Obsidian 볼트를 강력하게 다중 장치 동기화하는 포괄적이고 고급 방법론을 제공합니다. 아키텍처 모범 사례를 상세히 설명하며, 쓰기 충돌을 방지하기 위해 모바일 장치는 읽기 전용으로 작동해야 함을 강조합니다. 이 과정은 초기 설정(SSH 키 관리), 일반적인 셸 문제 해결(zsh 주석), LFS를 통한 대용량 파일 관리, 그리고 서버, 데스크톱, 모바일 클라이언트 간의 최적 워크플로우 구축을 다루며, 공식 Obsidian Sync와 Git을 혼합하는 것을 강력히 권장하지 않습니다.

## Key Points
- **읽기 전용 모바일 전략:** 볼트 무결성을 유지하기 위해, 모바일 장치는 실수로 메인 리포지토리 브랜치에 쓰기 충돌이 발생하는 것을 방지하도록 읽기 전용 뷰어로 구성해야 합니다.
- **히스토리 정리 (LFS):** 대용량 파일을 로컬에서 삭제하지 않으면서 Git 히스토리에서 제거할 때는 `git rm --cached`를 사용하십시오.
- **셸별 수정 사항:** 올바른 주석 기능(#)을 보장하기 위해 zsh에서 `setopt interactive_comments`를 설정하는 것과 같은 셸 환경 문제를 인지하십시오.
- **단일 진실 공급원:** 항상 하나의 동기화 방법(Git 또는 공식 Sync)을 선택하고 동일한 볼트에 대해 혼합하여 사용하지 마십시오.

## Topics
[[topics/untitled]]
[[topics/untitled]]
[[topics/untitled]]
[[topics/untitled]]
[[topics/untitled]]

## Entities
[[entities/obsidian]]
[[entities/gitlab]]
[[entities/untitled]]
[[entities/git-rm-cached]]

## Raw Source
- `Clippings/헤드리스 서버 + AI 에이전트 환경에서 Obsidian을 GitLab으로 동기화하기 (삽질기 포함 완전 정리).md`
