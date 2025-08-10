# 🚀 Deployment Guide - GHG Emissions Calculator

## AWS Deployment (Production Ready)

### Prerequisites
- AWS Account (✅ You have this!)
- AWS CLI installed
- Basic familiarity with AWS console

### Step 1: Setup AWS RDS Database

1. **Create RDS MySQL Instance**:
   - Go to AWS RDS Console: [console.aws.amazon.com/rds](https://console.aws.amazon.com/rds)
   - Click "Create database"
   - Choose "MySQL" 
   - Select "Free tier" template
   - Settings:
     - DB instance identifier: `ghg-emissions-db`
     - Master username: `admin`
     - Master password: Create a strong password
   - DB instance class: `db.t3.micro` (free tier)
   - Storage: 20 GB (free tier)
   - **Important**: Enable "Public access" for initial setup
   - Create database

2. **Configure Security Group**:
   - Go to EC2 Console → Security Groups
   - Find your RDS security group
   - Add inbound rule:
     - Type: MySQL/Aurora
     - Port: 3306
     - Source: Anywhere (0.0.0.0/0) for initial setup
   - Save rules

3. **Note Database Details**:
   - Endpoint (hostname)
   - Port (usually 3306)
   - Username (admin)
   - Password (what you set)
   - Database name: Create `ghg_emissions_db`

### Step 2: Deploy Application

#### Option A: AWS App Runner (Recommended - Easiest)

1. **Push Code to GitHub** (if not done):
   ```bash
   git init
   git add .
   git commit -m "AWS deployment setup"
   git remote add origin https://github.com/YOURUSERNAME/ghg-emissions-calculator.git
   git push -u origin main
   ```

2. **Create App Runner Service**:
   - Go to AWS App Runner Console
   - Click "Create service"
   - Source: "Source code repository"
   - Connect to GitHub
   - Select your repository: `ghg-emissions-calculator`
   - Branch: `main`
   - Configuration: "Configure all settings here"
   - Build settings:
     - Runtime: Python 3
     - Build command: `pip install -r requirements.txt`
     - Start command: `streamlit run main_app.py --server.port=8080 --server.address=0.0.0.0 --server.headless=true`
   - Service settings:
     - Service name: `ghg-emissions-calculator`
     - Port: 8080
   - Environment variables:
     ```
     ENVIRONMENT=production
     DB_HOST=your-rds-endpoint
     DB_NAME=ghg_emissions_db
     DB_USER=admin
     DB_PASSWORD=your-rds-password
     DB_PORT=3306
     SECRET_KEY=your-super-secret-key
     ```
   - Create service

#### Option B: AWS Elastic Beanstalk

1. **Install EB CLI**:
   ```bash
   pip install awsebcli
   ```

2. **Initialize Elastic Beanstalk**:
   ```bash
   eb init
   # Choose your region
   # Select "Create new application"
   # Application name: ghg-emissions-calculator
   # Platform: Python 3.9
   ```

3. **Create Environment**:
   ```bash
   eb create production
   ```

4. **Set Environment Variables**:
   ```bash
   eb setenv ENVIRONMENT=production DB_HOST=your-rds-endpoint DB_NAME=ghg_emissions_db DB_USER=admin DB_PASSWORD=your-password SECRET_KEY=your-secret-key
   ```

5. **Deploy**:
   ```bash
   eb deploy
   ```

### Step 3: Initialize Database

1. **Connect to Your Deployed App**
2. **Access Database Setup** - The app will guide you through initial setup
3. **Or manually run setup** if needed

### Step 4: Secure Your Database

After successful deployment:
1. **Update RDS Security Group**:
   - Remove "Anywhere" access
   - Add specific IP ranges or your App Runner/EB security group
2. **Enable SSL** for production

## Quick Start - Streamlit Community Cloud (Recommended)

### Prerequisites
- GitHub account
- Cloud database (recommended: PlanetScale, AWS RDS, or Railway)

### Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial deployment setup"
   ```

2. **Create GitHub Repository**:
   - Go to [github.com](https://github.com)
   - Create new repository: `ghg-emissions-calculator`
   - Push your code:
   ```bash
   git remote add origin https://github.com/YOURUSERNAME/ghg-emissions-calculator.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Setup Cloud Database

#### Option A: PlanetScale (Recommended - Free Tier)
1. Sign up at [planetscale.com](https://planetscale.com)
2. Create new database: `ghg-emissions-db`
3. Get connection details from dashboard
4. Note down: host, username, password, database name

#### Option B: Railway
1. Sign up at [railway.app](https://railway.app)
2. Create new project
3. Add MySQL database
4. Get connection string

### Step 3: Deploy on Streamlit Cloud

1. **Visit Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

2. **Deploy App**:
   - Click "New app"
   - Select your repository: `ghg-emissions-calculator`
   - Main file: `main_app.py`
   - Click "Deploy"

3. **Add Secrets** (Environment Variables):
   - In your app dashboard, go to "Secrets"
   - Add the following:
   ```toml
   ENVIRONMENT = "production"
   DB_HOST = "your-database-host"
   DB_NAME = "ghg_emissions_db" 
   DB_USER = "your-database-user"
   DB_PASSWORD = "your-database-password"
   DB_PORT = "3306"
   SECRET_KEY = "your-super-secret-key-make-it-long-and-random"
   ```

### Step 4: Initialize Database

After deployment, your app will be available at: `https://your-app-name.streamlit.app`

The first time you access it, you may need to initialize the database:
1. The app will show database setup instructions
2. Run the database migration if needed

## Alternative: Heroku Deployment

### Step 1: Setup Heroku
```bash
# Install Heroku CLI
# Visit: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-app-name
```

### Step 2: Add Database
```bash
# Add ClearDB MySQL addon
heroku addons:create cleardb:ignite

# Get database URL
heroku config:get CLEARDB_DATABASE_URL
```

### Step 3: Configure Environment
```bash
heroku config:set ENVIRONMENT=production
heroku config:set SECRET_KEY=your-secret-key
# Database URL is automatically set by ClearDB addon
```

### Step 4: Deploy
```bash
git push heroku main
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `ENVIRONMENT` | Deployment environment | `production` |
| `DB_HOST` | Database hostname | `abc123.us-east-1.rds.amazonaws.com` |
| `DB_NAME` | Database name | `ghg_emissions_db` |
| `DB_USER` | Database username | `admin` |
| `DB_PASSWORD` | Database password | `your-secure-password` |
| `DB_PORT` | Database port | `3306` |
| `SECRET_KEY` | Application secret key | `long-random-string-here` |

## Post-Deployment Checklist

- [ ] App loads without errors
- [ ] Database connection successful
- [ ] User registration works
- [ ] Login functionality works
- [ ] All 17 Scope 3 categories display
- [ ] Emissions calculation works
- [ ] Data visualization displays
- [ ] No console errors

## Troubleshooting

### Common Issues:

1. **Database Connection Failed**:
   - Check environment variables
   - Verify database credentials
   - Ensure database allows external connections

2. **Missing Categories**:
   - Run database setup script
   - Check database has all GHG categories

3. **Login Issues**:
   - Verify SECRET_KEY is set
   - Check user table exists

### Getting Help:
- Check app logs in your deployment platform
- Verify all environment variables are set
- Test database connection separately

## Monitoring

After deployment, monitor:
- App performance and response times
- Database connection health
- User registration and login success rates
- Error logs

Your GHG Emissions Calculator is now ready for global access! 🌍✨
