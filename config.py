import os
from typing import Dict, Any
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration management for deployment"""
    
    def __init__(self):
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self.is_production = self.environment == 'production'
    
    @property
    def database_config(self) -> Dict[str, Any]:
        """Get database configuration based on environment"""
        if self.is_production:
            # Production database configuration
            # Check for database URL (Heroku style)
            if os.getenv('DATABASE_URL'):
                # Parse DATABASE_URL
                import urllib.parse as urlparse
                url = urlparse.urlparse(os.getenv('DATABASE_URL'))
                return {
                    'host': url.hostname,
                    'database': url.path[1:],  # Remove leading slash
                    'user': url.username,
                    'password': url.password,
                    'port': url.port or 3306,
                    'ssl_disabled': False,
                    'autocommit': True,
                    'charset': 'utf8mb4',
                    'use_unicode': True,
                }
            else:
                # Standard environment variables
                return {
                    'host': os.getenv('DB_HOST', 'localhost'),
                    'database': os.getenv('DB_NAME', 'ghg_emissions_db'),
                    'user': os.getenv('DB_USER', 'root'),
                    'password': os.getenv('DB_PASSWORD', ''),
                    'port': int(os.getenv('DB_PORT', '3306')),
                    'ssl_disabled': os.getenv('DB_SSL_DISABLED', 'False').lower() == 'true',
                    'autocommit': True,
                    'charset': 'utf8mb4',
                    'use_unicode': True,
                'connect_timeout': 60,
                'pool_name': 'ghg_pool',
                'pool_size': 10,
                'pool_reset_session': True
            }
        else:
            # Development database configuration
            return {
                'host': os.getenv('DB_HOST', 'localhost'),
                'database': os.getenv('DB_NAME', 'ghg_emissions_db'),
                'user': os.getenv('DB_USER', 'root'),
                'password': os.getenv('DB_PASSWORD', ''),
                'port': int(os.getenv('DB_PORT', '3306')),
                'autocommit': True,
                'charset': 'utf8mb4'
            }
    
    @property
    def app_config(self) -> Dict[str, Any]:
        """Get application configuration"""
        return {
            'app_name': os.getenv('APP_NAME', 'GHG Emission Calculator'),
            'app_version': os.getenv('APP_VERSION', '1.0.0'),
            'debug': os.getenv('DEBUG', 'False').lower() == 'true' and not self.is_production,
            'secret_key': os.getenv('SECRET_KEY', 'your-secret-key-change-in-production'),
            'session_timeout': int(os.getenv('SESSION_TIMEOUT', '3600')),  # 1 hour
            'max_file_size': int(os.getenv('MAX_FILE_SIZE', '10485760')),  # 10MB
            'allowed_file_types': os.getenv('ALLOWED_FILE_TYPES', 'csv,xlsx,xls').split(','),
            'timezone': os.getenv('TIMEZONE', 'Europe/London')
        }
    
    @property
    def security_config(self) -> Dict[str, Any]:
        """Get security configuration"""
        return {
            'password_min_length': int(os.getenv('PASSWORD_MIN_LENGTH', '8')),
            'password_require_special': os.getenv('PASSWORD_REQUIRE_SPECIAL', 'True').lower() == 'true',
            'max_login_attempts': int(os.getenv('MAX_LOGIN_ATTEMPTS', '5')),
            'lockout_duration': int(os.getenv('LOCKOUT_DURATION', '900')),  # 15 minutes
            'session_cookie_secure': self.is_production,
            'session_cookie_httponly': True,
            'csrf_protection': self.is_production
        }
    
    def get_streamlit_config(self) -> Dict[str, Any]:
        """Get Streamlit-specific configuration"""
        return {
            'page_title': self.app_config['app_name'],
            'page_icon': '🌱',
            'layout': 'wide',
            'initial_sidebar_state': 'expanded',
            'menu_items': {
                'Get Help': 'https://github.com/your-repo/ghg-calculator',
                'Report a bug': 'https://github.com/your-repo/ghg-calculator/issues',
                'About': f"# {self.app_config['app_name']} v{self.app_config['app_version']}\n"
                        f"Greenhouse Gas Emission Tracking and Reporting System"
            }
        }

# Global configuration instance
config = Config()

def setup_streamlit_config():
    """Setup Streamlit page configuration"""
    st_config = config.get_streamlit_config()
    st.set_page_config(**st_config)
    
    # Add custom CSS to reduce console errors from tooltips and popovers
    st.markdown("""
    <style>
    /* Reduce popover and tooltip related console warnings */
    .stSelectbox > div > div > div {
        border: 1px solid #e0e0e0;
        border-radius: 4px;
    }
    
    /* Improve form stability and reduce JS conflicts */
    .stForm {
        border: none;
        padding: 0;
    }
    
    /* Hide Streamlit menu to reduce JS errors */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Improve selectbox appearance and reduce tooltip conflicts */
    .stSelectbox > div > div {
        position: relative;
    }
    
    /* Prevent tooltip overflow issues */
    .element-container {
        position: relative;
        overflow: visible;
    }
    </style>
    
    <script>
    // Suppress specific console warnings
    (function() {
        const originalWarn = console.warn;
        console.warn = function(...args) {
            const message = args.join(' ');
            // Filter out popper.js modifier warnings
            if (message.includes('preventOverflow') || 
                message.includes('modifier is required') ||
                message.includes('message channel closed')) {
                return;
            }
            originalWarn.apply(console, args);
        };
        
        // Handle async response errors gracefully
        window.addEventListener('unhandledrejection', function(event) {
            if (event.reason && event.reason.message && 
                event.reason.message.includes('message channel closed')) {
                event.preventDefault();
            }
        });
    })();
    </script>
    """, unsafe_allow_html=True)

def get_database_url() -> str:
    """Get database URL for deployment platforms"""
    db_config = config.database_config
    if config.is_production and os.getenv('DATABASE_URL'):
        return os.getenv('DATABASE_URL')
    else:
        return f"mysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

def validate_environment():
    """Validate environment configuration"""
    required_vars = []
    
    if config.is_production:
        required_vars = [
            'DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD',
            'SECRET_KEY'
        ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        st.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        st.stop()
    
    return True
