# Running Chanlun Pro Locally

This document explains how to successfully run the Chanlun Pro application on your local machine.

## Prerequisites

- Python 3.11
- macOS/Linux environment
- Access to external data sources (optional, for full functionality)

## Installation Process

### 1. Install Dependencies

```bash
# Install TA-Lib C library (macOS)
brew install ta-lib

# Install Python dependencies using uv
uv sync
```

If you don't have uv installed:

```bash
pip install uv
uv sync
```

### 2. Install Additional Packages

```bash
# Install pytdx from local wheel
pip install package/pytdx-1.72r2-py3-none-any.whl

# Install TA-Lib Python wrapper
pip install TA-Lib
```

### 3. Configure the Application

Copy the configuration template:

```bash
cp src/chanlun/config.py.demo src/chanlun/config.py
```

### 4. Update Configuration for Local Development

Edit `src/chanlun/config.py` and make the following changes:

1. Change all exchange settings from external sources to "db":

```python
EXCHANGE_A = "db"  # 沪深A股市场
EXCHANGE_HK = "db"  # 港股市场
EXCHANGE_FUTURES = "db"  # 期货市场
EXCHANGE_NY_FUTURES = "db"  # 纽约期货市场
EXCHANGE_CURRENCY = "db"  # 数字货币（合约）
EXCHANGE_CURRENCY_SPOT = "db"  # 数字货币（现货）
EXCHANGE_US = "db"  # 美股市场
EXCHANGE_FX = "db"  # 外汇市场
```

2. Ensure SQLite database is configured:

```python
DB_TYPE = "sqlite"
DB_HOST = ''
DB_PORT = 0
DB_USER = ''
DB_PWD = ''
DB_DATABASE = 'chanlun_klines'
```

### 5. Create Data Directory

```bash
mkdir -p ~/.chanlun_pro
```

## Running the Application

### Standard Method

The main application may have issues with background tasks that consume too many resources. Use the minimal startup script:

```bash
cd /Users/frank/work/chanlun-pro && python start_app.py
```

### Full Application (Advanced Users)

If you have configured external data sources and API keys, you can try running the full application:

```bash
cd /Users/frank/work/chanlun-pro/web/chanlun_chart && PYTHONPATH="/Users/frank/work/chanlun-pro/src:." python app.py
```

## Accessing the Application

Once running, the application will be available at:

- **Web Interface**: http://127.0.0.1:9900
- **Health Check**: http://127.0.0.1:9900/health

## Troubleshooting

### Common Issues

1. **Process Gets Killed ("Killed: 9")**:

   - This is typically due to the application trying to initialize external data connections
   - Solution: Use the minimal startup script or ensure all exchange settings are set to "db"

2. **Database Connection Errors**:

   - Ensure the `~/.chanlun_pro` directory exists
   - Check that `DB_TYPE` is set to "sqlite" in config

3. **Port Already in Use**:
   - Kill existing processes: `pkill -f "python.*app\.py"`
   - Or change the port in the application code

### Configuration Notes

- The application works best in "db" mode for local development
- External data sources (TDX, Binance, etc.) require valid API keys and network connectivity
- Background tasks are disabled in the minimal startup to prevent resource issues

## Features Available

With the minimal setup:

- Basic web interface
- Chart visualization (using local/empty data)
- Configuration management
- Basic API endpoints

Full functionality requires:

- External data source configurations
- Valid API keys for various exchanges
- Proper network connectivity
