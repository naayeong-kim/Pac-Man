# Pac-Man Project

UC Berkeley의 인공 지능 입문 과정인 CS 188을 위해 개발된 팩맨 프로젝트는 게임을 플레이하기 위해 다양한 AI 기술을 적용합니다. 프로젝트는 비디오 게임용 AI 구축이 아닌, 정보에 입각한 상태 공간 검색, 확률 추론 및 강화 학습과 같은 기본 AI 개념에 중점을 두고 있습니다. 프로젝트를 통해 우리는 구현한 기술의 결과를 시각화하고 도전적인 문제 환경에서의 창의적인 솔루션을 갖기를 기대합니다. 실제 AI 문제는 매우 도전적이며 이 프로젝트에서 다루는 과제 또한 도전적입니다.<br/>

이 프로젝트는 PyCharm IDE에서 Python을 사용하여 진행되었으며, 자세한 구현 방법 및 결과는 다음과 같은 추가 코드 파일 및 리포트에서 확인하실 수 있습니다. 최종 시연 영상은 본 문서의 하단에 첨부되어 있습니다. <br/> 
- [해당 연구에 대한 code 보러가기](/code) <br/>
- [해당 연구에 대한 full report 보러가기](report.pdf) <br/> 



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
- 계산 시간: 각 에이전트는 0.2초 이내에 각 작업(이동)을 반환해야 합니다. 그렇지 않을 시 경고가 발생되며, 경고가 3번이 발생하면 해당 레벨의 게임은 자동으로 종료됩니다.


## Strategies

### Single-goal Search

복잡한 알고리즘을 구현하기 위해서는 우선 단일 목표를 검색하는 것에서 시작합니다. 고스트가 없고 단일 음식 펠릿만이 있는 환경에서 다양한 검색 알고리즘을 사용하여 고정된 푸드 도트를 찾도록 하였습니다. tinyMaze 맵을 사용하여 진행되었으며, 이를 위해 사용된 검색 알고리즘은 다음과 같습니다: <br/>
- DepthFirst Search (DFS)
- BreadthFirst Search (BFS)
- Uniform Cost
- A* algorithm

### Multi-goal Search

여러개의 음식이 맵에 주어진 경우, 팩맨이 모든 음식을 먹기 위해 가능한 효율적으로(즉, 최소 이동 횟수로) 작동하도록 이전의 검색 방법을 확장시켰습니다. 네 모서리에 모두 도달했는지 여부를 감지하는데 필요한 모든 정보를 인코딩 하는 상태 정보를 구현하고, admisibility 한 휴리스틱을 구현하여 consistency를 갖는지 확인하는 작업이 이루어졌습니다. 또한 팩맨의 합리적인 이동을 만들어 내기 위하여 음식으로 부터 가장 짧은 경로를 찾는 함수를 추가로 구현하였습니다.

### Multi-agent pacman

주변에 Pacman을 죽이려고 하는 유령이 여러명 있는 경우입니다. 팩맨은 유령을 피하면서 펠릿을 먹는 목표를 달성하기 위해 계획을 세워야 합니다. alpha-beta prunning 및 minimax search를 구현하고 평가 함수를 설계하여 성능을 살펴보았습니다. 이를 활용하여 음식 위치와 유령의 위치를 모두 고려하여 움직이는 유능한 반사 에이전트를 만들어냈습니다.
<br/>

처음에는 alpha-beta prunning을 사용하는 다중 에이전트를 사용했습니다. 해당 에이전트는 이전에 계산된 성능들과 비교하였을 때, 더 나쁜 점수를 초래하는 무브는 포기하고 다음에 만들 무브에 영향을 줄 수 없는 최소/최대 분기를 잘라냅니다. 그러나 이동 방향을 반환하는 데 너무 많은 계산시간이 소요됨을 관찰했습니다. 결국 우리는 정교한 평가기능과 함께 간단한 반사 에이전트를 사용하기로 선택했습니다.
<br/>
그러나 단순한 반사 에이전트를 사용하기 때문에 보다 광범위한 평가 기능이 요구되어졌습니다. 우리는 다음과 같은 사항을 고려하여 더 나은 작업을 수행할 수 있었습니다:
- 게임에서 승리하는 움직임을 취하고 지는 움직임은 피합니다.
- 가능한 최소한의 움직임으로 모든 음식을 먹습니다.
- 움직이는 도중에 파워 캡슐이 있다면 먹이보다 선호되며, 이후 겁먹은 유령을 잡아먹는 움직임을 반환합니다.
- 유령이 팩맨에게 너무 가까이 올 때 충분히 멀어집니다.
- 적은 양의 음식이 남아있고 그 주위에 고스트가 존재한다면, 유령이 해당 장소에 갇히지 않도록 충분한 움직임을 만들어 냅니다.
<br/>

### >> 구현된 AI 기반 솔루션 적용 결과 영상<br/>
<img src="img/pac1.gif" width="70%"><br/>



## Result

추가적으로 구현한 알고리즘이나 결과 및 분석 등 자세한 사항은 [full report](report.pdf)를 참조바랍니다.


