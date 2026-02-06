import streamlit as st
import asyncio
import os
import sys
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.mcp import MCPClient

st.set_page_config(page_title="Project Chimera | MCP Dashboard", layout="wide")

st.title("🔌 MCP Server Inspector")

# Sidebar for configuration
st.sidebar.header("Configuration")
config_path = st.sidebar.text_input("Config Path", value=".cursor/mcp.json")

# Initialize Client in Session State
if 'mcp_tools' not in st.session_state:
    st.session_state['mcp_tools'] = None
if 'server_status' not in st.session_state:
    st.session_state['server_status'] = "Disconnected"

async def connect_and_fetch():
    try:
        # Resolve absolute path
        abs_config_path = os.path.join(os.getcwd(), config_path)
        if not os.path.exists(abs_config_path):
            st.error(f"Config file not found at: {abs_config_path}")
            return

        client = MCPClient(config_path=abs_config_path)
        
        # Load config to get server names
        with open(abs_config_path, 'r') as f:
            config = json.load(f)
        
        server_names = list(config.get('mcpServers', {}).keys())
        
        if not server_names:
            st.warning("No servers found in config.")
            return
            
        # For this demo, just connect to the first one or specific 'tenxfeedbackanalytics'
        target_server = "tenxfeedbackanalytics" if "tenxfeedbackanalytics" in server_names else server_names[0]
        
        with st.spinner(f"Connecting to {target_server}..."):
            await client.connect(target_server)
            st.session_state['server_status'] = f"Connected to {target_server}"
            
            tools_response = await client.list_tools()
            st.session_state['mcp_tools'] = tools_response.tools
            
            await client.close()
            
    except Exception as e:
        st.error(f"Connection Failed: {str(e)}")
        st.session_state['server_status'] = "Error"

# Main Action Button
if st.button("Check Connection & List Tools"):
    asyncio.run(connect_and_fetch())

# Display Status
st.metric("Status", st.session_state['server_status'])

# Display Tools
if st.session_state['mcp_tools']:
    st.header("🛠️ Available Tools")
    
    for tool in st.session_state['mcp_tools']:
        with st.expander(f"**{tool.name}**"):
            st.markdown(f"_{tool.description}_")
            st.code(json.dumps(tool.inputSchema, indent=2), language='json')

elif st.session_state['server_status'] == "Connected":
    st.info("No tools found on this server.")
