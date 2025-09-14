#!/bin/bash

# Nephro API Backend Service Startup Script
# This script starts the Nephrology AI Agent API server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_PORT=8002
API_HOST="0.0.0.0"
API_FILE="nephro_api.py"
ENV_FILE=".env"
REQUIREMENTS_FILE="requirements.txt"

echo -e "${BLUE}=== Nephro API Backend Service Startup ===${NC}"
echo -e "${BLUE}Script Directory: ${SCRIPT_DIR}${NC}"
echo -e "${BLUE}Timestamp: $(date)${NC}"
echo ""

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to kill process on port
kill_port_process() {
    local port=$1
    echo -e "${YELLOW}Killing existing process on port $port...${NC}"
    local pid=$(lsof -ti:$port)
    if [ ! -z "$pid" ]; then
        kill -9 $pid
        sleep 2
        echo -e "${GREEN}Process killed successfully${NC}"
    fi
}

# Change to script directory
cd "$SCRIPT_DIR"

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${RED}Error: $ENV_FILE file not found!${NC}"
    echo -e "${YELLOW}Please copy .env.example to .env and configure your API keys${NC}"
    exit 1
fi

# Check if API file exists
if [ ! -f "$API_FILE" ]; then
    echo -e "${RED}Error: $API_FILE not found!${NC}"
    exit 1
fi

# Check if requirements file exists
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo -e "${YELLOW}Warning: $REQUIREMENTS_FILE not found${NC}"
else
    echo -e "${BLUE}Installing/updating Python dependencies...${NC}"
    pip install -r "$REQUIREMENTS_FILE" --quiet
    echo -e "${GREEN}Dependencies installed successfully${NC}"
fi

# Check if port is already in use
if check_port $API_PORT; then
    echo -e "${YELLOW}Port $API_PORT is already in use${NC}"
    read -p "Do you want to kill the existing process and restart? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill_port_process $API_PORT
    else
        echo -e "${RED}Startup cancelled${NC}"
        exit 1
    fi
fi

# Load environment variables
echo -e "${BLUE}Loading environment variables...${NC}"
source "$ENV_FILE" 2>/dev/null || echo -e "${YELLOW}Warning: Could not source .env file${NC}"

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" = "your-api-key-here" ]; then
    echo -e "${RED}Error: GEMINI_API_KEY is not properly configured in $ENV_FILE${NC}"
    echo -e "${YELLOW}Please set a valid Google Gemini API key${NC}"
    exit 1
fi

echo -e "${GREEN}Environment configuration validated${NC}"
echo ""

# Start the API server
echo -e "${BLUE}Starting Nephro API Backend Service...${NC}"
echo -e "${BLUE}Host: $API_HOST${NC}"
echo -e "${BLUE}Port: $API_PORT${NC}"
echo -e "${BLUE}API File: $API_FILE${NC}"
echo ""

# Method 1: Direct Python execution
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo -e "${RED}Error: Python not found in PATH${NC}"
    exit 1
fi

echo -e "${GREEN}Using Python command: $PYTHON_CMD${NC}"
echo -e "${GREEN}Starting server...${NC}"
echo ""
echo -e "${YELLOW}=== API Server Output ===${NC}"

# Start the server with error handling
trap 'echo -e "\n${RED}Server interrupted${NC}"; exit 1' INT TERM

# Option 1: Direct Python execution
if [ "$1" = "--direct" ]; then
    echo -e "${BLUE}Starting with direct Python execution...${NC}"
    $PYTHON_CMD "$API_FILE"
else
    # Option 2: Using uvicorn (recommended)
    if command -v uvicorn >/dev/null 2>&1; then
        echo -e "${BLUE}Starting with uvicorn (recommended)...${NC}"
        uvicorn nephro_api:app --host "$API_HOST" --port "$API_PORT" --reload
    else
        echo -e "${YELLOW}uvicorn not found, installing...${NC}"
        pip install uvicorn --quiet
        echo -e "${BLUE}Starting with uvicorn...${NC}"
        uvicorn nephro_api:app --host "$API_HOST" --port "$API_PORT" --reload
    fi
fi