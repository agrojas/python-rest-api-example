FROM python:3.9


# Install Heroku GPG dependencies
RUN apt-get install -y gpg apt-transport-https gpg-agent curl ca-certificates

# Add Datadog repository and signing keys
ENV DATADOG_APT_KEYRING="/usr/share/keyrings/datadog-archive-keyring.gpg"
ENV DATADOG_APT_KEYS_URL="https://keys.datadoghq.com"
RUN sh -c "echo 'deb [signed-by=${DATADOG_APT_KEYRING}] https://apt.datadoghq.com/ stable 7' > /etc/apt/sources.list.d/datadog.list"
RUN touch ${DATADOG_APT_KEYRING}
RUN curl -o /tmp/DATADOG_APT_KEY_CURRENT.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_CURRENT.public" && \
    gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_CURRENT.public
RUN curl -o /tmp/DATADOG_APT_KEY_F14F620E.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_F14F620E.public" && \
    gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_F14F620E.public
RUN curl -o /tmp/DATADOG_APT_KEY_382E94DE.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_382E94DE.public" && \
    gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_382E94DE.public
# Install the Datadog agent
RUN apt-get update && apt-get -y --force-yes install --reinstall datadog-agent

# install poetry
RUN pip install poetry
# copy project requirement files here to ensure they will be cached.
WORKDIR /root
ADD app/ app/

COPY heroku/heroku-entrypoint.sh poetry.lock pyproject.toml alembic.ini ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
ENV POETRY_VIRTUALENVS_IN_PROJECT true

RUN poetry install

# Expose app port
EXPOSE 5000

# Expose DogStatsD and trace-agent ports
EXPOSE 8125/udp 8126/tcp
ENV DD_APM_ENABLED=true


# Copy Datadog configuration
COPY heroku/datadog-config/ /etc/datadog-agent/
# Use heroku entrypoint
CMD ["bash", "heroku-entrypoint.sh"]