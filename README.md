"""
# Aiogram Bot - Cake Shop Telegram Bot

Modern, well-structured Telegram bot for managing cake shop orders.

## Project Structure

```
aiogram-bot/
├── config/                 # Configuration and settings
│   ├── __init__.py
│   └── settings.py         # Environment variables and settings
├── core/                   # Core constants and configurations
│   ├── __init__.py
│   └── constants.py        # Application-wide constants
├── database/               # Database operations
│   ├── __init__.py
│   └── base.py             # Database connection and queries
├── handlers/               # Message and callback handlers
│   ├── __init__.py
│   ├── keyboards/          # Inline keyboard builders
│   │   ├── __init__.py
│   │   └── main.py
│   └── messages/           # Message handlers
│       ├── __init__.py
│       ├── callbacks.py    # Callback query handlers
│       └── commands.py     # Command and text message handlers
├── forms/                  # FSM forms for state management
│   ├── __init__.py
│   └── user.py            # User order form states
├── utils/                  # Utilities and helpers
│   ├── __init__.py
│   └── validators.py      # Data validation functions
├── main.py                # Application entry point
├── requirements.txt        # Project dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Features

- 📦 **Order Management** - Easy order creation and tracking
- 🎂 **Cake Selection** - Browse and select from available cakes
- 📅 **Date Scheduling** - Interactive calendar for delivery dates
- 📸 **Media Support** - Upload reference photos/videos
- 🔔 **Admin Notifications** - Orders sent directly to admin
- 💾 **Database Storage** - PostgreSQL for persistent data
- ✅ **Input Validation** - Phone, email, and date validation
- 🎨 **Inline Keyboards** - User-friendly interface

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/makssabdal-ai/aiogram-bot.git
cd aiogram-bot
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql://user:password@localhost/aiogram_bot
ADMIN_ID=your_admin_telegram_id
```

### 5. Run the bot

```bash
python main.py
```

## Code Style

This project follows PEP 8 standards:
- Maximum line length: 88 characters
- 4 spaces for indentation
- Type hints for all functions
- Comprehensive docstrings

## Architecture Highlights

### Modular Design
- Separated concerns (database, handlers, utilities)
- Easy to extend and maintain
- Clear dependency relationships

### Type Hints
All functions include type hints for better IDE support and code clarity.

### Configuration Management
- Centralized settings in `config/settings.py`
- Environment variables for sensitive data
- Easy to switch between development/production

### Database Abstraction
- Connection pooling for performance
- Organized query methods by entity
- Prepared statements for security

### Handler Organization
- Callbacks separated from message handlers
- Keyboard builders in dedicated module
- Clean import structure

## Development

### Add a new handler

1. Create a function in `handlers/messages/callbacks.py` or `handlers/messages/commands.py`
2. Use appropriate decorators (@router.callback_query, @router.message, etc.)
3. Follow naming conventions and docstring style

### Add a database query

1. Add method to `database/base.py` class
2. Use async/await syntax
3. Include type hints and docstrings

### Add constants

Add new constants to `core/constants.py` and import in relevant modules.

## License

This project is open source and available under the MIT License.

## Contact

- Telegram: @Sewwwqp
- VK: https://vk.com/polya_smi
- Channel: https://t.me/tortsm

"""
