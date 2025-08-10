# GHG Emissions Calculator 🌱

A comprehensive web application for calculating and tracking Greenhouse Gas emissions according to GHG Protocol standards.

## Features

- **Complete GHG Protocol Compliance**: All Scope 1, 2, and 3 categories
- **User Authentication**: Secure login and company registration
- **Data Visualization**: Interactive charts and dashboards
- **Real-time Calculations**: Automatic CO2 equivalent calculations
- **Multi-user Support**: Company-based data segregation
- **Audit Trail**: Complete tracking of all emissions data

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.9+
- **Database**: MySQL 8.0+
- **Visualization**: Plotly
- **Authentication**: bcrypt

## Deployment Options

### Option 1: Streamlit Community Cloud (Recommended - Free)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/ghg-emissions-calculator.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Add environment variables in the secrets management

3. **Database Setup**:
   - Use a cloud MySQL service (PlanetScale, AWS RDS, etc.)
   - Set environment variables in Streamlit Cloud secrets

### Option 2: Heroku Deployment

1. **Install Heroku CLI**
2. **Login and Create App**:
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Add Database**:
   ```bash
   heroku addons:create cleardb:ignite
   ```

4. **Set Environment Variables**:
   ```bash
   heroku config:set ENVIRONMENT=production
   heroku config:set SECRET_KEY=your-secret-key
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   ```

### Option 3: Railway (Modern Alternative)

1. **Connect GitHub**: Link your repository
2. **Add MySQL**: Use Railway's database service
3. **Deploy**: Automatic deployment from GitHub

## Environment Variables

Set these in your deployment platform:

```
ENVIRONMENT=production
DB_HOST=your-database-host
DB_NAME=ghg_emissions_db
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_PORT=3306
SECRET_KEY=your-super-secret-key
```

## Local Development

1. **Clone Repository**:
   ```bash
   git clone https://github.com/yourusername/ghg-emissions-calculator.git
   cd ghg-emissions-calculator
   ```

2. **Setup Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Database**:
   ```bash
   python setup_database.py
   ```

5. **Run Application**:
   ```bash
   streamlit run main_app.py
   ```

## Database Schema

The application includes comprehensive GHG Protocol categories:

- **Scope 1**: 4 categories (Direct emissions)
- **Scope 2**: 2 categories (Indirect energy emissions)
- **Scope 3**: 17 categories (Other indirect emissions)

## Security Features

- Password hashing with bcrypt
- Session management
- SQL injection prevention
- Input validation
- Audit logging

## Support

For issues or questions, please contact the development team or create an issue in the repository.

## License

MIT License - see LICENSE file for details.
