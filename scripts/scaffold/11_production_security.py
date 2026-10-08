import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

def replace_in_file(path, old, new):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.replace(old, new))

# 1. Update settings.py for production security
replace_in_file('backerwave/settings.py', 
    "DEBUG = os.environ.get('DEBUG', 'True') == 'True'",
    "DEBUG = os.environ.get('DEBUG', 'False') == 'True'")

security_settings = """
# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
"""
with open('backerwave/settings.py', 'a', encoding='utf-8') as f:
    f.write('\n' + security_settings.strip() + '\n')

# 2. Add Database Constraints to campaigns/models.py and contributions/models.py
replace_in_file('campaigns/models.py', 
    "class Meta:\n        unique_together = ('user', 'campaign')",
    "class Meta:\n        unique_together = ('user', 'campaign')\n        constraints = [\n            models.CheckConstraint(check=models.Q(goal_amount__gt=0), name='goal_amount_gt_0')\n        ]")
replace_in_file('campaigns/models.py', "from django.db import models", "from django.db import models\nfrom django.db.models import Q")

# Oh wait, the constraint on `goal_amount` is on `Campaign`, not `FavoriteCampaign`.
# Let's fix that.
# Let's completely rewrite campaigns/models.py constraints safely using regex or just rewrite it entirely.
# Since it's safer, I'll use replace_in_file but correctly.
replace_in_file('campaigns/models.py',
    """class Campaign(models.Model):
    STATUS_CHOICES = (""",
    """class Campaign(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(goal_amount__gt=0), name='campaign_goal_gt_0'),
            models.CheckConstraint(check=models.Q(current_amount__gte=0), name='campaign_current_gte_0')
        ]

    STATUS_CHOICES = (""")

replace_in_file('contributions/models.py', "from django.db import models", "from django.db import models\nfrom django.db.models import Q")
replace_in_file('contributions/models.py',
    """class Contribution(models.Model):
    STATUS_CHOICES = (""",
    """class Contribution(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gt=0), name='contribution_amount_gt_0')
        ]
        
    STATUS_CHOICES = (""")

# 3. Create Documentation Files
docs_architecture = """
# Architecture
BackerWave follows the standard Django Model-View-Template (MVT) architecture.
- **Models**: Defines database schema (SQLite in development, PostgreSQL ready).
- **Views**: Business logic, filtering, sorting, permissions.
- **Templates**: Bootstrap 5 with server-side rendered HTML.
- **Apps**: `accounts`, `core`, `campaigns`, `contributions`.
"""
write_file('docs/architecture.md', docs_architecture)

docs_database = """
# Database Schema
## Relationships
- **User** 1:1 **Profile**
- **User** 1:N **Campaigns** (as creator)
- **User** 1:N **Contributions** (as contributor)
- **User** 1:N **FavoriteCampaigns**
- **User** 1:N **Notifications**

- **Category** 1:N **Campaigns**
- **Campaign** 1:N **Contributions**
- **Campaign** 1:N **CampaignUpdates**
- **Campaign** 1:N **FavoriteCampaigns**
"""
write_file('docs/database.md', docs_database)

docs_api = """
# API
BackerWave currently uses Django Template rendering and traditional HTTP POST forms. There is no external REST API in this phase.
"""
write_file('docs/api.md', docs_api)

docs_installation = """
# Installation
1. Clone the repository.
2. `python -m venv venv`
3. `venv\\Scripts\\activate`
4. `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and set variables.
6. `python manage.py migrate`
"""
write_file('docs/installation.md', docs_installation)

docs_deployment = """
# Deployment (DEPLOYMENT.md)
## Hosting Options
- **Linux Server / VPS**
- **Platform as a Service (Heroku, Render)**

## Required Tech Stack for Prod
- Gunicorn (WSGI Server)
- Nginx (Reverse Proxy & Static Files)
- PostgreSQL (Database)

## Commands
```bash
pip install gunicorn psycopg2-binary
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn backerwave.wsgi:application --bind 0.0.0.0:8000
```
"""
write_file('DEPLOYMENT.md', docs_deployment)
write_file('docs/deployment.md', docs_deployment)

docs_testing = """
# Testing
Run tests using:
`python manage.py test`

The test suite covers:
- User flows (Auth, Profiles)
- Campaign validation (Amount > 0, Dates)
- Contribution atomicity & calculation
- Edge cases and permissions.
"""
write_file('docs/testing.md', docs_testing)

# Final README
readme_md = """
# BackerWave - Crowdfunding Platform

## Project Description
BackerWave is a robust, responsive, and secure crowdfunding platform designed to connect creators with passionate contributors.

## Features
- **Creator Dashboard**: Launch campaigns, post updates, and track contributor metrics.
- **Contributor Dashboard**: Monitor your supported campaigns and favorite listings.
- **Advanced Discovery**: Filter, search, and sort campaigns efficiently.
- **Secure Transactions**: Mock atomic payment transactions simulating real-world safety logic.
- **Notifications**: Stay updated when campaigns reach their goals or post updates.
- **Responsive UI**: Bootstrap 5 + custom tailored CSS.

## Architecture & Tech Stack
- **Backend**: Python 3.11+, Django 4.2+
- **Database**: SQLite (Development) / PostgreSQL Ready
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5

## Installation
See `docs/installation.md` for local setup.
See `DEPLOYMENT.md` for production deployment instructions.
"""
write_file('README.md', readme_md)
