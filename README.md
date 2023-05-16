# generate knowledge graph used to forecast stocks
주식 예측에 사용되는 knowledge graph 생성


## 프로젝트 소개
wikidata의 정보를 이용하여 주식 예측 프로그램에 이용되는 graph를 생성한다.

### 개발 환경
- python
- Neo4j
- wikidata query

## 파일 설명
### file_arrange.ipynb
first order와 second order에서 사용되는 wikidata relation을 graph 생성에 적용하기 좋게 csv 파일로 만든다.  

### history.ipynb
각각의 timestamp에 따라 과거 wikidata 페이지에서 웹 크롤링을 한다.(이때 wikidata query 사용) 그 후 neo4j를 활용하여 graph 구축
-> 과거 graph를 학습하여 미래 graph 예측에 사용

### main.ipynb
현재 wkidata page에서 웹 크롤링 하여 neo4j 에서 graph 구축 -> dynamic graph 생성에 활용
