ARG USERNAME=devuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

FROM python:3.11-bookworm

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    build-essential ca-certificates curl dumb-init git gnupg iputils-ping nano sudo wget && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo \
        "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
        "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" > \
        /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    apt-get clean

ARG USERNAME USER_UID USER_GID

RUN groupadd -g ${USER_GID} ${USERNAME} && useradd -m -u ${USER_UID} -g ${USERNAME} -s /bin/bash ${USERNAME} && adduser ${USERNAME} sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >>/etc/sudoers

USER ${USERNAME}
WORKDIR /home/${USERNAME}
ENV USER=${USERNAME} SHELL=/bin/bash

RUN python3.11 -m venv /home/${USERNAME}/venv
ENV PATH=/home/${USERNAME}/venv/bin:/opt/python/cp311-cp311/bin:${PATH}

RUN pip3 install --upgrade pip setuptools wheel

COPY --chown=${USERNAME} requirements.txt /usr/src/lua-eval-server/requirements.txt
COPY --chown=${USERNAME} requirements-dev.txt /usr/src/lua-eval-server/requirements-dev.txt
WORKDIR /usr/src/lua-eval-server

RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements-dev.txt

ENTRYPOINT [ "/usr/bin/dumb-init" ]
CMD [ "/usr/bin/env", "bash" ]
