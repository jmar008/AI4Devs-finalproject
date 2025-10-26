# Imagen base con Python y Node.js
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Instalar dependencias del sistema
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    build-essential \
    postgresql-client \
    libpq-dev \
    python3-dev \
    python3-pip \
    python3-venv \
    curl \
    git \
    vim \
    nano \
    wget \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Instalar Node.js 18 LTS
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Instalar herramientas globales de Node
RUN npm install -g \
    pnpm \
    yarn \
    typescript \
    ts-node \
    @nestjs/cli \
    vercel \
    eslint \
    prettier

# Instalar Python y herramientas (usar entorno virtual para evitar PEP 668)
RUN python3 -m venv /opt/python-dev \
    && /opt/python-dev/bin/pip install --upgrade pip setuptools wheel

# Instalar herramientas de desarrollo Python en el entorno virtual
RUN /opt/python-dev/bin/pip install \
    black \
    isort \
    flake8 \
    pylint \
    mypy \
    pytest \
    pytest-cov \
    ipython \
    ipdb \
    django-extensions \
    django-debug-toolbar

# Configurar PATH para usar el entorno virtual
ENV PATH="/opt/python-dev/bin:$PATH"

# Configurar usuario vscode
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Crear usuario si no existe
RUN if ! id -u $USERNAME > /dev/null 2>&1; then \
    groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME; \
    fi

# Configurar workspace
WORKDIR /workspace

# Cambiar al usuario vscode
USER $USERNAME

# Configurar Git
RUN git config --global init.defaultBranch main

CMD ["/bin/bash"]
