Write-Host ""
Write-Host "======================================"
Write-Host " Restarting Pendragon containers"
Write-Host "======================================"
Write-Host ""

docker compose down
docker compose up -d --build
docker ps