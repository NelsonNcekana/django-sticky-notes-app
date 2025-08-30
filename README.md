# Sticky Notes Application

A modern, responsive Django web application for creating, managing, and organizing sticky notes with advanced features like categorization, priority levels, search, and filtering.

## Features

### Core Functionality
- **CRUD Operations**: Create, Read, Update, Delete notes
- **Note Management**: Title, content, category, and priority
- **Search & Filter**: Search by title/content, filter by category/priority
- **Archive System**: Soft delete functionality
- **Responsive Design**: Mobile-first, Bootstrap-powered interface

### Technical Features
- **Django MVT Architecture**: Model-View-Template pattern
- **Class-Based Views**: Efficient, maintainable code structure
- **Form Validation**: Client and server-side validation
- **Static File Management**: CSS and JavaScript organization
- **Admin Interface**: Full Django admin integration

## Technology Stack

- **Backend**: Django 5.2.5
- **Frontend**: HTML5, CSS3, JavaScript
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.0.0
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Python**: 3.8+

## Project Structure

```
sticky_notes_project/
├── sticky_notes_project/          # Project settings and configuration
│   ├── __init__.py
│   ├── settings.py                # Django settings
│   ├── urls.py                    # Main URL configuration
│   ├── wsgi.py                    # WSGI configuration
│   └── asgi.py                    # ASGI configuration
├── sticky_notes_app/              # Main application
│   ├── __init__.py
│   ├── admin.py                   # Admin interface configuration
│   ├── apps.py                    # App configuration
│   ├── forms.py                   # Form definitions
│   ├── models.py                  # Database models
│   ├── urls.py                    # App URL patterns
│   ├── views.py                   # View logic
│   ├── static/                    # Static files (CSS, JS)
│   │   └── sticky_notes_app/
│   │       └── css/
│   │           └── style.css      # Custom styles
│   └── templates/                 # HTML templates
│       └── sticky_notes_app/
│           ├── base.html          # Base template
│           ├── note_list.html     # Notes list view
│           ├── note_detail.html   # Note detail view
│           ├── note_form.html     # Create/edit form
│           ├── note_confirm_delete.html # Delete confirmation
│           └── search_results.html # Search results
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── design_documentation.md        # Design diagrams and documentation
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd sticky_notes

# Or download and extract the ZIP file
cd sticky_notes
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Collect Static Files
```bash
python manage.py collectstatic
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

### Step 8: Access the Application
- **Main App**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/admin/

## Usage

### Creating Notes
1. Navigate to the main page
2. Click "New Note" button
3. Fill in title, content, category, and priority
4. Click "Create Note"

### Managing Notes
- **View**: Click the eye icon on any note
- **Edit**: Click the edit icon to modify notes
- **Delete**: Click the trash icon (with confirmation)
- **Archive**: Use the archive button to hide notes

### Searching and Filtering
- **Search**: Use the search bar in the navigation
- **Filters**: Use the sidebar filters for category and priority
- **Combined Search**: Combine search terms with filters

## Database Models

### Note Model
- **title**: CharField (max 200 characters)
- **content**: TextField (unlimited text)
- **category**: ChoiceField (Personal, Work, Shopping, Ideas, Reminders, Other)
- **priority**: ChoiceField (Low, Medium, High, Urgent)
- **created_at**: DateTimeField (auto-created)
- **updated_at**: DateTimeField (auto-updated)
- **is_archived**: BooleanField (default: False)

## URL Structure

| URL Pattern | View | Description |
|-------------|------|-------------|
| `/` | Home | Redirects to notes list |
| `/notes/` | Note List | Display all notes with search/filters |
| `/note/new/` | Create | Form to create new note |
| `/note/<id>/` | Detail | View individual note |
| `/note/<id>/edit/` | Edit | Form to edit existing note |
| `/note/<id>/delete/` | Delete | Confirmation page for deletion |
| `/note/<id>/archive/` | Archive | Toggle archive status |
| `/search/` | Search | Search and filter results |

## Customization

### Styling
- **CSS**: Modify `sticky_notes_app/static/sticky_notes_app/css/style.css`
- **Bootstrap**: Update Bootstrap version in `base.html`
- **Icons**: Change Font Awesome version in `base.html`

### Functionality
- **Categories**: Add/modify categories in `models.py`
- **Priorities**: Adjust priority levels in `models.py`
- **Forms**: Customize forms in `forms.py`
- **Views**: Modify view logic in `views.py`

## Development

### Running Tests
```bash
python manage.py test
```

### Code Quality
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to classes and methods
- Keep functions under 20 lines when possible

### Adding New Features
1. Create models in `models.py`
2. Add forms in `forms.py`
3. Create views in `views.py`
4. Add URL patterns in `urls.py`
5. Create templates in `templates/`
6. Add static files in `static/`

## Production Deployment

### Environment Variables
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### Static Files
```bash
python manage.py collectstatic
# Configure web server to serve from STATIC_ROOT
```

### Database
- Use PostgreSQL for production
- Configure database settings in `settings.py`
- Set up database backups

### Security
- Change `SECRET_KEY`
- Set `DEBUG=False`
- Configure `ALLOWED_HOSTS`
- Use HTTPS
- Set up proper file permissions

## Troubleshooting

### Common Issues

#### Static Files Not Loading
```bash
python manage.py collectstatic
# Check STATIC_URL and STATIC_ROOT in settings.py
```

#### Database Errors
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Import Errors
- Ensure virtual environment is activated
- Check `INSTALLED_APPS` in settings.py
- Verify app is properly installed

#### Template Errors
- Check template file paths
- Verify template syntax
- Check context variables in views

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review Django documentation
3. Create an issue in the repository

## Acknowledgments

- Django framework and community
- Bootstrap team for the CSS framework
- Font Awesome for the icon library
- All contributors to this project

---

**Built with ❤️ using Django and modern web technologies**

