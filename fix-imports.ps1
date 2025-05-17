# PowerShell script to fix imports in Python files
$baseDir = "d:\ai_apps\modelcontextprotocol\testing\ai-hedge-fund\src"
$agentsDir = Join-Path $baseDir "agents"
$graphDir = Join-Path $baseDir "graph"

# Define the import replacements
$replacements = @(
    @{From = "from graph.state"; To = "from src.graph.state"},
    @{From = "from tools.api"; To = "from src.tools.api"},
    @{From = "from utils.progress"; To = "from src.utils.progress"},
    @{From = "from utils.llm"; To = "from src.utils.llm"},
    @{From = "from utils.display"; To = "from src.utils.display"},
    @{From = "from utils.analysts"; To = "from src.utils.analysts"},
    @{From = "from utils.visualize"; To = "from src.utils.visualize"},
    @{From = "import agents."; To = "import src.agents."},
    @{From = "from agents."; To = "from src.agents."},
    @{From = "import graph."; To = "import src.graph."},
    @{From = "from llm."; To = "from src.llm."}
)

# Function to fix imports in a file
function Fix-Imports {
    param (
        [string]$filePath
    )
    
    $content = Get-Content $filePath -Raw
    $changed = $false
    
    foreach ($replacement in $replacements) {
        if ($content -match $replacement.From) {
            $content = $content -replace $replacement.From, $replacement.To
            $changed = $true
        }
    }
    
    if ($changed) {
        Set-Content -Path $filePath -Value $content
        Write-Host "Fixed imports in $filePath"
    }
}

# Fix imports in agents directory
Get-ChildItem -Path $agentsDir -Filter "*.py" | ForEach-Object {
    Fix-Imports -filePath $_.FullName
}

# Fix imports in graph directory (if it exists)
if (Test-Path $graphDir) {
    Get-ChildItem -Path $graphDir -Filter "*.py" | ForEach-Object {
        Fix-Imports -filePath $_.FullName
    }
}

# Fix main.py
$mainPath = Join-Path $baseDir "main.py"
if (Test-Path $mainPath) {
    Fix-Imports -filePath $mainPath
}

Write-Host "Import fixing completed!"
