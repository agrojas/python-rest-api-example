FROM python:3.9

# install poetry
RUN pip install poetry
# copy project requirement files here to ensure they will be cached.
WORKDIR /root
ADD app/ app/
COPY docker/entrypoint.sh poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
ENV POETRY_VIRTUALENVS_IN_PROJECT true
RUN poetry install

EXPOSE 5000
# Use heroku entrypoint
CMD ["bash", "entrypoint.sh"]
