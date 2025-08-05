@echo off
echo ========================================
echo      🎮 亚马逊游戏展示器 - 打包工具
echo ========================================
echo.

echo 正在检查环境...

REM 检查是否存在虚拟环境
if not exist "venv" (
    echo [提示] 创建虚拟环境...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo [错误] 创建虚拟环境失败，请确保已安装Python
        pause
        exit /b 1
    )
)

echo [✓] 虚拟环境检查完成

REM 激活虚拟环境并安装依赖
echo [提示] 安装打包依赖...
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\pip install -r requirements_standalone.txt

if %ERRORLEVEL% neq 0 (
    echo [错误] 安装依赖失败
    pause
    exit /b 1
)

echo [✓] 依赖安装完成

REM 检查游戏数据文件
if not exist "amazon_scraper\games_data.json" (
    echo.
    echo [错误] 未找到游戏数据文件！
    echo 请确保 amazon_scraper\games_data.json 文件存在
    echo 如果没有数据，请先运行 run.bat 获取数据
    echo.
    pause
    exit /b 1
)

echo [✓] 游戏数据文件检查完成

REM 清理之前的打包文件
echo [提示] 清理旧的打包文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM 开始打包
echo.
echo ========================================
echo        开始打包独立可执行程序...
echo ========================================
echo.

venv\Scripts\pyinstaller standalone_app.spec

if %ERRORLEVEL% neq 0 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

REM 复制游戏数据到打包目录
echo [提示] 复制游戏数据文件...
copy "amazon_scraper\games_data.json" "dist\"

echo.
echo ========================================
echo          🎉 打包完成！
echo ========================================
echo.
echo 📁 可执行文件位置: dist\亚马逊游戏展示器.exe
echo 📋 使用说明:
echo    1. 将 dist 文件夹整个复制到目标电脑
echo    2. 确保 games_data.json 与 exe 文件在同一目录
echo    3. 双击 亚马逊游戏展示器.exe 即可运行
echo.
echo 💡 提示: 
echo    - 无需安装Python环境
echo    - 程序会自动打开浏览器
echo    - 访问地址: http://127.0.0.1:5000
echo.

pause
