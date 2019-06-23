# Brunch Article Recommendation
브런치 글 추천 대회 참가자에게 제공되는 예제 코드입니다. 간단한 추천 모델과 평가 코드가 포함되어 있습니다. (데이터셋이 `./res` 이외에 위치한 경우는 `config.py`를 수정하세요)
```bash
$> tree -d
.
├── res
│   ├── contents
│   ├── predict
│   └── read
└── tmp
```

1. 데이터 분할
학습과 개발 데이터를 나누기 위해 아래와 같이 실행합니다.
```bash
$> python database.py groupby 2018100100 2019022200 ./tmp/ ./tmp/train
$> python database.py groupby 2019022200 2019030100 ./tmp/ ./tmp/dev
```
- 18.10.01부터 19.02.22일까지 학습 데이터로 사용하고, 19.02.22 이후 데이터는 내부 평가 데이터로 사용합니다.
- 만약 메모리 부족 에러가 발생시 --num-chunks 값을 10보다 더 큰 값으로 지정하세요.
- **주의** 평가시 사용하게될 데이터와는 다르게 여기서 분할한 데이터에는 한 사용자가 본 데이터가 학습과 평가 데이터에 모두 등장할 수도 있습니다.

개발 과정에서 평가할 사용자 리스트를 추출합니다.
```bash
$> python database.py sample_users ./tmp/dev ./tmp/dev.users --num-users=100
```

2. 모델 생성 및 추천 결과 생성
mostpopular.py에는 특정 기간 동안 가장 많이 본 글을 모두에게 추천하는 간단한 로직입니다. 내부 평가 데이터에서 추출한 100명의 사용자에게 2019년 02월 15일부터 2019년 02월 22일전까지 가장 인기가 좋았던 글을 추천하는 결과는 아래와 같이 생성할 수 있습니다.


```bash
$> python mostpopular.py --from-dtm 2019020100 --to-dtm 2019022200 recommend ./tmp/dev.users ./tmp/dev.users.recommend
```

3. 평가
생성된 추천 결과는 아래 커맨드로 평가할 수 있습니다.
```
$> python evaluate.py run ./tmp/dev.users.recommend ./tmp/dev --topn=100
```

4. 제출하기
위와 동일한 방법으로 predict/dev.users에 대한 추천 결과를 생성해 아레나 홈페이지에 결과를 제출하는 방식은 아래와 같습니다.

```
$> python mostpopular.py --from-dtm 2019020100 --to-dtm 2019030100 recommend ./res/predict/dev.users recommend.txt
```
- 19.02.01 부터 19.03.01 일까지 가장 인기가 좋았던 글 100개로 추천 결과를 생성합니다.

recommend.txt 파일과 소스코드를 각각 zip으로 압축한 뒤에 홈페이지로 제출하시면 점수를 확인하실 수 있습니다. 
