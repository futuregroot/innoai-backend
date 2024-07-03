# InnoAI Backend

## Overview

The InnoAI Backend is a Python-based web application. This README provides instructions for setting up the environment, installing dependencies, and running the application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Environment](#setup-environment)
- [Install Dependencies](#install-dependencies)
- [Run Application](#run-application)
- [Additional Information](#additional-information)
  
## Prerequisites

Before you begin, ensure you have the following installed:

- [Anaconda](https://www.anaconda.com/products/individual) (or Miniconda)
  
## Setup Environment

1. **Create a Conda environment:**

    ```sh
    conda create --name innoai_backend python=3.11
    ```

2. **Activate the environment:**

    ```sh
    conda activate innoai_backend
    ```

## Install Dependencies

1. **Install pip:**

    ```sh
    conda install pip
    ```

2. **Install the required Python packages:**

    ```sh
    pip install -r requirements.txt
    ```

## Run Application

1. **Run the application:**

    ```sh
    local : ENV=local python server.py
    dev : ENV=development python server.py
    local : ENV=production python server.py
    ```

    The server should now be running at `http://localhost:5000`.

## Additional Information

- Ensure that the environment variables are properly set. You can use an `.env` file for this purpose.
- To deactivate the conda environment, use:

    ```sh
    conda deactivate
    ```

## Using PyCharm

To use this project in PyCharm:

1. **Open PyCharm** and select **Open** to open the project directory.
2. **Set the Python interpreter**:
    - Go to `File` > `Settings` (or `PyCharm` > `Preferences` on macOS).
    - Select `Project: innoai_backend` > `Python Interpreter`.
    - Click the gear icon and select `Add`.
    - Choose `Conda Environment` and select the existing `innoai_backend` environment.
3. **Install dependencies**:
    - Open the terminal in PyCharm.
    - Ensure the `innoai_backend` environment is activated.
    - Run the commands listed above to install dependencies.

4. **Run the application**:
    - Ensure `server.py` is your entry-point script.
    - Right-click on `server.py` and select `Run 'server'`.

## Credits

Wolverine

## API Call in postman 
1. **Call CSRF Token api**
2. **For Calling API, add X-CSRFToken in the headers and {CSRF_TOKEN} in the value**

## Application Structure

innoai-backend/
│
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── local.py
│   │   └── prod.py
│   │
│   ├── extensions/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── cache.py
│   │   ├── chroma_db.py
│   │   ├── cors.py
│   │   ├── csrf.py
│   │   └── db.py
│   │   └── limiter.py
│   │
│   ├── routes/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── ingestion.py
│   │   │   └── tests.py
│   │   │
│   │   ├── auth/
│   │   │   └── __init__.py
│   │   │
│   │   └──pages/
│   │       ├── __init__.py
│   │       └── core.py
│   │
│   └── services/
│       ├── answer_gpt_service.py
│       ├── answer_llama_service.py
│       ├── split_gpt_service.py
│       ├── split_llama_service.py
│       └── ingestion_service.py
│
├── chroma_storage/
│   └── vehicle_collection/
│       └── 2afe62fc-154e-43f8-b717-511a21725fe0
│            ├── data_level0.bin
│            ├── header.bin
│            ├── length.bin
│            └── link_lists.bin
│   
├── .env
├── .env.dev
└── .env.local

innoai-backend/
│
├── app/
│
├── config/
│   ├── __init__.py
│   ├── base.py
│   ├── dev.py
│   ├── local.py
│   └── prod.py
│
├── extensions/
│   ├── __init__.py
│   ├── auth.py
│   ├── cache.py
│   ├── chroma_db.py
│   ├── cors.py
│   ├── csrf.py
│   ├── db.py
│   └── limiter.py
│
├── routes/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── ingestion.py
│   │   └── tests.py
│   ├── auth/
│   │   └── __init__.py
│   └── pages/
│       ├── __init__.py
│       └── core.py
│
├── services/
│   ├── answer_gpt_service.py
│   ├── answer_llama_service.py
│   ├── split_gpt_service.py
│   ├── split_llama_service.py
│   └── ingestion_service.py
│
├── chroma_storage/
│   └── vehicle_collection/
│       └── 2afe62fc-154e-43f8-b717-511a21725fe0/
│           ├── data_level0.bin
│           ├── header.bin
│           ├── length.bin
│           └── link_lists.bin
│
├── .env
├── .env.dev
└── .env.local


## Explanation of `chroma_storage` Directory Structure

### `vehicle_collection/2afe62fc-154e-43f8-b717-511a21725fe0`

This directory represents a specific collection within `chroma_storage`. Below are explanations of the files contained within this directory:

- **`data_level0.bin`**: This file stores the data records within the collection. Each record is stored in binary format, containing the actual data of the collection.

- **`header.bin`**: Contains metadata related to the collection. It includes information about the schema, index structure, and field definitions that define the database structure.

- **`length.bin`**: Manages the lengths of individual data records stored in data level 0. Efficiently managing the length of each data record improves data retrieval and management performance.

- **`link_lists.bin`**: Contains link list information that maintains relationships between data records. This file is used to manage complex relationships between data records.

These files provide essential components for storing and managing data efficiently within `chroma_storage`.










This project is developed and maintained by Wondermove Inc.

