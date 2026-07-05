Write-Host ""
Write-Host "======================================"
Write-Host " Migrating test database"
Write-Host "======================================"
Write-Host ""

docker exec -it pendragon_web bash -lc 'export DATABASE_URL="$TEST_DATABASE_URL" && alembic upgrade head'