# BackerWave - Crowdfunding Platform

## Description
BackerWave is a scalable, modern crowdfunding platform built with Django and Bootstrap 5. 

## Features Implemented
### Phase 1: Core & Authentication
- Custom user profiles (Creator, Contributor).
- User Registration, Login, and Logout.
- Profile management (view and update).
- Responsive UI using Bootstrap 5 and custom CSS.
- Secure authentication handling.

### Phase 2: Campaign Management
- Campaign Creation, Editing, and Deletion (for Creators).
- Category management for campaigns.
- Publicly browsing, searching, sorting, and filtering campaigns.
- Campaign detailed view with progress indicators.
- Creator Dashboard to manage campaigns and view stats.
- Role-based access control (only Creators can create/edit their own campaigns).

## Technology Stack
- **Backend**: Python 3.11+, Django 4.2+
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite
- **Environment**: python-dotenv for secret management

## Installation Steps
1. Clone the repository or navigate to the project directory.
2. Set up the virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy environment variables:
   ```bash
   cp .env.example .env
   ```
5. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Create an admin user:
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Running Tests
Run all unit tests using:
```bash
python manage.py test
```
