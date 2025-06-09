# Desired number of successful runs
$requiredSuccesses = 5

# Path to the HammerDB .ps1 script
$scriptPath = "C:\Program Files\HammerDB-5.0\scripts\tcl\mysql\tprocc\mysql_tprocc.ps1"

# The error message to look for in the output (adjust as needed)
$errorPattern = "Failed to load Pgtcl - couldn't open"

# Counter for successful tests
$successCount = 0
$globalAttempt = 0

while ($successCount -lt $requiredSuccesses) {
    $attempt = 0
    $success = $false

    do {
        $logFile = "output_test${successCount}_try${attempt}.log"
        Write-Host ""
        Write-Host "==============================="
        Write-Host "      Test #$($successCount + 1) - Attempt $attempt"
        Write-Host "==============================="

        # Run the script and capture output
        $output = & $scriptPath *>&1
        $output | Out-File -FilePath $logFile -Encoding UTF8

        # Check for the known error
        if ($output -match $errorPattern) {
            Write-Host "Error detected - retrying..."
            $attempt++
        } else {
            Write-Host "Test #$($successCount + 1) succeeded"
            $success = $true
            $successCount++
        }

        $globalAttempt++

    } while (-not $success)
}

Write-Host ""
Write-Host "==============================="
Write-Host "All $requiredSuccesses tests completed successfully!"
Write-Host "==============================="
