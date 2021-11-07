# WB demand brands

## requirements
python 3.10

## run

```commandline
docker-compose up -d
celery -A celery_tasks worker --loglevel=INFO -B -E
```


## TODO

- [ ] split web and celery
- [ ] config docker
- [ ] celery
    - [ ] proxy
    - [x] weekly full scan
    - [x] daily scan empties
    - [x] check periodic
- [ ] web
    - [ ] dashboard
        - [ ] pagination
        - [ ] filters
        - [ ] order
    - [ ] interests
    - [ ] realtime update target