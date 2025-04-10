FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

RUN apt-get update && \
    apt-get install -y xvfb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV DISPLAY=:99
WORKDIR /var/task

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir awslambdaric

COPY . .

ENTRYPOINT ["python", "-m", "awslambdaric"]
CMD ["app.lambda_handler"]