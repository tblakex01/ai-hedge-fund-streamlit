# PowerShell script to run Streamlit app

# Check if Streamlit is installed
$streamlitExists = Get-Command streamlit -ErrorAction SilentlyContinue
if (-not $streamlitExists) {
    Write-Error "Streamlit is not installed. Aborting."
    exit 1
}

# Activate the virtual environment
Write-Host "Activating virtual environment..."
try {
    & .\venv\Scripts\Activate.ps1
    if (-not $?) {
        throw "Failed to activate virtual environment"
    }
    Write-Host "Virtual environment activated successfully."
} catch {
    Write-Error "Failed to activate virtual environment: $_"
    exit 1
}

# Run the Streamlit app
Write-Host "Starting Streamlit app..."
streamlit run app.py
