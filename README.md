# Billing

## Stack

- Python
- FastAPI
- PostgreSQL

Keep all data in two tables: wallet, transaction

### Pros:
- Every transaction has uuid, in case of double http request
- No deadlock in case with 2 cyclic transactions

### Cons:
 - Slow access to wallet transaction history(no index)
 - System may be deadlocked in case with 3 or more cyclic transactions

## Tests
```docker-compose -f ./docker-compose-test.yaml up --build --abort-on-container-exit --exit-code-from test```

## Run api
`docker-compose up --build`

## Docs
http://127.0.0.1:8080/docs
