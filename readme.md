# WB demand brands

## requirements
python 3.10

## run

```commandline
docker-compose up -d
celery -A celery_tasks worker --loglevel=INFO -B -E
uvicorn backend.main:app --reload
```


## TODO

- [x] split backend and celery
- [ ] config docker
- [ ] celery
    - [ ] proxy
    - [x] weekly full scan
    - [x] daily scan empties
    - [x] check periodic
- [ ] backend
    - [ ] dashboard
        - [ ] pagination
        - [ ] filters
        - [ ] order
    - [ ] interests
    - [ ] realtime update target
- [ ] front