# Obsidian, Gitlab and the bridge between the worlds

## Summary
이 기사는 iCloud와 같은 네이티브 서비스나 독점 동기화 기능의 한계를 우회하여 여러 장치에서 옵시디언 노트를 동기화하는 방법을 설명합니다. 이 솔루션은 Git 클라이언트, 특히 iOS용 WorkingCopy를 사용하여 로컬 옵시디언 볼트와 원격 저장소(GitLab/GitHub) 간의 데이터 동기화를 관리합니다. 이 과정에는 저장소를 볼트 폴더로 복제하고, 옵시디언에서 편집하기 전에 WorkingCopy를 통해 변경 사항을 가져온 다음, 업데이트를 커밋하고 푸시하는 워크플로우를 설정하는 것이 포함됩니다.

## Key Points
- 옵시디언의 노트는 네이티브 동기화 서비스(예: iCloud)의 제한을 우회하기 위해 WorkingCopy와 같은 Git 클라이언트를 사용하여 동기화할 수 있습니다.
- 이 동기화 방법은 앱 간 직접 통신보다는 개별 앱 간의 공유 폴더에 접근하는 것에 의존합니다.
- 시작하려면 WorkingCopy를 사용하여 원격 저장소를 옵시디언 볼트 폴더 구조로 복제해야 합니다.
- 표준 워크플로우는 WorkingCopy를 통해 변경 사항을 가져오고(pull), 옵시디언에서 노트를 편집한 다음, WorkingCopy를 통해 업데이트를 커밋하고 푸시하는 것입니다.
- WorkingCopy는 초기 설정 후 Git 프로세스(Pull/Commit/Push)를 관리하는 데 사용됩니다.

## Topics
[[topics/untitled]]
[[topics/untitled]]
[[topics/untitled]]

## Entities
[[entities/untitled]]
[[entities/gitlab]]
[[entities/workingcopy]]

## Raw Source
- `Clippings/Obsidian, Gitlab and the bridge between the worlds.md`
