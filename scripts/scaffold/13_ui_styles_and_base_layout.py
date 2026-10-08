import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

# 1. CSS Architecture
css_variables = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    /* Colors */
    --primary: #2563eb;
    --primary-hover: #1d4ed8;
    --background: #f8fafc;
    --surface: #ffffff;
    --surface-muted: #f1f5f9;
    
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #94a3b8;
    --border: #e2e8f0;
    
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --info: #3b82f6;

    /* Spacing */
    --spacing-1: 4px;
    --spacing-2: 8px;
    --spacing-3: 12px;
    --spacing-4: 16px;
    --spacing-5: 24px;
    --spacing-6: 32px;
    --spacing-8: 48px;
    --spacing-10: 64px;
    --spacing-12: 80px;

    /* Radius */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 16px;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    
    /* Typography */
    --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
}

body {
    font-family: var(--font-sans);
    background-color: var(--background);
    color: var(--text-primary);
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
}

/* Typography Hierarchy */
h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: var(--spacing-4);
    line-height: 1.2;
}

.display { font-size: clamp(3rem, 5vw, 4rem); letter-spacing: -0.02em; font-weight: 700; }
h1 { font-size: clamp(2rem, 3vw, 2.5rem); letter-spacing: -0.01em; }
h2 { font-size: clamp(1.5rem, 2vw, 2rem); }
h3 { font-size: 1.5rem; }
h4 { font-size: 1.25rem; }
.text-body { font-size: 1rem; color: var(--text-secondary); }
.text-small { font-size: 0.875rem; color: var(--text-secondary); }
.text-caption { font-size: 0.75rem; color: var(--text-muted); }

/* Links */
a {
    color: var(--primary);
    text-decoration: none;
    transition: color 0.2s ease;
}
a:hover { color: var(--primary-hover); }

/* Overriding Bootstrap */
.btn {
    font-weight: 500;
    border-radius: var(--radius-md);
    padding: 0.5rem 1rem;
    transition: all 0.2s ease;
    box-shadow: var(--shadow-sm);
}
.btn-primary {
    background-color: var(--primary);
    border-color: var(--primary);
}
.btn-primary:hover {
    background-color: var(--primary-hover);
    border-color: var(--primary-hover);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}
.btn-outline-primary {
    color: var(--primary);
    border-color: var(--primary);
}
.btn-outline-primary:hover {
    background-color: var(--primary);
    color: white;
}
.card {
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    overflow: hidden;
}
.card:hover {
    box-shadow: var(--shadow-md);
}
.form-control, .form-select {
    border-radius: var(--radius-md);
    border-color: var(--border);
    padding: 0.75rem 1rem;
    font-size: 0.95rem;
}
.form-control:focus, .form-select:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* Custom Components */
.campaign-card-img {
    height: 220px;
    object-fit: cover;
    width: 100%;
}
.progress {
    height: 8px;
    border-radius: var(--radius-sm);
    background-color: var(--surface-muted);
}
.progress-bar {
    background-color: var(--success);
}
.badge-custom {
    padding: 0.35em 0.65em;
    font-weight: 500;
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
}

/* Layout Utilities */
.section-padding {
    padding: var(--spacing-10) 0;
}
.bg-surface { background-color: var(--surface); }
.border-subtle { border-color: var(--border) !important; }

/* Navbar */
.navbar-custom {
    background-color: var(--surface) !important;
    border-bottom: 1px solid var(--border);
    padding: var(--spacing-3) 0;
}
.navbar-custom .navbar-brand {
    color: var(--text-primary) !important;
    font-weight: 700;
    letter-spacing: -0.02em;
    font-size: 1.5rem;
}
.navbar-custom .nav-link {
    color: var(--text-secondary) !important;
    font-weight: 500;
}
.navbar-custom .nav-link:hover {
    color: var(--primary) !important;
}
"""
write_file('static/css/custom.css', css_variables)

# 2. Base Template
base_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}BackerWave{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <link rel="stylesheet" href="{% load static %}{% static 'css/custom.css' %}">
</head>
<body class="d-flex flex-column min-vh-100">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-custom sticky-top">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center gap-2" href="{% url 'core:home' %}">
                <i class="bi bi-layers-fill text-primary"></i> BackerWave
            </a>
            <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <i class="bi bi-list fs-1 text-dark"></i>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item"><a class="nav-link" href="{% url 'campaigns:list' %}">Explore</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'core:about' %}">How it Works</a></li>
                </ul>
                <div class="d-flex align-items-center gap-3 flex-wrap">
                    <form action="{% url 'campaigns:list' %}" method="get" class="position-relative d-none d-lg-block">
                        <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                        <input type="text" name="q" class="form-control rounded-pill ps-5 bg-light border-0" placeholder="Search projects..." style="width: 250px;">
                    </form>
                    
                    {% if user.is_authenticated %}
                        <a href="{% url 'core:notifications' %}" class="position-relative text-dark text-decoration-none fs-5">
                            <i class="bi bi-bell"></i>
                            {% if unread_notifications_count %}
                                <span class="position-absolute top-0 start-100 translate-middle p-1 bg-danger border border-light rounded-circle">
                                    <span class="visually-hidden">New alerts</span>
                                </span>
                            {% endif %}
                        </a>
                        
                        <div class="dropdown">
                            <a class="d-flex align-items-center text-decoration-none dropdown-toggle text-dark fw-medium" href="#" role="button" data-bs-toggle="dropdown">
                                {% if user.profile.profile_image %}
                                    <img src="{{ user.profile.profile_image.url }}" width="32" height="32" class="rounded-circle me-2 object-fit-cover">
                                {% else %}
                                    <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center me-2" style="width:32px; height:32px; font-size:0.8rem;">
                                        {{ user.username|make_list|first|upper }}
                                    </div>
                                {% endif %}
                                {{ user.username }}
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end shadow-sm border-0 mt-2">
                                {% if user.profile.user_type == 'CREATOR' %}
                                    <li><a class="dropdown-item py-2" href="{% url 'campaigns:my_campaigns' %}"><i class="bi bi-grid me-2"></i> Dashboard</a></li>
                                {% else %}
                                    <li><a class="dropdown-item py-2" href="{% url 'contributions:dashboard' %}"><i class="bi bi-grid me-2"></i> Dashboard</a></li>
                                {% endif %}
                                <li><a class="dropdown-item py-2" href="{% url 'campaigns:favorites' %}"><i class="bi bi-heart me-2"></i> Favorites</a></li>
                                <li><a class="dropdown-item py-2" href="{% url 'accounts:profile' %}"><i class="bi bi-person me-2"></i> Profile</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li>
                                    <form method="post" action="{% url 'accounts:logout' %}">
                                        {% csrf_token %}
                                        <button type="submit" class="dropdown-item py-2 text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</button>
                                    </form>
                                </li>
                            </ul>
                        </div>
                        {% if user.profile.user_type == 'CREATOR' %}
                            <a href="{% url 'campaigns:create' %}" class="btn btn-primary d-none d-lg-block">Start a Campaign</a>
                        {% endif %}
                    {% else %}
                        <a href="{% url 'accounts:login' %}" class="text-decoration-none text-dark fw-medium">Log In</a>
                        <a href="{% url 'accounts:register' %}" class="btn btn-primary px-4">Sign Up</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </nav>

    <main class="flex-grow-1">
        {% if messages %}
            <div class="container mt-4 position-relative" style="z-index: 1050;">
                {% for message in messages %}
                    <div class="alert alert-{{ message.tags|default:'info' }} alert-dismissible fade show shadow-sm border-0 d-flex align-items-center" role="alert">
                        {% if message.tags == 'success' %}<i class="bi bi-check-circle-fill text-success fs-4 me-3"></i>{% endif %}
                        {% if message.tags == 'error' %}<i class="bi bi-exclamation-triangle-fill text-danger fs-4 me-3"></i>{% endif %}
                        <div>{{ message }}</div>
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
        
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-white border-top border-subtle pt-5 pb-4 mt-auto">
        <div class="container">
            <div class="row gy-4 mb-4">
                <div class="col-lg-4">
                    <h5 class="fw-bold mb-3 d-flex align-items-center gap-2"><i class="bi bi-layers-fill text-primary"></i> BackerWave</h5>
                    <p class="text-muted text-small pe-lg-5">Fund ideas that matter. We connect passionate creators with a community of backers to bring visionary projects to life.</p>
                </div>
                <div class="col-6 col-lg-2 offset-lg-1">
                    <h6 class="fw-bold mb-3">Discover</h6>
                    <ul class="list-unstyled text-small">
                        <li class="mb-2"><a href="{% url 'campaigns:list' %}" class="text-muted text-decoration-none">Explore Projects</a></li>
                        <li class="mb-2"><a href="#" class="text-muted text-decoration-none">Success Stories</a></li>
                    </ul>
                </div>
                <div class="col-6 col-lg-2">
                    <h6 class="fw-bold mb-3">About</h6>
                    <ul class="list-unstyled text-small">
                        <li class="mb-2"><a href="{% url 'core:about' %}" class="text-muted text-decoration-none">How it Works</a></li>
                        <li class="mb-2"><a href="{% url 'core:contact' %}" class="text-muted text-decoration-none">Contact Us</a></li>
                    </ul>
                </div>
                <div class="col-lg-3 text-lg-end">
                    <h6 class="fw-bold mb-3">Connect</h6>
                    <div class="d-flex gap-3 justify-content-lg-end">
                        <a href="#" class="text-muted"><i class="bi bi-twitter fs-5"></i></a>
                        <a href="#" class="text-muted"><i class="bi bi-instagram fs-5"></i></a>
                        <a href="#" class="text-muted"><i class="bi bi-linkedin fs-5"></i></a>
                    </div>
                </div>
            </div>
            <div class="border-top border-subtle pt-4 d-flex flex-column flex-md-row justify-content-between align-items-center text-muted text-small">
                <span>&copy; 2026 BackerWave. All rights reserved.</span>
                <div class="d-flex gap-3 mt-3 mt-md-0">
                    <a href="#" class="text-muted text-decoration-none">Privacy Policy</a>
                    <a href="#" class="text-muted text-decoration-none">Terms of Service</a>
                </div>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Auto-dismiss alerts after 5 seconds
        setTimeout(function() {
            var alerts = document.querySelectorAll('.alert');
            alerts.forEach(function(alert) {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            });
        }, 5000);
    </script>
</body>
</html>
"""
write_file('templates/base.html', base_html)

# 3. Component: Campaign Card
campaign_card_html = """
<div class="card h-100 border-0 shadow-sm campaign-card group cursor-pointer text-decoration-none text-dark d-flex flex-column">
    <a href="{% url 'campaigns:detail' campaign.slug %}" class="text-decoration-none text-dark d-flex flex-column h-100">
        <div class="position-relative">
            {% if campaign.campaign_image %}
                <img src="{{ campaign.campaign_image.url }}" class="campaign-card-img" alt="{{ campaign.title }}">
            {% else %}
                <div class="campaign-card-img bg-light d-flex align-items-center justify-content-center text-muted">
                    <i class="bi bi-image fs-1"></i>
                </div>
            {% endif %}
            <span class="badge bg-white text-primary position-absolute top-0 end-0 m-3 px-3 py-2 shadow-sm rounded-pill fw-medium border">
                {{ campaign.category.name }}
            </span>
        </div>
        
        <div class="card-body d-flex flex-column p-4">
            <h5 class="card-title fw-bold text-truncate mb-2">{{ campaign.title }}</h5>
            <p class="text-muted text-small mb-3" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
                {{ campaign.short_description }}
            </p>
            
            <div class="d-flex align-items-center gap-2 mb-4 mt-auto">
                {% if campaign.creator.profile.profile_image %}
                    <img src="{{ campaign.creator.profile.profile_image.url }}" class="rounded-circle object-fit-cover" width="24" height="24">
                {% else %}
                    <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center" style="width:24px; height:24px; font-size:10px;">
                        {{ campaign.creator.username|make_list|first|upper }}
                    </div>
                {% endif %}
                <span class="text-small fw-medium">By {{ campaign.creator.profile.full_name|default:campaign.creator.username }}</span>
            </div>
            
            <div class="progress-section mt-auto">
                <div class="d-flex justify-content-between text-small fw-medium mb-2">
                    <span class="text-success">${{ campaign.current_amount }} raised</span>
                    <span class="text-muted">{{ campaign.progress_percentage|floatformat:0 }}%</span>
                </div>
                <div class="progress mb-3">
                    <div class="progress-bar" role="progressbar" style="width: {{ campaign.progress_percentage }}%"></div>
                </div>
                <div class="d-flex justify-content-between text-muted text-caption fw-medium">
                    <span>Goal: ${{ campaign.goal_amount }}</span>
                    <span><i class="bi bi-clock"></i> {{ campaign.end_date|timeuntil }} left</span>
                </div>
            </div>
        </div>
    </a>
</div>
"""
write_file('templates/components/campaign_card.html', campaign_card_html)
