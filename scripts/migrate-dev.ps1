Write-Host ""
Write-Host "======================================"
Write-Host " Migrating development database"
Write-Host "======================================"
Write-Host ""

docker exec -it pendragon_web alembic upgrade head