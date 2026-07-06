---
title: "[PT] RAG 기반 대학 규정 검색 챗봇 개발 및 성능 평가: 경희대학교 사례 연구"
collection: publications
category: conferences
permalink: /publication/2025-11-29-presentation-2
excerpt: '`Keywords: RAG, LLM, Knowledge Management, FAISS, Vector Database, University Regulations, Chatbot, RAGAS`'
date: 2025-11-29
venue: '한국전자거래학회 춘계학술대회'
paperurl: '/files/paper2.pdf'
citation: '<strong>Jang, H.</strong>, & Kim, Y*. (2025). &quot;RAG 기반 대학 규정 검색 챗봇 개발 및 성능 평가: 경희대학교 사례 연구.&quot; <i>한국전자거래학회 춘계학술대회</i>.'
---

# Abstract
본 연구는 Large Language Model (LLM)과 Retrieval Augmented Generation (RAG) 기술을 활용하여 경희대학교 규정 검색 챗봇을 개발한 사례를 제시한다. 방대한 대학 규정집의 효율적 검색과 일관된 해석을 위해 벡터 검색 시스템과 에이전트 Workflow를 구현하였다. PDF/HWP 문서를 JSON으로 구조화하고 FAISS 벡터 데이터베이스를 구축하여 컨텍스트 기반 RAG 시스템을 개발하였다. 성능 평가 결과 Faithfulness가 0.361에서 0.516으로 43% 향상되었으며, 교직원 업무시간 45% 감소, 학생 월간 처리시간 64% 단축(10.6시간→3.8시간)의 실무 개선 효과를 확인하였다. 본 연구는 LLM 기술의 실제 대학 행정 적용 가능성을 입증한 실증 사례이다.

<br/>

# Paper
<iframe src="/files/paper2.pdf#toolbar=0&navpanes=0&scrollbar=0" width="800" height="600" style="display: block; margin: auto; border: none;"></iframe>

<br/>

# Key Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Faithfulness (RAGAS) | 0.361 | 0.516 | +43% |
| Answer Relevancy | 0.837 | 0.783 | -6.4% |
| 교직원 업무시간 | - | - | -45% |
| 학생 월간 처리시간 | 10.6h | 3.8h | -64% |

<br/>

# System Architecture
- **Data Preprocessing:** HWP/PDF → JSON 변환, unstructured.io 라이브러리 활용 구조 기반 분할
- **Embedding:** OpenAI text-embedding-3-large 모델, RecursiveCharacterTextSplitter (2048자, 256자 오버랩)
- **Vector DB:** FAISS 벡터 데이터베이스 (Flat 인덱스)
- **RAG Pipeline:** History-Aware RAG, 출처 자동 병기
- **LLM:** GPT-4 기반 답변 생성

<br/>

# Key Contributions
- **JSON 전처리 최적화:** PDF 직접 임베딩 대비 Faithfulness 43% 향상
- **HWP 문서 처리:** 한국 대학 환경에 특화된 문서 처리 파이프라인 구축
- **실증적 효과 검증:** 교직원 4명, 학생 10명 대상 2주간 파일럿 운영으로 실무 개선 효과 입증
- **투명성 강화:** 답변 시 참조 문서 출처 자동 표시

<br/>

# Demo
개발된 시스템은 [https://kyunghee-chatbot-aimslab.streamlit.app](https://kyunghee-chatbot-aimslab.streamlit.app)에 배포되어 있습니다.

<br/>

# Acknowledgement
본 연구는 정부(과학기술정보통신부)의 재원으로 정보통신기획평가원의 지원을 받아 수행된 연구임 (No.RS-2022-00155911, 인공지능융합혁신인재양성(경희대학교)).
