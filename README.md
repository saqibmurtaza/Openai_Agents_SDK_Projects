openai_agents_sdk_projects/                     <-- Git repo root
│
├── README.md                        
├── requirements.txt                 
├── .gitignore                       
├── project_0/                       
│   ├── agents_configs/              <-- Contains project_0 code and pyproject.toml
│   │   ├── pyproject.toml
│   │   ├── README.md                    
│   │   ├── src/
│   │   │   └── project_0/
│   │   │       ├── __init__.py
│   │   │       ├── agent_level.py
│   │   │       ├── global_level.py
│   │   │       └── run_level.py
│   │   └── tests/
│   │       └── test_agent_level.py
│
├── project_1/                       
│   └── ... (similarly structured)
│
└── scripts/                         
    └── setup_env.sh
