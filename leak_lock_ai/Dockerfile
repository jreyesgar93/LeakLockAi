FROM python:3.8 as base

WORKDIR /home/leak_lock_ai

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt


# development image.
FROM base as development

COPY requirements_dev.txt requirements_dev.txt

RUN pip install -r requirements_dev.txt
ENV MODE=development


# testing image.
FROM base as testing

RUN pip install pytest && pip install requests


# production image.
FROM base as production

WORKDIR /production

COPY . .

ARG PORT=80
ARG HOST=0.0.0.0
ARG APP_MODULE=leak_lock_ai.main:app
ARG WORKERS_PER_CORE=1

ENV MODE=production
ENV APP_MODULE=${APP_MODULE}
ENV WORKERS_PER_CORE=${WORKERS_PER_CORE}}
ENV HOST=${HOST}
ENV PORT=${PORT}

EXPOSE ${PORT}

ENTRYPOINT [ "./scripts/start.sh" ]
