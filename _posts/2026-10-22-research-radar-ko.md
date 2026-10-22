---
title: "Research Radar — 2026년 10월 22일"
date: 2026-10-22
excerpt: "ESP32 기반 iPhone 자동화, 코딩 에이전트를 위한 오디오, 그리고 어떤 LLM도 시장을 이기지 못한 퀀트 벤치마크."
tags:
  - research-radar
  - llm-agents
  - hardware-automation
  - quantitative-finance
header:
  teaser: /images/radar/2026-10-22-card.png
lang: ko
translated_url: /blog/2026-10-22-research-radar/
---

[EN](/blog/2026-10-22-research-radar/) · [한국어](/blog/2026-10-22-research-radar-ko/)

*7달러짜리 iPhone 에이전트 해킹, 코딩 어시스턴트를 위한 청각, 프런티어 모델을 겸손하게 만드는 퀀트 벤치마크.*

## 저장소

### esp32-iphone-agent — 7달러 ESP32로 iPhone을 AI 제어 장치로 전환
[`onehumanbeing/esp32-iphone-agent`](https://github.com/onehumanbeing/esp32-iphone-agent) · C · 3,496 스타

- **새로운 점:** AirPlay로 화면을 캡처하고 USB HID로 입력을 전달하여, OpenAI 호환 비전 모델이 7달러짜리 ESP32를 통해 실제 iPhone을 조작할 수 있게 한다. Mac, 개발자 계정, 탈옥 모두 불필요.
- **왜 중요한가:** 폰 기반 에이전트 연구 비용을 고가 장비에서 범용 하드웨어 수준으로 낮춘다.
- **주의점:** README만 확인함; 지연시간, 안정성, 실제 수행 가능한 작업 범위에 대한 데이터 없음.
- **Take:** AirPlay + HID를 활용해 Apple의 폐쇄 생태계를 우회하는 영리한 접근 — Apple이 얼마나 빨리 막을지 궁금하다.

### earshot — 코딩 에이전트를 위한 오디오 인식
[`Leonxlnx/earshot`](https://github.com/Leonxlnx/earshot) · Python · 2,061 스타

- **새로운 점:** 코딩 에이전트에게 소리를 듣고, 검토하고, 생성하는 능력을 부여하며, GPU 없이 CPU만으로 동작한다.
- **왜 중요한가:** 대부분의 에이전트 툴킷은 텍스트와 이미지만 다루는데, 오디오를 추가하면 음향 파이프라인 디버깅이나 미디어 출력 검토 같은 작업이 가능해진다.
- **주의점:** README만 확인함; 지원하는 오디오 작업 범위와 기존 에이전트 프레임워크와의 통합 수준이 불분명.
- **Take:** 틈새지만 실재하는 공백 — 들을 수 없는 에이전트는 소리를 내는 것을 검증할 수 없다.

## 논문

### Quant-Arena: Benchmarking LLM Agents for Quantitative Trading Research
[arXiv 2610.30113v1](http://arxiv.org/abs/2610.30113v1) · Qian et al. · 2026

- **주장:** 실제 A주 시장 데이터에서 LLM이 피처를 구축하고, 2022–2023 피드백으로 스코어링 코드를 작성한 뒤, 봉인된 2024년 평가용 전략을 확정하는 엔드투엔드 벤치마크를 제안한다. 9개 프런티어 모델을 테스트한 결과, GPT-6 Astra가 최고점을 기록했으나 어떤 모델도 2024년에 동일가중 시장 수익률을 넘지 못했다.
- **왜 중요한가:** 수식·코드 단위 벤치마크를 넘어, 봉인된 표본외 기간으로 전체 퀀트 연구 루프를 검증한다.
- **주의점:** 초록만 확인함; A주 시장의 특수성이 일반화를 제한할 수 있으며, 호가창 충격 모델은 시뮬레이션 기반.
- **Take:** 어떤 모델도 미지 데이터에서 단순 기준선을 이기지 못했다는 헤드라인 결과가 이 논문에서 가장 유용한 숫자다.

## 출처

- [onehumanbeing/esp32-iphone-agent](https://github.com/onehumanbeing/esp32-iphone-agent)
- [Leonxlnx/earshot](https://github.com/Leonxlnx/earshot)
- [Quant-Arena: Benchmarking LLM Agents for Quantitative Trading Research (arXiv 2610.30113v1)](http://arxiv.org/abs/2610.30113v1)
