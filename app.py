import streamlit as st
import asyncio
from datetime import datetime
import plotly.graph_objects as go
from agents.coordinator import CoordinatorAgent
from utils.visualization import create_interactive_agent_visualization

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_visualization' not in st.session_state:
    st.session_state.show_visualization = False
if 'current_chat' not in st.session_state:
    st.session_state.current_chat = []

def format_chat_history(chat_item):
    """Format a chat history item for display"""
    return {
        "role": "user" if chat_item["is_user"] else "assistant",
        "content": chat_item["message"],
        "timestamp": chat_item["timestamp"],
        "sources": chat_item.get("sources", [])
    }

def display_chat_message(message, is_user=False):
    """Display a chat message with proper formatting"""
    with st.chat_message("user" if is_user else "assistant"):
        st.write(message["message"])
        if not is_user and "sources" in message:
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.markdown(f"""
                    🔍 **{source['title']}**
                    
                    💡 {source['snippet']}
                    
                    🔗 [Read more]({source['link']})
                    ___
                    """)
        st.caption(f"Sent at {message['timestamp']}")

async def process_query(query: str):
    """Process the query and update UI in real-time"""
    coordinator = CoordinatorAgent()
    
    try:
        with st.spinner('Agents are working on your query...'):
            result = await coordinator.coordinate_search(query)
            
            if 'error' in result:
                st.error(f"An error occurred: {result['error']}")
                return None
            
            # Format the response using the same structure as chat history
            response = {
                "is_user": False,
                "message": result['combined_answer'],
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "sources": result.get('google_result', {}).get('sources', [])
            }
            
            # Add to chat history
            st.session_state.chat_history.append({
                "is_user": True,
                "message": query,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.session_state.chat_history.append(response)
            
            return response
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    st.title("🤖 Multi-Agent Search Assistant")
    st.write("Ask anything! Our agents will search Wikipedia and the web for answers.")
    
    # Sidebar with enhanced features
    with st.sidebar:
        st.header("Settings")
        show_viz = st.toggle("Show Agent Visualization", value=st.session_state.show_visualization)
        if show_viz != st.session_state.show_visualization:
            st.session_state.show_visualization = show_viz
        
        if st.session_state.show_visualization:
            st.plotly_chart(create_interactive_agent_visualization())
        
        # Chat history controls
        st.header("Chat History")
        if st.button("Clear History"):
            st.session_state.chat_history = []
            st.rerun()
        
        # Download chat history
        if st.session_state.chat_history:
            if st.button("Download Chat History"):
                chat_text = "\n\n".join([
                    f"{'User' if msg['is_user'] else 'Assistant'} ({msg['timestamp']}):\n{msg['message']}"
                    for msg in st.session_state.chat_history
                ])
                st.download_button(
                    label="Save as Text",
                    data=chat_text,
                    file_name="chat_history.txt",
                    mime="text/plain"
                )
    
    # Display chat history
    for message in st.session_state.chat_history:
        display_chat_message(message, message["is_user"])
    
    # Chat input
    query = st.chat_input("Enter your question...")
    if query:
        response = asyncio.run(process_query(query))
        if response:
            display_chat_message(response)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Multi-Agent Search Assistant",
        page_icon="🤖",
        layout="wide"
    )
    main() 