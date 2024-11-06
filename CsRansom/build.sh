#!/bin/bash

# Lấy đường dẫn của thư mục hiện tại
currentDirectory=$(pwd)

# Đặt đường dẫn file dự án
projectFilePath="$currentDirectory/Ransomware.csproj"

# Đặt cấu hình cho build (Debug hoặc Release)
configuration="Release"

# Đường dẫn đến thư mục publish bên trong bin
publishBasePath="$currentDirectory/bin/$configuration"

# Danh sách các nền tảng để build (chỉ dành cho Linux và macOS)
platforms=(
    "linux-x64"     # Linux 64-bit
    "linux-arm"     # Linux ARM
    "linux-arm64"   # Linux ARM 64
    "osx-x64"       # macOS 64-bit
    "osx-arm64"      # macOS ARM 64
)

# Hiển thị danh sách các nền tảng cho người dùng
echo "CThe platform for build and publish (separated by commas) (Ex: 1,2):"
for i in "${!platforms[@]}"; do
    echo "$((i + 1)): ${platforms[$i]}"
done

# Yêu cầu người dùng nhập lựa chọn
read -p "Enter the number corresponding to the platform you want to build (1-${#platforms[@]}):" selectedPlatformsInput
IFS=',' read -r -a selectedPlatformsIndexes <<< "$selectedPlatformsInput"

# Kiểm tra xem có lựa chọn hợp lệ không
validIndexes=()
for index in "${selectedPlatformsIndexes[@]}"; do
    ((index--))
    if [[ $index -ge 0 && $index -lt ${#platforms[@]} ]]; then
        validIndexes+=($index)
    fi
done

if [ ${#validIndexes[@]} -eq 0 ]; then
    echo "There are no valid options. Please restart and try again."
    exit 1
fi

# Lặp qua từng nền tảng được chọn và thực hiện build và publish
for index in "${validIndexes[@]}"; do
    platform=${platforms[$index]}
    
    # Đặt đường dẫn đầu ra cho nền tảng đã chọn
    outputPath="$publishBasePath/$platform"
    publishPath="$outputPath/publish"

    # Kiểm tra xem có tồn tại thư mục bin hay không, nếu có thì xóa
    binDirectory="$(dirname "$projectFilePath")/bin"
    if [ -d "$binDirectory" ]; then
        rm -rf "$binDirectory"
    fi

    # Build dự án
    dotnet build "$projectFilePath" -c "$configuration" -r "$platform"
    if [ $? -ne 0 ]; then
        exit 1
    fi

    # Publish dự án
    dotnet publish "$projectFilePath" -c "$configuration" -r "$platform" -p:PublishSingleFile=true -p:PublishTrimmed=true -p:SelfContained=true -p:PublishDir="$publishPath" --self-contained
    if [ $? -ne 0 ]; then
        exit 1
    fi

    # Đường dẫn mới cho thư mục publish
    newPublishPath="$currentDirectory/build/$platform"

    # Tạo thư mục publish mới nếu nó không tồn tại
    mkdir -p "$newPublishPath"

    # Kiểm tra nếu thư mục publish tồn tại
    if [ -d "$publishPath" ]; then
        # Xóa thư mục cũ nếu đã tồn tại
        rm -rf "$newPublishPath"

        # Di chuyển và đổi tên thư mục publish
        mv "$publishPath" "$newPublishPath"
    fi
done