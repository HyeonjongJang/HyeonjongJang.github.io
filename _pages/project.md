---
layout: archive
title: "Projects & Programs"
permalink: /project/
author_profile: true
redirect_from:
  - /project
---

{% include base_path %}

<style>
.archive details {
  border: 1px solid #e6e8eb;
  border-radius: 6px;
  margin: 0.45em 0;
  padding: 0 0.9em;
  background: #fafbfc;
  transition: background 0.15s, border-color 0.15s;
}
.archive details[open] {
  background: #fff;
  border-color: #d4d9df;
}
.archive summary {
  cursor: pointer;
  list-style: none;
  padding: 0.6em 0 0.6em 1.5em;
  position: relative;
  outline: none;
}
.archive summary::-webkit-details-marker { display: none; }
.archive summary::before {
  content: "\25B8"; /* triangle */
  position: absolute;
  left: 0.35em;
  top: 0.55em;
  color: #9aa4ae;
  transition: transform 0.15s;
}
.archive details[open] summary::before {
  transform: rotate(90deg);
}
.archive summary:hover { color: #0067b8; }
.archive summary code {
  background: #eef2f7;
  color: #3a6ea5;
  font-size: 0.78em;
  font-weight: 600;
  padding: 0.12em 0.5em;
  border-radius: 4px;
  margin-right: 0.45em;
  vertical-align: middle;
}
.archive summary em {
  font-style: normal;
  background: #fff4e0;
  color: #a8620a;
  font-size: 0.78em;
  padding: 0.12em 0.5em;
  border-radius: 4px;
  margin-left: 0.3em;
  vertical-align: middle;
}

/* Dark theme (site applies data-theme="dark" on <html>) */
html[data-theme="dark"] .archive details {
  background: #3f3f3f;
  border-color: #5a5a5a;
}
html[data-theme="dark"] .archive details[open] {
  background: #4a4a4a;
  border-color: #6b6b6b;
}
html[data-theme="dark"] .archive summary {
  color: #f2f2f2;
}
html[data-theme="dark"] .archive summary::before {
  color: #aab4be;
}
html[data-theme="dark"] .archive summary:hover {
  color: #4db8e0;
}
html[data-theme="dark"] .archive summary code {
  background: #2f4a63;
  color: #bcd8f0;
}
html[data-theme="dark"] .archive summary em {
  background: #5a4520;
  color: #ffcf8a;
}
</style>

**Work Projects**
----

**Kyung Hee University — Course Support Assistant (English/Japanese), Humanitas College, Global Campus (경희대학교 국제캠퍼스 후마니타스칼리지 조교)**
- `Address:` Humanitas College, Kyung Hee University Global Campus, Yongin, Gyeonggi-do
- `Period:` 2026.03 ~ Present
- `Role:` Course Support Assistant — course-support office operations, English/Japanese assistance, computer-lab & server administration, and planning/operation of faculty training, engineer certification exams, and the design-skills competition

<details>
<summary><strong><code>2026–Present</code> TA Scheduling System — first-come-first-served slot reservation (in production)</strong></summary>
<div markdown="1">

- `Role:` Developer
- `Tech Stack:` Python, Web Application, Database
- `Contents:` <br/>
1. Built a ticket-style reservation system that automatically accepts teaching-assistant timetable sign-ups on a first-come-first-served basis. <br/>
2. Replaced manual, error-prone scheduling with an automated intake flow, eliminating double-booking and cutting coordination overhead. <br/>
3. Deployed to real operation and adopted by the Humanitas College course-support office. <br/>

</div>
</details>

<details>
<summary><strong><code>2026–Present</code> Humanitas Staff Chatbot — internal work-guidance assistant (in use)</strong></summary>
<div markdown="1">

- `Role:` Developer
- `Tech Stack:` Python, LLM, RAG, Streamlit
- `Contents:` <br/>
1. Developed an internal chatbot for Humanitas College staff, covering onboarding and day-to-day administrative task guidance. <br/>
2. Provided instant answers to routine work questions via a RAG-based knowledge base, reducing repetitive inquiries. <br/>
3. Adopted by college staff in real operation. <br/>

</div>
</details>

<br/>

**IDO Co., Ltd. — Dormitory Management Assistant, KHU Global Campus (주식회사 이도, 경희대학교 국제캠퍼스 제2기숙사)**
- `Address:` Kyung Hee University Global Campus, 2nd Dormitory, Yongin, Gyeonggi-do
- `Period:` 2025.02 ~ 2026.02
- `Role:` Dormitory Management Assistant (Administrative & Technical Operations)

<details>
<summary><strong><code>2025–2026</code> Dormitory Chatbot — RAG Q&A assistant for staff & onboarding</strong></summary>
<div markdown="1">

- `Role:` Developer
- `Tech Stack:` Python, LLM, RAG, Streamlit
- `Contents:` <br/>
1. Developed a dormitory-specific chatbot to enhance work efficiency for staff, new assistants, and mentors. <br/>
2. Implemented RAG-based Q&A system for instant access to dormitory regulations and guidelines. <br/>
3. Reduced repetitive inquiries and improved onboarding experience for new team members. <br/>

</div>
</details>

<br/>

**[Esu Partners — Lead AI Developer & Project Manager (이수파트너스)](https://esupartners.com/)**
- `Address:` 6th floor, 47 Gwangjang-ro 2beon-gil, Sasang-gu, Busan
- `Period:` 2023.07 ~ 2024.06 (1 Year)
- `Role:` Lead AI Developer & Project Manager (Healthcare/Platform)

<details>
<summary><strong><code>2023–2024</code> Kinicare — personalized cancer-patient nutrition app (10K+ downloads)</strong></summary>
<div markdown="1">

- `Link:` [Google Play Store](https://play.google.com/store/apps/details?id=com.utinfra.jihun.kinicare&hl=ko&pli=1)
- `Role:` Lead AI Developer
- `Tech Stack:` Python, Machine Learning, Mobile App Development
- `Achievements:` 
  - Joint research project with Severance Hospital (Sinchon)
  - Built personalized nutrition algorithm based on 100,000+ cancer patient diet records
  - 10,000+ downloads on Google Play Store
- `Contents:` <br/>
1. Developed and refined a personalized nutrition management algorithm tailored to cancer type and treatment stage. <br/>
2. Built a real-time nutritional analysis and personalized feedback engine based on big data. <br/>
3. Led the entire process from data architecture design to app deployment and operation. <br/>

</div>
</details>

<details>
<summary><strong><code>2023–2024</code> Mukkebi — national public delivery platform (1.75M downloads, PM)</strong></summary>
<div markdown="1">

- `Link:` [Google Play Store](https://play.google.com/store/apps/details?id=mukkebi.user.app.android)
- `Role:` Project Manager
- `Tech Stack:` Mobile App Development, Backend Systems, Payment Integration
- `Achievements:` 
  - 1.75 million cumulative downloads / 1 million+ on Google Play Store
  - Largest regional coverage nationwide (Seoul, Gyeongbuk, Jeonnam, etc.)
  - ~8.6% market share (as of 2025) in public delivery sector
- `Contents:` <br/>
1. Oversaw the entire product roadmap and development lifecycle as PM. <br/>
2. Achieved service stability and enhanced functionality in a high-traffic environment. <br/>
3. Successfully launched key features including improved UX and local currency-linked payment system. <br/>

</div>
</details>

<details>
<summary><strong><code>2023–2024</code> Cocodrone — 3D drone-simulation edutech (Unity)</strong></summary>
<div markdown="1">

- `Link:` [Cocodrone Official](http://cocodrone.co.kr/kr/sub3_1.html?pa_id=sub3_1&code=30)
- `Role:` Core Engine Developer
- `Tech Stack:` Unity, C#, 3D Modeling, Drone Physics Simulation
- `Contents:` <br/>
1. Led the development of the core engine and content for an edutech-based 3D drone simulator. <br/>
2. Precisely simulated real-world drone flight dynamics using Unity/3D engine. <br/>
3. Visualized Gaya historical sites in high-resolution virtual space. <br/>

</div>
</details>

<details>
<summary><strong><code>2023–2024</code> ODDS — interactive screen-futsal system (Unity)</strong></summary>
<div markdown="1">

- `Role:` Software Architect & Core Engine Developer
- `Tech Stack:` Unity, Sensor Integration, Projection Mapping, Real-time Tracking
- `Contents:` <br/>
1. Designed overall software architecture for the immersive sports platform "ODDS." <br/>
2. Implemented interactive game logic tracking user movements and ball trajectories in real-time. <br/>
3. Developed an integrated control system combining hardware and software for optimal UX. <br/>

</div>
</details>

<details>
<summary><strong><code>2023–2024</code> IDCO — nationwide GIS construction-zone platform</strong></summary>
<div markdown="1">

- `Role:` Backend Developer & GIS System Architect
- `Tech Stack:` Python, GIS, Mobile App Development, Real-time Data Visualization
- `Contents:` <br/>
1. Established infrastructure for automatic/manual grid-based construction zone setting and GIS data visualization based on entire South Korean land data. <br/>
2. Developed worksite-specific zone allocation logic enabling tens of thousands of workers to check assigned zones in real-time via mobile app. <br/>
3. Improved construction status tracking accuracy and prevented work duplication through digitization. <br/>

</div>
</details>

<br/>

**Projects**
----

<details>
<summary><strong><code>2025</code> CGAFuzz — curriculum-guided adaptive fuzzing (AFL++)</strong> 🏆 <em>Excellence Prize, KRW 2,000,000</em></summary>
<div markdown="1">

- `Link:` [GitHub](https://github.com/HyeonjongJang/CGAFuzz)
- `Role:` Team Leader
- `Period:` 2025 AI-Powered Vulnerability Discovery System Competition, 2025.09 ~ 2025.10
- `Tech Stack:` AFL++, Curriculum Learning, EMA-based Adaptive Mutation, LLM-powered Seed Generation
- `Prize:` [Excellence Prize](/images/AI를_활용한_취약점_발굴_시스템_공모전_상장_ver01.jpg), Chairperson of the IT Platform Safety Research Group, <strong>KRW 2,000,000</strong>
- `Contents:` <br/>
1. Designed a three-phase progression strategy based on JSON validation success rates using Parse-Rate Driven Curriculum Learning. <br/>
2. Proposed EMA-Based Adaptive Mutation, a lightweight and real-time operator scheduling mechanism that learns mutations capable of discovering new paths. <br/>
3. Implemented Plateau Detection to automatically identify coverage stagnation and integrated optional LLM support to generate diverse initial seeds. <br/>
4. Demonstrated superior performance in both code coverage (+4.03%) and execution speed (+6.50%) compared to standard AFL++. <br/>

</div>
</details>

<details>
<summary><strong><code>2025</code> RAG-FSR — RAG language model for food-science journal classification</strong> 🏆 <em>Top Excellence Prize, KRW 500,000</em></summary>
<div markdown="1">

- `Role:` Team Leader
- `Period:` 2025 Korea Food Research Institute Food Data Analysis and Utilization Competition, 2025.06 ~ 2025.07
- `Tech Stack:` RAG (Retrieval-Augmented Generation), NLP, LLM, Python
- `Prize:` [Top Excellence Prize](/images/한국식품연구원_상장1.jpg), President of Korea Food Research Institute (KFRI), <strong>KRW 500,000</strong>
- `Contents:` <br/>
1. Addressed limitations of existing keyword-based search systems for rapidly increasing academic data in science and technology. <br/>
2. Proposed and implemented RAG-FSR, a language model specialized for the food research domain utilizing RAG technology. <br/>
3. Achieved accuracy of 0.960 in multi-keyword classification task; 4-9x better exact-match accuracy for abstract generation compared to baseline models. <br/>
4. Empirically demonstrated effective mitigation of hallucination phenomenon in large language models. <br/>

</div>
</details>

<details>
<summary><strong><code>2024–Present</code> KyungHee-Chatbot — RAG assistant for university regulations</strong></summary>
<div markdown="1">

- `Link:` [GitHub](https://github.com/HyeonjongJang/KyungHee-Chatbot)
- `Role:` Developer
- `Period:` 2024 ~ Present
- `Tech Stack:` Python, LangChain, FAISS, Streamlit, OpenAI API, Knowledge Graph (OWL/SHACL)
- `Contents:` <br/>
1. Developed a Virtual Assistant delivering answers based on the latest regulations from Kyung Hee University's Regulation Management System. <br/>
2. Implemented RAG architecture using FAISS-based dense retriever with document embedding and reranking capabilities. <br/>
3. Built Knowledge Graph-first architecture with OWL schema and SHACL shapes for structured regulation data management. <br/>
4. Designed query routing and parsing system to efficiently handle diverse user questions. <br/>
5. Deployed on Streamlit Cloud with member ID verification for access control. <br/>

</div>
</details>

<details>
<summary><strong><code>2024</code> Convex — Seoul parking assignment via convex optimization</strong></summary>
<div markdown="1">

- `Link:` [GitHub](https://github.com/HyeonjongJang/Convex)
- `Role:` Developer
- `Period:` 2024
- `Tech Stack:` Python, Flask, CVXPY, ECOS Solver, Leaflet.js, OpenAI GPT API
- `Contents:` <br/>
1. Developed a Convex Optimization-based parking lot assignment system for Seoul optimizing efficiency, distance, and cost simultaneously. <br/>
2. Implemented real-time optimization for 1,000+ users, achieving 6.4% reduction in congestion score and 2.2% reduction in average distance vs Greedy algorithm. <br/>
3. Designed multi-objective optimization with adjustable weights (α, β, γ) using CVXPY and ECOS solver. <br/>
4. Integrated OpenAI GPT API for AI-powered weight recommendation based on situational scenarios. <br/>
5. Built real-time congestion visualization dashboard for 62 major Seoul locations using Leaflet.js. <br/>

</div>
</details>

<details>
<summary><strong><code>2024</code> Google Image Scraping — food-image dataset crawler (Selenium)</strong></summary>
<div markdown="1">

- `Link:` [GitHub](https://github.com/HyeonjongJang/Crawling)
- `Role:` Developer
- `Period:` 2024
- `Tech Stack:` Python, Selenium/BeautifulSoup (Web Scraping)
- `Contents:` <br/>
1. Developed an automated web scraping tool to collect food images from Google Images for machine learning dataset construction. <br/>
2. Implemented batch processing to crawl approximately 200 images per food menu item from a predefined menu list. <br/>
3. Designed utility functions for efficient image downloading and storage management. <br/>

</div>
</details>

<details>
<summary><strong><code>2023–2024</code> Fseg-app — food detection, segmentation & nutrition (YOLOv5, SAM)</strong></summary>
<div markdown="1">

- `Link:` [GitHub](https://github.com/Esupartners/Fseg-app)
- `Role:` Team Member
- `Period:` 2023 ~ 2024
- `Tech Stack:` Python, YOLOv5, SAM (Segment Anything Model), FastAPI, Conda
- `Contents:` <br/>
1. Developed a comprehensive solution for automating food detection, segmentation, classification, and nutrition value calculation. <br/>
2. Implemented food type detection using YOLOv5 for real-time object detection. <br/>
3. Integrated Meta's SAM model for precise food area segmentation without manual annotations. <br/>
4. Extended functionality to detect and classify packaged food items for comprehensive meal analysis. <br/>
5. Calculated nutrition values by analyzing pixel counts of segmentation masks relative to plate dimensions. <br/>

</div>
</details>

<details>
<summary><strong><code>2023</code> SWATTER — acoustic UAV detection on-device (TensorFlow Lite)</strong></summary>
<div markdown="1">

- `Link:` [GitHub](https://github.com/K-SW-SWATTER/KSW-Purdue)
- `Role:` Team Member
- `Period:` 2023 Winter (Purdue University, West Lafayette, Indiana, USA)
- `Tech Stack:` Python, TensorFlow Lite, Android (Java/Kotlin), SVM, MFCC Feature Extraction, TCP Socket Server (C++)
- `Contents:` <br/>
1. Developed a novel solution for drone detection using machine learning-based smartphone application. <br/>
2. Implemented acoustic-based UAV detection by extracting MFCC features from sound data using librosa and jlibrosa libraries. <br/>
3. Trained SVM classification model and deployed on Android devices using TensorFlow Lite Interpreter for real-time edge inference. <br/>
4. Designed TCP socket server for comparing inference time between edge computing and server-side processing. <br/>
5. Achieved practical drone detection capability using only smartphones, eliminating need for specialized equipment. <br/>

</div>
</details>

<details>
<summary><strong><code>2022</code> VegeChecker — barcode food-ingredient analysis (Android)</strong></summary>
<div markdown="1">

- `Link:` [GitHub](https://github.com/HyeonjongJang/vegechecker)
- `Role:` Team Member
- `Period:` Dongseo University Sogaesil3 Project
- `Tech Stack:` Java, Android SDK, Barcode Scanner API
- `Contents:` <br/>
1. Developed an Android application that analyzes food ingredients through barcode recognition. <br/>
2. Implemented barcode scanning functionality to retrieve product information automatically. <br/>
3. Designed user-friendly interface for quick and convenient food ingredient checking. <br/>

</div>
</details>

<br/>

**Global Programs**
----

<details>
<summary><strong><code>2023</code> Indonesia Creativity Station — smart-farm DX capstone, Bandung</strong></summary>
<div markdown="1">

- `Link:` [PNU News](https://www.pusan.ac.kr/kor/CMS/Board/Board.do?mcode=&mCode=MN114&searchID=title&searchKeyword=%EC%B0%BD%EC%9D%98%EC%B6%A9%EC%A0%84%EC%86%8C&mgr_seq=16&mode=view&mgr_seq=16&board_seq=1491753)
- `Role:` Global Engineering Volunteer
- `Partner organizations:` Pusan National University (PNU), Dongseo University, Telkom University (Indonesia)
- `Period:` 2023.08 ~ 2023.08 (12 days)
- `Contents:` <br/>
1. Multi-National Collaborative Capstone Design: Participated in a global engineering project in Bandung, Indonesia, collaborating with students from Telkom University and various Korean universities. <br/>
2. Digital Transformation (DX) for Smart Farming: Conducted on-site research at 'SEIN Farm' and proposed technical solutions leveraging ABCD (AI, Blockchain, Cloud, Data) technologies. <br/>
3. Technical Prototyping & Implementation: Contributed to the development of smart farm management solutions to enhance productivity and data accessibility. <br/>
4. Global Problem-Solving & Leadership: Facilitated cross-cultural teamwork and delivered final presentation to international evaluators. <br/>

</div>
</details>

<details>
<summary><strong><code>2022–2023</code> K-SW Square Winter Program — global SW capstone, Purdue University (USA)</strong></summary>
<div markdown="1">

- `Link:` [Dongseo University](https://uni.dongseo.ac.kr/sw/?pCode=MN1000014&mode=view&idx=1534)
- `Partner organizations:` Purdue University, IITP (Institute for Information & Communications Technology Planning & Evaluation)
- `Period:` 2022.12 ~ 2023.02 (8 weeks)
- `Contents:` <br/>
1. Participated in an intensive global SW training program at Purdue University, focusing on advanced software engineering and creative problem-solving. <br/>
2. Collaborative Capstone Project: Conducted hands-on capstone design project with Purdue University students and U.S. software industry engineers. <br/>
3. Technical Expertise: Attended specialized seminars on IoT, Machine Learning, and Robotics, while mastering Agile/Scrum methodologies. <br/>
4. Global Professionalism: Enhanced technical communication through 1:1 mentoring with local experts and interactive English-medium modules. <br/>

</div>
</details>

<details>
<summary><strong><code>2022</code> Asia Summer Program — multinational academic exchange, Josai Int'l University (Japan)</strong></summary>
<div markdown="1">

- `Link:` [Dongseo University](https://uni.dongseo.ac.kr/iec/?pCode=MN5000027&mode=view&idx=336&fbclid=IwAR1sNIK9kkcRbxH8uwcrtCgTi4sLZsbbzdrEnpvoTJVi-QCy0xhyPQHt79A)
- `Partner organizations:` Josai International University (JIU)
- `Period:` 2022.07 ~ 2022.08 (2 weeks)
- `Contents:` <br/>
1. Represented Dongseo University in a multi-national academic exchange program, engaging with peers from over 10 Asian countries. <br/>
2. Completed intensive credit-bearing coursework and delivered final group presentations in a multicultural team environment. <br/>
3. Facilitated cross-cultural dialogue and collaborative problem-solving, overcoming language barriers and diverse perspectives. <br/>
4. Enhanced global leadership and communication competencies through interactive seminars and cultural exchange sessions. <br/>

</div>
</details>

<details>
<summary><strong><code>2022</code> Global SW Education Program — IT English intensive, Univ. of the Cordilleras (Philippines)</strong></summary>
<div markdown="1">

- `Partner organizations:` University of the Cordilleras (UC), Baguio, Philippines
- `Period:` 2022.03 ~ 2022.04 (4 weeks)
- `Contents:` <br/>
1. Completed an intensive global education program to enhance professional software engineering skills and technical communication. <br/>
2. Selected based on high academic and language performance; mastered customized IT modules tailored to global industry standards. <br/>
3. Acquired 'English for IT' and 'Global Communication' skills through interactive Zoom sessions with 1:1 native tutor mentoring. <br/>
4. Earned official joint certification from Dongseo University and UC Philippines with institutional recognition (SMileage). <br/>

</div>
</details>

<details>
<summary><strong><code>2019</code> UTAR Korean Culture Experience Program — interpretation & cultural exchange, Malaysia</strong></summary>
<div markdown="1">

- `Link:` [UPM Sarawak](https://sarawak.upm.edu.my/content/south_korea_dongseo_universitys_cultural_exchange_programs-49875?L=bm)
- `Partner organizations:` University of Tunku Abdul Rahman (UTAR)
- `Period:` 2019.08 ~ 2019.08
- `Contents:` <br/>
1. Daily Interpretation Support: Provided real-time interpretation during Korean language classes and workshops for UTAR students. <br/>
2. Cultural Tour Guidance: Enhanced visits to Haeundae Beach, Bulguksa Temple, and Gameunsa Temple Site with historical explanations. <br/>
3. Cultural Experience Accompaniment: Provided safety guidance and cultural etiquette during Taekwondo demonstrations and Korean food preparation. <br/>

</div>
</details>

<details>
<summary><strong><code>2019</code> Dongseo Global English Program — one-year intensive English track</strong> 🏆 <em>Grand Award, KRW 200,000</em></summary>
<div markdown="1">

- `Link:` [UNN News](https://news.unn.net/news/articleView.html?idxno=208379)
- `Period:` 2019.03 ~ 2019.12
- `Prize:` [Grand Award](/images/DGEP.png), Dongseo University President's Award in a speech contest recognizing one-year achievements, <strong>KRW 200,000</strong>
- `Contents:` <br/>
1. Selected as a new student to cultivate talented individuals with both English and specialized skills through intensive English instruction. <br/>
2. Completed a total of 18 credits per week: Morning English classes (9 credits), Afternoon major and liberal arts classes (up to 9 credits). <br/>

</div>
</details>
