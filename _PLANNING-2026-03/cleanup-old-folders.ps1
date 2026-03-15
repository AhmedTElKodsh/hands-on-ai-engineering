# Cleanup Script - March 2026 Reorganization
# Run this AFTER verifying archives are complete
# Date: March 10, 2026

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "March 2026 Reorganization - Cleanup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verify archives exist
Write-Host "Step 1: Verifying archives..." -ForegroundColor Yellow
$archivePath = "_ARCHIVE_2026-03"
if (Test-Path $archivePath) {
    Write-Host "  ✓ Archive folder exists: $archivePath" -ForegroundColor Green
    
    $archivedItems = Get-ChildItem $archivePath -Directory
    Write-Host "  Archived items:" -ForegroundColor Gray
    foreach ($item in $archivedItems) {
        Write-Host "    - $($item.Name)" -ForegroundColor Gray
    }
} else {
    Write-Host "  ✗ Archive folder NOT found! Stopping cleanup." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Verify LAYER1-FINAL exists
Write-Host "Step 2: Verifying LAYER1-FINAL (canonical curriculum)..." -ForegroundColor Yellow
$layer1Final = "LAYER1-FINAL"
if (Test-Path $layer1Final) {
    Write-Host "  ✓ LAYER1-FINAL exists: $layer1Final" -ForegroundColor Green
} else {
    Write-Host "  ✗ LAYER1-FINAL NOT found! CRITICAL - do not delete anything!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Verify planning docs
Write-Host "Step 3: Verifying planning documents..." -ForegroundColor Yellow
$planningPath = "_PLANNING-2026-03"
if (Test-Path $planningPath) {
    Write-Host "  ✓ Planning folder exists: $planningPath" -ForegroundColor Green
    
    $planningDocs = Get-ChildItem $planningPath -Filter "*.md"
    Write-Host "  Planning documents:" -ForegroundColor Gray
    foreach ($doc in $planningDocs) {
        Write-Host "    - $($doc.Name)" -ForegroundColor Gray
    }
} else {
    Write-Host "  ✗ Planning folder NOT found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verification Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Items to delete
Write-Host "The following items will be DELETED:" -ForegroundColor Yellow
Write-Host "  Folders:" -ForegroundColor Yellow
Write-Host "    - Layer1-Curriculum/" -ForegroundColor Gray
Write-Host "    - Layer2-Curriculum/" -ForegroundColor Gray
Write-Host "    - layer1-phase1/" -ForegroundColor Gray
Write-Host ""
Write-Host "  Files:" -ForegroundColor Yellow
Write-Host "    - MODIFIED-CURRICULUM-INDEX.md" -ForegroundColor Gray
Write-Host "    - MIGRATION-GUIDE.md" -ForegroundColor Gray
Write-Host "    - CURRICULUM-REVIEW-2026-03-08.md" -ForegroundColor Gray
Write-Host ""

# Confirmation
$confirmation = Read-Host "Are you sure you want to proceed? Type 'YES' to confirm"
if ($confirmation -ne "YES") {
    Write-Host "Cleanup cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Starting cleanup..." -ForegroundColor Yellow
Write-Host ""

# Delete folders
$foldersToDelete = @("Layer1-Curriculum", "Layer2-Curriculum", "layer1-phase1")
foreach ($folder in $foldersToDelete) {
    if (Test-Path $folder) {
        Write-Host "  Deleting: $folder/" -ForegroundColor Yellow
        Remove-Item -Path $folder -Recurse -Force
        Write-Host "    ✓ Deleted" -ForegroundColor Green
    } else {
        Write-Host "    - Skipped (not found): $folder/" -ForegroundColor Gray
    }
}

Write-Host ""

# Delete files
$filesToDelete = @("MODIFIED-CURRICULUM-INDEX.md", "MIGRATION-GUIDE.md", "CURRICULUM-REVIEW-2026-03-08.md")
foreach ($file in $filesToDelete) {
    if (Test-Path $file) {
        Write-Host "  Deleting: $file" -ForegroundColor Yellow
        Remove-Item -Path $file -Force
        Write-Host "    ✓ Deleted" -ForegroundColor Green
    } else {
        Write-Host "    - Skipped (not found): $file" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cleanup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Remaining structure:" -ForegroundColor White
Write-Host "  ✓ LAYER1-FINAL/ (canonical curriculum)" -ForegroundColor Green
Write-Host "  ✓ _PLANNING-2026-03/ (planning docs)" -ForegroundColor Green
Write-Host "  ✓ _ARCHIVE_2026-03/ (archived versions)" -ForegroundColor Green
Write-Host ""
Write-Host "Next step: Update main README.md" -ForegroundColor Yellow
Write-Host ""
