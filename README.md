# Piper TTS

## Installation

### Step 1: Set Up Virtual Environment

create a virtual environment using `venv`:

```bash
python -m venv venv
```

### Step 2: Activate the Virtual Environment

Activate the virtual environment. Note that the command might differ based on your operating system.

For Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### Step 2: Install Requirements

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

```bash
sudo apt install rubberband-cli
```

## Usage

With the virtual environment activated, you can now run the UVicorn server. Use the following command:

```bash
uvicorn src.python_run.piper.test:app --reload
```

Now you can access the server on
http://127.0.0.1:8000/docs

This command starts the Uvicorn server with automatic reloading enabled, so any changes you make to the code will automatically trigger a server restart.
