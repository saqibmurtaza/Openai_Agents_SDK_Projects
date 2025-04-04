openai-projects/                     <-- Main Git repository root
│
├── README.md                        <-- Overview of all projects
├── requirements.txt                 <-- Common dependencies (if any)
├── .gitignore                       <-- Ignore unwanted files globally
├── project_0/                       <-- First OpenAI project
│   ├── src/
│   │   └── project_0/
│   │       ├── __init__.py
│   │       ├── agent_level.py
│   │       ├── global_level.py
│   │       └── run_level.py
│   ├── README.md                    <-- Description of project_0
│   ├── requirements.txt             <-- Specific dependencies
│   └── tests/
│       └── test_agent_level.py
│
├── project_1/                       <-- Next OpenAI project
│   ├── src/
│   │   └── project_1/
│   │       ├── __init__.py
│   │       ├── core.py
│   │       └── utils.py
│   ├── README.md
│   ├── requirements.txt
│   └── tests/
│       └── test_core.py
│
└── scripts/                         <-- Optional: helper scripts (shared)
    └── setup_env.sh
