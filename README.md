# Pac-Man Project

UC Berkeley의 인공 지능 입문 과정인 CS 188을 위해 개발된 팩맨 프로젝트는 게임을 플레이하기 위해 다양한 AI 기술을 적용합니다. 이러한 프로젝트는 비디오 게임용 AI 구축이 아닌, 정보에 입각한 상태 공간 검색, 확률 추론 및 강화 학습과 같은 기본 AI 개념에 중점을 두고 있습니다. 이러한 개념은 자연어 처리, 컴퓨터 비전 및 로봇과 같은 실제 응용 분야의 기초가 됩니다. <br/>

프로젝트를 통해 우리는 구현한 기술의 결과를 시각화할 수 있으며, Pac-Man은 창의적인 솔루션을 요구하는 도전적인 문제 환경을 제공합니다. 실제 AI 문제는 매우 도전적이며 이 프로젝트에서 다루는 과제 또한 도전적입니다.<br/>


## Rules of Pac-man Survival

- 레벨 당 점수 계산: 팩맨이 음식을 먹으면 음식이 영구적으로 제거되며 10점을 얻습니다. 일반적인 채점 규칙은 다음과 같습니다. 
	- 팩맨이 움직일 때 마다 스텝 당 -1점.
	- 음식을 먹을 때마다 +10점.
	- 고스트를 잡아먹을 때마다 +200점. 
 	- 맵 내의 모든 음식을 먹으면 +500점. 이 경우, 해당 레벨이 자동으로 종료됩니다.
	- 시간 부족 또는 고스트에 의해 죽는 경우 -500.
- 레벨 종료: 팩맨이 음식을 모두 먹은 경우, 레벨이 종료됩니다 (파워 캡슐은 음식으로 계산되지 않습니다). 또한 레벨 당 에이전트는 최대 3000번의 이동만 가능합니다. 이 이동 제한에 도달한 경우에도 팩맨이 자동으로 죽게됩니다.
- 레벨 진행: 많은 수의 음식과 적은 수의 고스트가 있는 쉬운 오픈 월드부터 더 많은 벽, 더 적은 음식, 더 많은 고스트가 있는 최종 레벨까지 다양한 유형의 맵이 존재합니다. 또한 3가지 유형의 고스트(아래 설명 참조)가 있으며, 높은 레벨일수록 팩맨이 피하기 어려운 더 지능적인 고스트가 존재합니다.
- 최종 스코어 계산: 모든 레벨의 맵에 대해 자동으로 실행되며, 최종 점수는 각 레벨의 평균 점수로 계산됩니다.
- 유령: 팩맨 월드에는 3가지 유형의 고스트가 존재합니다. 초기 레벨에는 주로 추적하는 유령이 있지만, 
	- Track-following 고스트: 이 고스트는 팩맨 및 월드의 다른 모든 특성을 무시하고 임의의 트랙을 계속해서 활보합니다.
	- 무작위 고스트: 이 고스트는 매 순간 무작위로 움직임을 선택합니다
	- Pacman-seeking 고스트: 이 고스트는 80% 의 확률로 팩맨쪽으로 이동합니다. 팩맨이 파워캡슐을 얻어 고스트를 잡아먹을 수 있는 경우에는 80% 의 확률로 팩맨으로부터 멀어집니다. 때때로 20% 의 확률로 무작위로 움직이기도 합니다.


## Strategies

### Single-agent Search

복잡한 알고리즘을 구현하기 위해서는 우선 단일 에이전트를 검색하는 것에서 시작합니다. 고스트가 없고 단일 음식 펠릿만이 있는 환경에서 다양한 검색 알고리즘을 사용하여 고정된 푸드 도트를 찾도록 하였습니다. tinyMaze 맵을 사용하여 진행되었으며, 이를 위해 사용된 검색 알고리즘은 다음과 같습니다: <br/>
- DepthFirst Search (DFS)
- BreadthFirst Search (BFS)
- Uniform Cost
- A* algorithm

### Multi-agent Search




