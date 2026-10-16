# Check if venv already exists, if not, create it
if (-not (Test-Path -Path ".\venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
}

# Run the activation script and install dependencies inside the same block
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Cyan
& .\venv\Scripts/pip install -r requirements.txt

Write-Host "Setup complete! To start working, run:" -ForegroundColor Green
Write-Host ".\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
