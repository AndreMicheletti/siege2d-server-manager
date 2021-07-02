
# LOCAL DEVELOPMENT

local:
	docker run -p 5000:5000 siege2d_matchmaker

# BUILDING

build:
	docker build -t siege2d_matchmaker .

# DEPLOYING

# warning: your shell docker must be out of kubectl context (open a new terminal or check $DOCKER_HOST)
deploy: build
	docker tag siege2d_matchmaker gcr.io/effective-relic-318403/siege2d_matchmaker
	docker push gcr.io/effective-relic-318403/siege2d_matchmaker
