# Project Description

## FastAPI application that allow users report a bug and track status of reported bug. Users can:

* Report a bug
* Track reported bug
* Developers can work on bug

![Static Badge](https://img.shields.io/badge/FastAPI-0.116.1-green?color=%23006400)
![Static Badge](https://img.shields.io/badge/Python-3.13-green?color=%23006400)

# Steps to run and test endpoints

## 1. Clone repo

```shell
git clone https://github.com/Samson23-ux/Bug-Tracker.git
```

## 2. Create enviroment

```shell
python -m venv venv
```

## 3. Activate enviroment

```shell
venv\Scripts\activate or source venv/bin/activate (for apple)
```

## 4. Run Server

```shell
uvicorn app.main:main --reload
```

## 5. Test Endpoints

```shell
run http://localhost:8000/docs on browser
```
