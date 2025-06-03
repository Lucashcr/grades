import uvicorn


def run_dev():
    uvicorn.run("grades.application.app:app", reload=True)


if __name__ == "__main__":
    run_dev()
