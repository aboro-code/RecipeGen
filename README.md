# Multi-Agent AI Recipe Generator

This project is a multi-agent AI system built using LangChain and LangGraph. It takes a user's available ingredients and dietary restrictions to generate a complete recipe, nutritional estimates, and a missing grocery list through the collaboration of four specialized AI agents.

## Architecture

The system utilizes a sequential LangGraph workflow with a shared state. The agents (nodes) include:
1. **Head Chef Agent**: Brainstorms the recipe and provides cooking instructions.
2. **Nutritionist Agent**: Estimates calories and macronutrients based on the Chef's recipe.
3. **Pantry Assistant Agent**: Cross-references the recipe with the user's initial ingredients to generate a grocery list.
4. **Food Critic Agent**: Compiles the data into a formatted markdown output.

The application uses the Groq API (Llama 3.1) for fast inference and Streamlit for the frontend user interface.

## Local Setup and Installation

Follow these steps to run the project locally.

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone <your-repository-url>
cd RecipeGen
```

### 2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies:

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install the required packages using pip:
```bash
pip install langchain langgraph langchain-groq streamlit
```

### 4. Set the API Key
This project requires a free Groq API key. You can get one at console.groq.com. 
Once you have the key, set it as an environment variable in your terminal:

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

**Mac/Linux:**
```bash
export GROQ_API_KEY="your_api_key_here"
```

### 5. Run the Application
Start the Streamlit graphical interface:
```bash
streamlit run multi_agent_system.py
```

This command will automatically open a local server in your default web browser where you can interact with the AI agents.
