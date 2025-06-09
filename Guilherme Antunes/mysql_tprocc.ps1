# Define log directory (adjust as needed)
$logDir = "C:\Users\guipm\logs\Set7"

# Get current number of cpu log files
$existingCpuLogs = Get-ChildItem -Path $logDir -Filter "cpu*.log" -ErrorAction SilentlyContinue
$testNumber = if ($existingCpuLogs) { $existingCpuLogs.Count + 1 } else { 1 }

# Define log file paths for this test
$cpuLog = "$logDir\cpu$testNumber.log"
$ioLog = "$logDir\io$testNumber.log"

# --- Your HammerDB workflow ---
Write-Output "BUILD HAMMERDB SCHEMA"
Write-Output "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-"
hammerdbcli auto ./scripts/tcl/mysql/tprocc/mysql_tprocc_buildschema.tcl 
Write-Output "CHECK HAMMERDB SCHEMA"
Write-Output "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-"
hammerdbcli auto ./scripts/tcl/mysql/tprocc/mysql_tprocc_checkschema.tcl
Write-Output "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-"
Write-Output "RUN HAMMERDB TEST"
Write-Output "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-"
Write-Output "Starting logging for Test #$testNumber"
# Start logging CPU and IO inside WSL asynchronously (adjust duration 300s to your test length)
Start-Process -NoNewWindow -FilePath wsl -ArgumentList "timeout 420 mpstat -P ALL 1 > /mnt/c/Users/guipm/logs/Set7/cpu$testNumber.log" 
Start-Process -NoNewWindow -FilePath wsl -ArgumentList "timeout 420 iostat -dx 1 > /mnt/c/Users/guipm/logs/Set7/io$testNumber.log"
hammerdbcli auto ./scripts/tcl/mysql/tprocc/mysql_tprocc_run.tcl 
Write-Output "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-"
Write-Output "DROP HAMMERDB SCHEMA"
hammerdbcli auto ./scripts/tcl/mysql/tprocc/mysql_tprocc_deleteschema.tcl
Write-Output "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-"
Write-Output "HAMMERDB RESULT"
hammerdbcli auto ./scripts/tcl/mysql/tprocc/mysql_tprocc_result.tcl 
Write-Output "Test #$testNumber completed. Stopping logging..."

# Stop logging by killing mpstat and iostat inside WSL
wsl pkill mpstat
wsl pkill iostat
