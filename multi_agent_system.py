import os
from typing import TypedDict, Dict, Any

import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

# State Definition

class RecipeState(TypedDict):
    """
    The shared state dictionary that gets passed along the graph nodes.
    Each node (agent) updates specific keys.
    """
    ingredients: str
    dietary_preferences: str
    recipe_title: str
    recipe_instructions: str
    nutrition_info: str
    grocery_list: str
    final_output: str

# Agent Initialization
# Initialize the Groq model
try:
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)
except Exception as e:
    print(f"Error initializing LLM. Did you set GROQ_API_KEY? Error: {e}")
    llm = None

# Agent Node Functions

def head_chef_node(state: RecipeState):
    print("-> Head Chef Agent is brainstorming a recipe...")
    sys_msg = SystemMessage(content="You are a Master Chef. Create a creative recipe title and step-by-step instructions. Only return the title on the first line, and the instructions below it.")
    user_msg = HumanMessage(content=f"Ingredients available: {state['ingredients']}. Dietary Preferences: {state['dietary_preferences']}.")
    
    if llm:
        response = llm.invoke([sys_msg, user_msg]).content
        # Simple string splitting for title and instructions
        parts = response.split('\n', 1)
        state['recipe_title'] = parts[0].strip()
        state['recipe_instructions'] = parts[1].strip() if len(parts) > 1 else ""
    return state

def nutritionist_node(state: RecipeState):
    print("-> Nutritionist Agent is estimating calories and macros...")
    sys_msg = SystemMessage(content="You are a Nutritionist. Estimate the calories, protein, carbs, and fat for the given recipe. Add a 1-sentence health tip. Keep it brief.")
    user_msg = HumanMessage(content=f"Recipe: {state['recipe_title']}\nInstructions: {state['recipe_instructions']}")
    
    if llm:
        state['nutrition_info'] = llm.invoke([sys_msg, user_msg]).content
    return state

def pantry_assistant_node(state: RecipeState):
    print("-> Pantry Assistant Agent is making a grocery list...")
    sys_msg = SystemMessage(content="You are a Pantry Assistant. Look at the recipe and the user's initial ingredients. List the missing standard items they might need to buy (like specific oils, spices, or garnishes). Output as a bulleted list.")
    user_msg = HumanMessage(content=f"User Ingredients: {state['ingredients']}\nRecipe: {state['recipe_title']}\nInstructions: {state['recipe_instructions']}")
    
    if llm:
        state['grocery_list'] = llm.invoke([sys_msg, user_msg]).content
    return state

def food_critic_node(state: RecipeState):
    print("-> Food Critic Agent is formatting the final review...")
    # Formatting everything nicely into Markdown
    final_markdown = f"""
# {state.get('recipe_title', 'Untitled Recipe')}

### Ingredients Provided
{state.get('ingredients', 'None')}
**(Dietary: {state.get('dietary_preferences', 'None')})**

---
### Chef's Instructions
{state.get('recipe_instructions', 'No instructions found.')}

---
### Nutritional Estimates
{state.get('nutrition_info', 'No nutrition info found.')}

---
### Pantry Groceries to Buy
{state.get('grocery_list', 'No missing ingredients found.')}
"""
    state['final_output'] = final_markdown.strip()
    return state

# PHASE 5: Graph Routing and Compilation
# Initialize the graph
workflow = StateGraph(RecipeState)

# Add our 4 nodes
workflow.add_node("chef", head_chef_node)
workflow.add_node("nutritionist", nutritionist_node)
workflow.add_node("pantry", pantry_assistant_node)
workflow.add_node("critic", food_critic_node)

# Add edges to enforce a strict sequential workflow
workflow.add_edge(START, "chef")
workflow.add_edge("chef", "nutritionist")
workflow.add_edge("nutritionist", "pantry")
workflow.add_edge("pantry", "critic")
workflow.add_edge("critic", END)

# Compile the final multi-agent application
app = workflow.compile()

# PHASE 6: Main Execution Loop (Streamlit UI)
def main():
    st.set_page_config(page_title="AI Recipe Generator", page_icon="👨‍🍳")
    
    st.title("Multi-Agent AI Recipe Generator")
    st.markdown("Enter your available ingredients, and our team of AI agents (Chef, Nutritionist, Pantry Assistant, and Critic) will create a complete recipe plan for you!")
    
    with st.sidebar:
        st.header("Your Ingredients")
        ingredients = st.text_area("What do you have in your fridge?", "Chicken, rice, eggs", height=100)
        dietary_prefs = st.text_input("Dietary preferences/allergies?", "None")
        generate_btn = st.button("Generate Recipe", type="primary")

    if generate_btn:
        if not ingredients.strip():
            st.error("Please enter some ingredients!")
            return
            
        # Initialize the starting state
        initial_state = RecipeState(
            ingredients=ingredients,
            dietary_preferences=dietary_prefs,
            recipe_title="",
            recipe_instructions="",
            nutrition_info="",
            grocery_list="",
            final_output=""
        )
        
        with st.spinner("Our AI Agents are cooking... (This depends on the model's speed)"):
            try:
                # Run the graph
                final_state = app.invoke(initial_state)
                st.success("Recipe generated successfully!")
                
                # Display the final output
                st.markdown(final_state.get('final_output', 'No final output generated.'))
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
