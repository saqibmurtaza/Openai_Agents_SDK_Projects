MODULAR APPROACH:
Files	            Responsibilities
shopping_agents.py	Agent + tools definition
config_agents.py	Model setup + RunConfig
app.py (Chainlit)	Chat UI loop, message handling

HOW TO RUN THE PROJECT:
1: chainlit run app.py or
2: uv run project-2 or
3: python shopping_agents.py (go to dir where this file locate)

UV COMMANDS:
1: uv run <project name>
2: uv venv
3: uv pip install -e .
4: uv add <package name>
5: uv clean (clean the cache)
6: uv pip uninstall <package name>
7: uv pip show <package name>