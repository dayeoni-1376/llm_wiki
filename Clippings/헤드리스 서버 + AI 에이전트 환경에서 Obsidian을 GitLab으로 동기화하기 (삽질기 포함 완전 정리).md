---
title: "헤드리스 서버 + AI 에이전트 환경에서 Obsidian을 GitLab으로 동기화하기 (삽질기 포함 완전 정리)"
source: "https://bkman.tistory.com/44"
author:
  - "[[Bookman]]"
published: 2026-07-14
created: 2026-07-17
description: "홈서버(맥미니)에서 AI 에이전트를 돌리면서 마크다운 노트를 관리하다 보면, 결국 \"이 노트들을 어떻게 여러 기기에서 볼 것인가\"라는 문제에 부딪히게 됩니다. 이 글은 헤드리스 맥미니에서 에이전트가 쓰는 노트를 GitLab을 허브로 데스크톱·노트북·스마트폰까지 동기화한 전체 과정을 정리한 것입니다. 세팅 방법만이 아니라, 실제로 겪은 오류와 해결 과정, 그리고 \"왜 이 방식을 선택했는지\"까지 담았습니다.1. 왜 Obsidian Sync가 아니라 GitLab인가Obsidian을 여러 기기에서 쓰는 가장 쉬운 방법은 공식 Obsidian Sync 구독입니다. 그런데 제 환경에는 결정적인 제약이 하나 있었습니다. 헤드리스 서버는 Obsidian Sync의 정식 피어가 될 수 없다는 점입니다.Obsidian S.."
tags:
  - "clippings"
---
홈서버(맥미니)에서 AI 에이전트를 돌리면서 마크다운 노트를 관리하다 보면, 결국 "이 노트들을 어떻게 여러 기기에서 볼 것인가"라는 문제에 부딪히게 됩니다. 이 글은 헤드리스 맥미니에서 에이전트가 쓰는 노트를 GitLab을 허브로 데스크톱·노트북·스마트폰까지 동기화한 전체 과정을 정리한 것입니다. 세팅 방법만이 아니라, 실제로 겪은 오류와 해결 과정, 그리고 "왜 이 방식을 선택했는지"까지 담았습니다.

## 1\. 왜 Obsidian Sync가 아니라 GitLab인가

Obsidian을 여러 기기에서 쓰는 가장 쉬운 방법은 공식 Obsidian Sync 구독입니다. 그런데 제 환경에는 결정적인 제약이 하나 있었습니다. **헤드리스 서버는 Obsidian Sync의 정식 피어가 될 수 없다** 는 점입니다.

Obsidian Sync는 Obsidian 앱 인스턴스가 실제로 실행 중이어야 동작합니다. GUI 없이 돌아가는 헤드리스 서버에서는 앱을 상주시키는 것 자체가 부자연스럽고, 무엇보다 에이전트가 파일을 직접 읽고 쓰는 워크플로우와 따로 노는 계층이 하나 더 생깁니다.

반면 Git은 순수 CLI라 헤드리스 환경의 네이티브입니다. 에이전트 워크플로우 안에 git pull → 파일 작업 → commit → push를 그대로 끼워 넣을 수 있습니다. 부수적인 장점도 큽니다.

- **버전 관리**: 에이전트가 노트를 자동 생성·수정하는 환경에서는 "언제 뭘 바꿨는지"와 "잘못 쓰면 되돌리기"가 중요합니다. Git은 diff와 히스토리가 기본입니다.
- **충돌 가시성**: 자동화 프로세스와 사람이 같은 파일을 건드리면 충돌은 필연인데, Git은 이를 명시적으로 드러내고 사람이 머지하게 합니다. 조용히 덮어써지는 것보다 훨씬 안전합니다.
- **비용**: GitLab 무료 플랜으로 충분합니다. 무료 플랜은 프로젝트당 저장소+LFS 합산 10GiB 한도인데, 마크다운 위주라면 한참 여유가 있습니다.

단점도 분명히 있습니다. **모바일 경험이 공식 Sync보다 훨씬 거칩니다.** 이 부분은 뒤에서 자세히 다룹니다. 그리고 한 가지 강조하고 싶은 것 — **Git과 Obsidian Sync를 같은 vault에 동시에 얹는 하이브리드는 절대 권하지 않습니다.** 두 동기화 메커니즘이 같은 파일을 건드리면 서로의 변경을 덮어쓰면서 관리 비용이 폭증합니다. 하나를 진실의 원천으로 정해야 합니다.

## 2\. 폴더 구조 설계 — 마크다운과 대용량 파일의 분리

핵심 설계 결정은 **마크다운 노트와 대용량 첨부파일(엑셀·PDF·워드)을 형제 폴더로 분리** 하는 것입니다.

```
~/vault/                    ← git 리포 루트
├── .gitattributes          ← LFS 추적 규칙
├── .gitignore
├── ObsidianVault/          ← Obsidian이 여는 vault (md 전용)
│   ├── .obsidian/
│   ├── Notes/
│   ├── Projects/
│   └── Research/
└── RealFiles/              ← 대용량 원본 파일
    ├── Projects/
    └── Research/
```

이렇게 나누는 이유는 두 가지입니다. 첫째, Obsidian이 대용량 바이너리를 인덱싱하지 않아 성능에 유리합니다. 둘째, 동기화 정책을 다르게 가져갈 수 있습니다. 저는 처음엔 RealFiles도 Git LFS로 올렸다가, 결국 **원격에서 빼고 서버 로컬에만 두는** 쪽으로 정리했습니다. 노트(지식)는 어디서나 보고 싶지만, 원본 파일은 서버에 있으면 충분했고 10GiB 한도를 아끼는 효과도 있었기 때문입니다.

## 3\. GitLab 프로젝트 생성

1. GitLab.com 로그인 → 우상단 **+** → **New project → Create blank project**
2. 이름 입력, Visibility는 **Private**
3. **"Initialize repository with a README" 체크 해제** — 로컬 리포를 그대로 푸시할 것이므로 비워둡니다
4. 생성 후 SSH 주소를 메모합니다: git@gitlab.com:<계정>/<프로젝트>.git

## 4\. 서버(맥미니) 세팅

### 사전 준비

```
git --version || xcode-select --install
brew install git-lfs
git lfs install

git config --global user.name "server"
git config --global user.email "본인 이메일"
```

user.name/user.email 설정은 사소해 보이지만 빠뜨리면 나중에 커밋 시점에 Please tell me who you are 에러로 멈춥니다. 서버뿐 아니라 **모든 기기에서** 해야 합니다. 실제로 노트북 세팅 때 이걸 빠뜨려서 한참 헤맸습니다.

### SSH 키 인증

헤드리스 자동화에는 비밀번호 없는 SSH 키가 정답입니다.

```
ssh-keygen -t ed25519 -C "server" -f ~/.ssh/id_ed25519_gitlab
cat ~/.ssh/id_ed25519_gitlab.pub
```

출력된 공개키를 GitLab **Preferences → SSH Keys** 에 등록하고, ~/.ssh/config에 호스트를 지정합니다.

```
Host gitlab.com
  HostName gitlab.com
  User git
  IdentityFile ~/.ssh/id_ed25519_gitlab
```

ssh -T git@gitlab.com 실행 시 Welcome 메시지가 나오면 통과입니다.

**팁**: 기기마다 SSH 키를 따로 만드는 것을 권합니다. 기기 하나를 정리할 때 그 키만 GitLab에서 폐기하면 되기 때문입니다.

### 리포 초기화 — 순서가 중요합니다

**LFS 추적 규칙은 반드시 첫 git add 전에** 설정해야 합니다. 순서가 어긋나면 바이너리가 일반 blob으로 커밋되어 나중에 git lfs migrate로 히스토리를 다시 써야 하는 큰 공사가 됩니다.

```
cd ~/vault
git init -b main

# (1) LFS 추적 먼저
git lfs track "*.pdf" "*.xlsx" "*.docx" "*.pptx" "*.zip"

# (2) .gitignore — 기기마다 달라 충돌만 일으키는 Obsidian UI 상태 제외
cat > .gitignore << 'EOF'
.DS_Store
.trash/
ObsidianVault/.obsidian/workspace.json
ObsidianVault/.obsidian/workspace-mobile.json
ObsidianVault/.obsidian/cache
EOF

# (3) 그다음에 add/commit/push
git remote add origin git@gitlab.com:<계정>/<프로젝트>.git
git add .
git commit -m "Initial vault structure"
git push -u origin main
```

.obsidian 폴더 자체는 추적합니다. 플러그인·설정을 기기 간 공유하는 편이 편하고, 기기별 UI 상태 파일 세 개만 빼면 충돌이 거의 없습니다.

푸시 후 git lfs ls-files에 바이너리 파일들이 뜨는지 확인하세요. 목록에 있으면 git에는 포인터만, 실파일은 LFS에 들어간 정상 상태입니다. 더 확실하게는 git show HEAD:"경로/파일.xlsx" | head -3을 실행해서 version [https://git-lfs.github.com/spec/v1](https://git-lfs.github.com/spec/v1) 로 시작하는 포인터 텍스트가 나오는지 보면 됩니다.

### 자주 하는 실수 — origin 등록 누락

세팅 중 커밋은 잘 쌓이는데 fatal: 'origin' does not appear to be a git repository 에러가 난다면 git remote add origin을 빠뜨린 것입니다. git remote -v로 확인하고 등록한 뒤 git push -u origin main으로 밀면, 그동안 쌓인 커밋이 한 번에 올라갑니다.

## 5\. 자동 동기화 — 이중 트리거 구조

서버의 동기화는 두 경로로 트리거되게 설계했습니다.

1. **에이전트 직후 호출**: 에이전트가 노트를 쓰고 나면 워크플로우 마지막에 동기화 스크립트를 호출 → 거의 즉시 push
2. **launchd 5분 타이머**: 다른 기기에서 들어온 변경 회수 + 누락분 안전망

트리거가 둘이면 실행이 겹칠 수 있으므로, 스크립트에 **동시 실행 방지 락** 을 넣는 것이 핵심입니다.

```bash
#!/bin/bash
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
VAULT="$HOME/vault"
LOCKDIR="/tmp/vault-sync.lock"

# mkdir는 원자적이므로 락으로 활용 — 다른 실행 중이면 조용히 종료
if ! mkdir "$LOCKDIR" 2>/dev/null; then
  exit 0
fi
trap 'rmdir "$LOCKDIR"' EXIT

cd "$VAULT" || exit 1

git add -A
git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M:%S')" 2>/dev/null

if git pull --no-rebase --no-edit origin main; then
  git push origin main
else
  echo "[$(date)] vault sync CONFLICT" >> "$HOME/vault-sync.log"
fi
```

몇 가지 설계 포인트를 설명하면 이렇습니다.

- **export PATH**: launchd는 로그인 셸의 PATH를 물려받지 않아서, Homebrew로 설치한 git-lfs 등을 못 찾을 수 있습니다. 명시가 안전합니다.
- **mkdir 락**: mkdir은 원자적(atomic) 연산이라 두 프로세스가 동시에 진입해도 하나만 성공합니다. 파일 기반 락보다 단순하고 견고합니다.
- **충돌 시 자동 머지하지 않음**: pull이 실패하면 로그만 남기고 멈춥니다. 단일 작성자 위주 환경에서 충돌은 드물고, 났을 때 조용히 덮어쓰는 것보다 멈춰서 알리는 편이 안전합니다.
- 변경이 없으면 commit이 no-op으로 끝나 불필요한 커밋이 쌓이지 않습니다.

launchd 등록은 ~/Library/LaunchAgents/에 plist를 만들어 StartInterval을 300초로 두면 됩니다.

```
http://www.apple.com/DTDs/PropertyList-1.0.dtd">

  Labellocal.vaultsync
  ProgramArguments
  
    /bin/bash
    /Users/<계정>/scripts/vault-sync.sh
  
  StartInterval300
  StandardErrorPath/tmp/vault-sync.err.log
```

launchctl load 후 launchctl list | grep vaultsync에서 상태 코드가 0이면 정상입니다.

### 에이전트 지시문 작성 시 배운 것

에이전트에게 "파일을 쓴 뒤 동기화 스크립트를 호출하라"고 지시할 때, 지시문을 허술하게 쓰면 에이전트가 이상한 방향으로 폭주할 수 있습니다. 실제로 겪은 사례인데, 스크립트 호출에 셸 백그라운드 연산자(&)를 붙이라고 했더니 에이전트의 터미널 도구가 이를 경고로 감지했고, 에이전트는 그 **경고를 치명적 실패로 오인** 해서 "올바른 호출법"을 찾겠다며 스킬 설정 파일을 대여섯 번 덮어쓰고, 존재하지도 않는 경로를 지어내는 사태까지 갔습니다.

여기서 얻은 교훈을 지시문에 반영하면 이렇습니다.

```markdown
## 최종 단계: GitLab 동기화 (반드시 마지막에 1회만)

vault 내 파일의 생성·수정·삭제를 모두 완료한 뒤, 워크플로우 종료 직전에
아래 명령을 정확히 한 번만 실행한다.

    bash "/경로/vault-sync.sh"

### 규칙
- 명령은 위 한 줄 그대로 실행한다. \`&\`, 리다이렉션 등을 덧붙이지 않는다.
- 실행 결과로 경고가 떠도 명령은 정상 수행된 것이다. 경고를 실패로
  간주하지 말고, 재시도하거나 설정을 수정하지 않는다.
- 이 명령은 워크플로우당 한 번만. 파일마다 호출하지 않는다.
- vault를 변경하지 않은 작업에서는 실행하지 않는다.
```

특히 **"경고를 실패로 간주하지 말 것"** 항목이 폭주 재발 방지의 핵심이었습니다. 에이전트는 도구의 경고 메시지에 과민하게 반응해 멀쩡한 설정을 스스로 망가뜨리는 경향이 있습니다.

## 6\. 데스크톱(macOS/Windows) 세팅

편집용 기기에서는 리포를 클론하고 Obsidian으로 **ObsidianVault/ 하위폴더** 를 vault로 엽니다. 리포 루트가 아니라 하위폴더를 여는 것이 포인트입니다.

동기화는 커뮤니티 플러그인 **obsidian-git** (작성자 Vinzent03, 목록에는 "Git"으로 표시)이 담당합니다. 설정은 세 가지면 충분합니다.

- **Auto commit-and-sync interval: 5** (분 단위 자동 commit+push)
- **Auto pull interval: 5**
- **Pull on startup: ON**

참고로 이 플러그인은 버전에 따라 설정 항목 이름이 다릅니다. 예전 문서에는 "Vault backup interval"로 나오는데 최신 버전에서는 "Auto commit-and-sync interval"입니다. 여기서 "sync"는 pull 후 push를 한 번에 한다는 의미입니다.

### Windows에서 추가로 겪은 것들

Windows 노트북을 붙이면서 겪은 함정들입니다. 맥 기준 가이드를 따라 하다 보면 반드시 만나게 되는 것들이라 정리해 둡니다.

**PowerShell은 문법이 다릅니다.** command1 || command2 같은 bash 관용구가 구버전 PowerShell에서 파서 에러를 냅니다. 명령을 한 줄씩 따로 실행하면 됩니다. 설치는 winget이 편합니다.

```sql
winget install --id Git.Git -e
winget install --id GitHub.GitLFS -e
```

설치 후 **PowerShell 창을 완전히 닫고 새로 열어야** PATH가 갱신됩니다. 참고로 LFS 설치가 exit code 1로 실패해도 당황할 필요 없습니다. Git for Windows에 LFS가 이미 포함된 경우 "이미 있어서" 실패하는 것으로, git lfs version이 나오면 정상입니다.

**줄바꿈(CRLF) 설정.** Windows와 맥/리눅스는 줄바꿈 방식이 달라, 그냥 두면 파일이 통째로 "변경됨"으로 잡혀 불필요한 커밋과 충돌이 생깁니다. 한 번만 설정해 두세요.

```
git config --global core.autocrlf input
```

**git 신원 설정 누락.** 위에서 언급한 Please tell me who you are 에러입니다. 클론까지는 잘 되는데 obsidian-git이 커밋하려는 순간 멈춥니다. git config --global user.name/user.email을 미리 해두면 됩니다.

**SSH 공개키 복사 깨짐.** 공개키를 화면에서 드래그해 복사하다 일부가 잘리면 GitLab이 "Key is invalid" 에러를 냅니다. PowerShell에서 클립보드로 직접 복사하는 것이 안전합니다.

```
Get-Content $env:USERPROFILE\.ssh\id_ed25519_gitlab.pub | Set-Clipboard
```

참고로 "Fingerprint has already been taken" 에러는 그 키가 이미 등록돼 있다는 뜻입니다. 이 경우 ssh -T git@gitlab.com으로 연결이 되는지부터 확인하면 헛수고를 줄일 수 있습니다.

### zsh에서 # 주석이 안 먹을 때

원격 SSH로 서버에 붙어 가이드의 명령 블록을 통째로 붙여넣다 보면, 주석 줄(#...)에서 command not found 에러가 날 수 있습니다. macOS 기본 셸인 zsh는 대화형 모드에서 #를 주석으로 처리하지 않는 것이 기본값이기 때문입니다. 해결은 한 줄입니다.

```bash
echo 'setopt interactive_comments' >> ~/.zshrc
```

## 7\. 대용량 파일을 원격에서 빼기

앞서 언급했듯 저는 처음에 RealFiles를 LFS로 올렸다가 나중에 뺐습니다. 이때 유용한 것이 git rm --cached입니다. --cached를 붙이면 **git 추적만 끊고 디스크의 실제 파일은 남깁니다.**

```
git rm -r --cached RealFiles
echo "RealFiles/" >> .gitignore
git add .gitignore
git commit -m "Keep large files local only"
git push origin main
```

한 가지 알아둘 점: 이 방법은 현재 시점 이후로만 제거합니다. 과거 히스토리와 LFS 객체에는 파일이 남아 용량을 차지합니다. 민감 자료라 흔적까지 지워야 한다면 git filter-repo로 히스토리를 다시 써야 하는데, 되돌릴 수 없는 무거운 작업이므로 신중하게 판단해야 합니다.

## 8\. 모바일(안드로이드) — 읽기 전용 뷰어 전략

모바일이 이 구성에서 가장 거친 부분입니다. 결론부터 말하면, 저는 폰을 **읽기 전용 뷰어** 로 못 박았고 이 결정에 매우 만족합니다.

### 왜 읽기 전용인가

기기가 늘수록 동시 편집으로 인한 충돌 확률이 올라갑니다. 그런데 폰에서 본격적으로 편집할 일은 사실 많지 않고, 급한 메모는 서버의 에이전트에게 메신저로 시키면 그쪽 경로로 vault에 들어옵니다. 즉 **쓰기는 서버 한 곳으로 일원화** 하고 폰은 받기만 하면, 폰발 충돌이 구조적으로 0이 됩니다.

이를 강제하는 방법이 **read 전용 액세스 토큰** 입니다. GitLab **Preferences → Access Tokens** 에서 scope를 read\_repository만 체크해 토큰을 만들면, 이 토큰으로는 push 자체가 불가능합니다. 실수로라도 폰에서 뭔가 올라갈 일이 없습니다.

### 세팅 절차

모바일에서는 SSH 키보다 HTTPS+토큰이 훨씬 수월합니다.

1. Obsidian 앱 설치 후 **빈 vault를 앱 저장소에** 생성 — 저장 위치 선택에서 반드시 "앱 저장소"를 골라야 합니다. 공유 저장소(기기 저장소)에 만들면 안드로이드 권한 문제로 git이 "Git is not ready" 상태에서 벗어나지 못하는 경우가 많습니다.
2. Community plugins 활성화 → "Git" 플러그인 설치·활성화
3. 명령 팔레트에서 **"Git: Clone an existing remote repo"** 실행
	- 모바일에서 명령 팔레트 찾기가 은근히 어려운데, 설정의 Toolbar 항목에서 하단 툴바에 "명령 팔레트 열기"를 추가해 두면 편합니다.
4. URL 입력. 인증 프롬프트가 제대로 안 뜨는 경우가 있어, 처음부터 URL에 인증을 넣는 형식이 안정적입니다.
	```xml
	https://<계정>:<read전용토큰>@gitlab.com/<계정>/<프로젝트>.git
	```
5. "원격 리포 루트에.obsidian이 있느냐"는 질문 → 우리 구조에서는 루트가 아니라 하위폴더에 있으므로 **No**
6. vault root에 클론하겠느냐 → **Yes** (폰 vault는 이 리포 전용이므로)
7. 중간에 author name/email이 not set이라는 경고가 떠도, 읽기 전용 용도에서는 무시해도 됩니다. 커밋(쓰기)에만 필요한 정보라 클론과 pull은 그것과 무관하게 진행됩니다.

### 읽기 전용 설정

클론 후 Git 플러그인 설정에서 다음과 같이 맞춥니다.

- **Pull on startup: ON** — 앱 열 때 자동 최신화. 뷰어의 핵심 동작입니다.
- **Auto commit-and-sync interval: 0** — 자동 커밋/푸시 끔
- **Push on commit-and-sync: OFF**

이러면 폰은 "열면 최신, 절대 안 보냄" 상태가 됩니다.

### 안드로이드 특유의 한계 — 빈 폴더 잔존

쓰다 보면 한 가지 증상을 만나게 됩니다. **다른 기기에서 폴더째 노트를 지웠는데, 폰에는 빈 폴더 껍데기가 남는** 현상입니다. PC에서는 깔끔하게 사라지는데 폰에서만 그렇습니다.

원인은 구현 차이입니다. 데스크톱 obsidian-git은 시스템의 진짜 git을 쓰지만, 안드로이드 버전은 isomorphic-git이라는 JavaScript 구현을 내장하는데, 이쪽이 pull 후 빈 디렉토리를 정리하는 처리가 약합니다. 설정으로 고칠 수 있는 문제가 아닙니다.

다행히 대응은 간단합니다. 빈 폴더는 원격에 존재하지 않으므로, **폰에서 길게 눌러 삭제하면 끝** 입니다. 다음 pull이 되살리지 않습니다(원격에 없으니까요). 반대로 원격에 파일이 있는 폴더는 지워도 pull이 되살리므로, 데이터가 사라질 걱정도 없습니다. 껍데기가 많이 쌓였다면 vault를 지우고 재클론하는 것도 방법입니다. 읽기 전용이라 폰 로컬에 잃을 것이 없기 때문에 부담 없는 리셋입니다.

## 9\. 최종 구조

완성된 토폴로지는 이렇습니다.

```
GitLab (중앙 허브)
       /        |          \
   서버       데스크톱들      폰
(에이전트,    (Obsidian,   (Obsidian,
 쓰기+자동     양방향        읽기 전용
 동기화)      편집)         뷰어)
```
- **서버**: 에이전트가 노트를 쓰면 직후 push, 5분 타이머가 안전망
- **데스크톱**: obsidian-git 5분 주기 양방향
- **폰**: read 전용 토큰 + startup pull, 순수 뷰어

운영 요령은 단순합니다. 여러 기기를 오갈 때는 **작업 시작 전 pull, 끝나고 push** 습관 하나면 충돌은 거의 없습니다. 충돌이 나더라도 git은 양쪽 내용을 마커로 둘 다 남겨두므로 데이터가 사라지지는 않습니다.

## 10\. 마치며 — 이 구성이 맞는 사람

정리하면 이렇습니다.

- **서버/에이전트가 vault를 직접 다루는 것이 핵심이라면** Git 동기화가 정답에 가깝습니다. 버전 관리와 충돌 가시성은 덤이고, 비용도 들지 않습니다.
- **폰에서의 매끄러운 편집 경험이 핵심이라면** 공식 Obsidian Sync가 낫습니다. 모바일 git은 분명히 거칩니다.
- **둘을 섞지는 마세요.** 하나만 고르는 것이 이 글에서 가장 강조하고 싶은 조언입니다.

세팅 자체는 반나절이면 끝나지만, 실제로는 자잘한 함정(신원 설정, CRLF, zsh 주석, 안드로이드 저장 위치 등)에서 시간을 씁니다. 이 글의 삽질 기록이 그 시간을 아껴드리길 바랍니다.

#### 'AI 활용기' 카테고리의 다른 글

| [맥미니로 24시간 도는 AI 에이전트 만들기 (3) — 활용기: 커스텀 스킬과 멀티에이전트](https://bkman.tistory.com/40) (0) | 2026.06.23 |
| --- | --- |
| [맥미니로 24시간 도는 AI 에이전트 만들기 (2) — 모델 운용기](https://bkman.tistory.com/39) (0) | 2026.06.23 |
| [맥미니로 24시간 도는 AI 에이전트 만들기 (1) — 구축기](https://bkman.tistory.com/38) (1) | 2026.06.23 |