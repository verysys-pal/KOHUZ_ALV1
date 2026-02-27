# [PLN-18] Motor Popup 제어 패널 레이아웃 최적화 계획서
 
 > **요약**: `motor_popup.html`의 제어 패널 내 주요 섹션을 2단 구성으로 변경하고 Servo 패널을 가로형으로 최적화합니다.
 >
 > **프로젝트**: KOHUZ_ALV1
 > **작성자**: Antigravity (AI Assistant)
 > **날짜**: 2026-02-27
 > **상태**: 완료 (Done)
 
 ---
 
 ## 1. 개요 (Overview)
 
 ### 1.1 목적
 `motor_popup.html`의 제어 패널 레이아웃을 조정하여 기존의 수직 나열 방식에서 벗어나, 연관된 패널들을 병렬로 배치함으로써 화면 공간을 효율적으로 사용하고 사용자 편의성을 증대합니다.
 
 ### 1.2 배경
 사용자 지침(Instruction.md 136라인)에 따라 Dynamics/Backlash 그룹과 Jog/Homing 그룹을 다시 2단 구성으로 복구하고, Servo 패널의 내부 디자인을 개선해야 합니다.
 
 ---
 
 ## 2. 작업 범위 (Scope)
 
 ### 2.1 포함 사항 (In Scope)
 - [x] **Dynamics & Backlash**: 기존 `space-y-4` 레이아웃을 `grid-cols-2` 기반의 2단 구성으로 변경.
 - [x] **Jog Control & Homing**: 기존 `space-y-4` 레이아웃을 `grid-cols-2` 기반의 2단 구성으로 변경.
 - [x] **Servo (PID)**: 1단 구성 유지하되, P/I/D 입력 필드와 라벨을 1행(Row)에 가로로 배치.
 - [x] **대시보드 반영**: `gen_dashboard.py`를 실행하여 `dashboard.html`에 변경사항 동기화.
 
 ---
 
 ## 3. 상세 설계 (Implementation Plan)
 
 ### 3.1 레이아웃 구조 변경
 | 섹션 | 현재 구조 | 변경 후 구조 | 비고 |
 |------|-----------|--------------|------|
 | **Dynamics & Backlash** | Stacked (1-column) | Grid (2-columns) | `grid grid-cols-2 gap-4` 적용 완료 |
 | **Jog & Homing** | Stacked (1-column) | Grid (2-columns) | `grid grid-cols-2 gap-4` 적용 완료 |
 | **Servo (PID)** | Vertical rows | Single Horizontal row | `flex items-center gap-4` 적용 완료 |
 
 ---
 
 ## 4. 리스크 및 대응 (Risks and Mitigation)
 - **리스크**: 2단 구성 시 좁은 가로 폭으로 인한 텍스트 겹침 가능성.
 - **대응**: 각 입력 필드의 너비를 조절하고 라벨 텍스트를 최적화하여 가독성 유지.
 
 ---
 
 ## 5. 단계별 실행 계획 (Execution Steps)
 
 1. **[Step 1]**: `motor_popup.html` 파일 수정 (HTML/Tailwind 클래스 업데이트). - **완료**
 2. **[Step 2]**: 로컬 빌드 및 `gen_dashboard.py` 실행. - **완료**
 3. **[Step 3]**: 최종 화면 구성 확인 및 피드백 반영. - **완료**
 
 ---
 
 ## 6. 성공 기준 (Success Criteria)
 - [x] Dynamics와 Backlash가 좌우로 배치됨.
 - [x] Jog Control과 Homing이 좌우로 배치됨.
 - [x] Servo(PID)의 P, I, D 설정이 세로가 아닌 가로 한 줄로 표시됨.
 - [x] `dashboard.html`에서 정상적으로 반영됨.
