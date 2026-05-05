ARG PYTHON_VERSION=3.11.11-alpine

FROM python:${PYTHON_VERSION} AS base

ARG APP_HOME=/code
ARG APP_DOCKER=/docker

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=/code

ENV UV_PROJECT_ENVIRONMENT=/venv

ENV TZ=America/Maceio
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR $APP_HOME

FROM base AS compiler

RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
        make \
        postgresql-dev \
        build-base \
        python3-dev \
        musl-dev \
        unixodbc-dev \
        curl

RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv

COPY . .

RUN uv sync --no-dev --frozen

RUN apk del .build-deps \
    && rm -rf /root/.cache /tmp/*

FROM base

RUN apk add --no-cache \
    make \
    postgresql-libs

COPY --from=compiler /venv /venv
COPY --from=compiler /code /code

COPY ./docker/entrypoint/entrypoint.sh /entrypoint/entrypoint.sh

RUN chmod +x /entrypoint/entrypoint.sh

ENV PYTHONPATH=src

ENTRYPOINT ["/entrypoint/entrypoint.sh"]
