@echo off
echo ========================================
echo    亚马逊游戏展示 - Web应用启动器
echo ========================================
echo.

REM 检查是否存在游戏数据
echo 正在检查游戏数据...
if not exist "amazon_scraper\games_data.json" (
    echo.
    echo [错误] 未找到游戏数据文件！
    echo 请先运行 run.bat 进行数据爬取，或确保 games_data.json 文件存在
    echo.
    pause
    exit /b 1
)

REM 检查数据文件是否为空
for %%A in (amazon_scraper\games_data.json) do set size=%%~zA
if %size% lss 10 (
    echo.
    echo [警告] 游戏数据文件过小，可能数据不完整
    echo 建议运行 run.bat 重新爬取数据
    echo.
    pause
)

echo [✓] 游戏数据文件检查完成
echo.

REM 检查虚拟环境
echo 正在检查Python虚拟环境...
if not exist "venv\Scripts\python.exe" (
    echo.
    echo [错误] 未找到虚拟环境！
    echo 请先运行 run.bat 创建虚拟环境
    echo.
    pause
    exit /b 1
)

echo [✓] 虚拟环境检查完成
echo.

echo 正在启动Web应用...
echo.
echo ========================================
echo  🌐 请在浏览器中访问以下地址：
echo     http://127.0.0.1:5000
echo ========================================
echo.
echo 提示：按 Ctrl+C 可停止Web服务器
echo.

REM 启动Web应用
cd web_app
..\venv\Scripts\python app.py

REM 如果Web应用异常退出
echo.
echo Web应用已停止运行
pause
