# Lấy đường dẫn của thư mục hiện tại
$currentDirectory = Get-Location

# Đặt đường dẫn file dự án
$projectFilePath = Join-Path $currentDirectory "Ransomware.csproj"

$configuration = "Release"

# Đường dẫn đến thư mục publish bên trong bin
$publishBasePath = Join-Path $currentDirectory "bin\$configuration"

# Danh sách các nền tảng để build
$platforms = @(
    "win-x64",       # Windows 64-bit
    "win-x86",       # Windows 32-bit
    "linux-x64",     # Linux 64-bit
    "linux-arm",     # Linux ARM
    "linux-arm64",   # Linux ARM 64
    "osx-x64",       # macOS 64-bit
    "osx-arm64"      # macOS ARM 64
)

# Hiển thị danh sách các nền tảng cho người dùng
for ($i = 0; $i -lt $platforms.Count; $i++) {
    Write-Host "$($i + 1): $($platforms[$i])"
}
Write-Host "Chọn nền tảng để build (Ex: 1,2,3 or 1)"

# Yêu cầu người dùng nhập lựa chọn
$selectedPlatformsInput = Read-Host "Nhập số tương ứng với nền tảng bạn muốn (1-$($platforms.Count)):"
$selectedPlatformsIndexes = $selectedPlatformsInput -split ',' | ForEach-Object { [int]($_.Trim()) - 1 }

# Kiểm tra xem có lựa chọn hợp lệ không
$validIndexes = $selectedPlatformsIndexes | Where-Object { $_ -ge 0 -and $_ -lt $platforms.Count }
if ($validIndexes.Count -eq 0) {
    Write-Host "Không có lựa chọn hợp lệ. Vui lòng khởi động lại và thử lại." -ForegroundColor Red
    exit
}

# Lặp qua từng nền tảng được chọn và thực hiện build và publish
foreach ($index in $validIndexes) {
    $platform = $platforms[$index]
    
    # Đặt đường dẫn đầu ra cho nền tảng đã chọn
    $outputPath = Join-Path $publishBasePath "$platform"
    $publishPath = Join-Path $outputPath "bin"

    # Kiểm tra xem có tồn tại thư mục bin hay không, nếu có thì xóa
    $binDirectory = Join-Path (Split-Path $projectFilePath) "bin"
    if (Test-Path $binDirectory) {
        Remove-Item -Recurse -Force $binDirectory
    }

    # Build dự án
    dotnet build $projectFilePath -c $configuration -r $platform

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Build for $platform failed." -ForegroundColor Red
        exit $LASTEXITCODE
    }

    # Publish dự án
    dotnet publish $projectFilePath -c $configuration -r $platform -p:PublishSingleFile=true -p:PublishTrimmed=true -p:SelfContained=true -p:PublishDir="$publishPath" --self-contained

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Publish for $platform failed." -ForegroundColor Red
        exit $LASTEXITCODE
    }

    Write-Host "Build and publish completed successfully for $platform." -ForegroundColor Green

    # Đường dẫn mới cho thư mục publish
    $newPublishPath = Join-Path $currentDirectory "build\$platform"

    # Tạo thư mục publish mới nếu nó không tồn tại
    if (-not (Test-Path $newPublishPath)) {
        New-Item -ItemType Directory -Path $newPublishPath -Force
    }

    # Kiểm tra nếu thư mục publish tồn tại
    if (Test-Path $publishPath) {
        # Xóa thư mục cũ nếu đã tồn tại
        Remove-Item -Recurse -Force $newPublishPath -ErrorAction SilentlyContinue
        
        # Di chuyển và đổi tên thư mục publish
        Move-Item -Path $publishPath -Destination $newPublishPath
    }
}
