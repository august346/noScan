# WB demand brands

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
    - [ ] weekly full scan
    - [ ] daily scan empties
    - [ ] check periodic
- [ ] web
    - [ ] dashboard
        - [ ] pagination
        - [ ] filters
        - [ ] order
    - [ ] interests
    - [ ] realtime update target