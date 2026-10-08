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

# 1. Update base.html to include Notifications count in navbar and link to favorites
base_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}BackerWave{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <style>
        body { d-flex flex-column min-vh-100; }
        .hero { background: linear-gradient(135deg, #0d6efd, #0dcaf0); color: white; padding: 100px 0; }
        .card-img-top { height: 200px; object-fit: cover; }
        .card { transition: transform 0.2s ease, box-shadow 0.2s ease; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important; }
        .nav-link { font-weight: 500; }
        .footer { margin-top: auto; }
    </style>
</head>
<body class="d-flex flex-column min-vh-100 bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
        <div class="container">
            <a class="navbar-brand fw-bold" href="{% url 'core:home' %}"><i class="bi bi-water"></i> BackerWave</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item"><a class="nav-link" href="{% url 'core:home' %}">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'campaigns:list' %}">Explore Campaigns</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'core:about' %}">About</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'core:contact' %}">Contact</a></li>
                </ul>
                <ul class="navbar-nav align-items-center">
                    {% if user.is_authenticated %}
                        <li class="nav-item me-2">
                            <a class="nav-link position-relative" href="{% url 'core:notifications' %}">
                                <i class="bi bi-bell fs-5"></i>
                                {% if unread_notifications_count %}
                                <span class="position-absolute top-25 start-75 translate-middle badge rounded-pill bg-danger" style="font-size: 0.6rem;">
                                    {{ unread_notifications_count }}
                                </span>
                                {% endif %}
                            </a>
                        </li>
                        <li class="nav-item"><a class="nav-link" href="{% url 'campaigns:favorites' %}"><i class="bi bi-heart"></i> Favorites</a></li>
                        
                        {% if user.profile.user_type == 'CREATOR' %}
                            <li class="nav-item"><a class="nav-link" href="{% url 'campaigns:my_campaigns' %}">Dashboard</a></li>
                        {% else %}
                            <li class="nav-item"><a class="nav-link" href="{% url 'contributions:dashboard' %}">Dashboard</a></li>
                        {% endif %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                                <i class="bi bi-person-circle"></i> {{ user.username }}
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li><a class="dropdown-item" href="{% url 'accounts:profile' %}">Profile</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li>
                                    <form method="post" action="{% url 'accounts:logout' %}">
                                        {% csrf_token %}
                                        <button type="submit" class="dropdown-item">Logout</button>
                                    </form>
                                </li>
                            </ul>
                        </li>
                    {% else %}
                        <li class="nav-item"><a class="nav-link" href="{% url 'accounts:login' %}">Login</a></li>
                        <li class="nav-item"><a class="btn btn-primary ms-2" href="{% url 'accounts:register' %}">Register</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4 mb-5 flex-grow-1">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show shadow-sm">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>

    <footer class="footer bg-dark text-white pt-5 pb-3">
        <div class="container">
            <div class="row">
                <div class="col-md-4 mb-3">
                    <h5><i class="bi bi-water"></i> BackerWave</h5>
                    <p class="text-muted small">Empowering creators and backers to bring innovative ideas to life through community funding.</p>
                </div>
                <div class="col-md-4 mb-3">
                    <h5>Links</h5>
                    <ul class="list-unstyled">
                        <li><a href="{% url 'core:about' %}" class="text-muted text-decoration-none">About Us</a></li>
                        <li><a href="{% url 'campaigns:list' %}" class="text-muted text-decoration-none">Explore</a></li>
                        <li><a href="{% url 'core:contact' %}" class="text-muted text-decoration-none">Contact</a></li>
                    </ul>
                </div>
                <div class="col-md-4 mb-3">
                    <h5>Connect</h5>
                    <a href="#" class="text-white me-2 fs-4"><i class="bi bi-twitter"></i></a>
                    <a href="#" class="text-white me-2 fs-4"><i class="bi bi-facebook"></i></a>
                    <a href="#" class="text-white fs-4"><i class="bi bi-instagram"></i></a>
                </div>
            </div>
            <hr class="border-secondary">
            <div class="text-center text-muted small">
                &copy; 2026 BackerWave. All rights reserved.
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
write_file('templates/base.html', base_html)

# 2. Add favorite button to Campaign Details
replace_in_file('templates/campaigns/detail.html',
    '<h1 class="mb-3">{{ campaign.title }}</h1>',
    """
    <div class="d-flex justify-content-between align-items-start mb-3">
        <h1 class="mb-0">{{ campaign.title }}</h1>
        {% if user.is_authenticated and campaign.status == 'ACTIVE' %}
            <form method="post" action="{% url 'campaigns:favorite' campaign.slug %}">
                {% csrf_token %}
                <button type="submit" class="btn btn-outline-danger">
                    {% if is_favorited %}
                        <i class="bi bi-heart-fill"></i> Unfavorite
                    {% else %}
                        <i class="bi bi-heart"></i> Favorite & Follow
                    {% endif %}
                </button>
            </form>
        {% endif %}
    </div>
    """)

# Change creator link to public profile
replace_in_file('templates/campaigns/detail.html',
    '<p class="mb-0 fw-bold">{{ campaign.creator.profile.full_name|default:campaign.creator.username }}</p>',
    '<p class="mb-0 fw-bold"><a href="{% url \'campaigns:creator_profile\' campaign.creator.username %}" class="text-decoration-none text-dark">{{ campaign.creator.profile.full_name|default:campaign.creator.username }}</a></p>')

# 3. Create core/notifications.html
core_notifications = """
{% extends 'base.html' %}
{% block title %}Notifications{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="bi bi-bell"></i> Notifications</h2>
            {% if notifications %}
            <form method="post" action="{% url 'core:mark_all_read' %}">
                {% csrf_token %}
                <button type="submit" class="btn btn-sm btn-outline-secondary">Mark all as read</button>
            </form>
            {% endif %}
        </div>
        
        <div class="list-group shadow-sm">
            {% for notification in notifications %}
                <div class="list-group-item list-group-item-action {% if not notification.is_read %}list-group-item-primary{% endif %}">
                    <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-1">{{ notification.title }}</h5>
                        <small class="text-muted">{{ notification.created_at|timesince }} ago</small>
                    </div>
                    <p class="mb-1">{{ notification.message }}</p>
                    {% if not notification.is_read %}
                        <form method="post" action="{% url 'core:mark_read' notification.id %}" class="mt-2">
                            {% csrf_token %}
                            <button type="submit" class="btn btn-sm btn-primary">Mark as Read & View</button>
                        </form>
                    {% endif %}
                </div>
            {% empty %}
                <div class="list-group-item text-center py-5 text-muted">
                    <i class="bi bi-bell-slash fs-1 d-block mb-2"></i>
                    You have no notifications.
                </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/core/notifications.html', core_notifications)

# 4. Create campaigns/favorites.html
campaigns_favorites = """
{% extends 'base.html' %}
{% block title %}My Favorites{% endblock %}
{% block content %}
<h2 class="mb-4"><i class="bi bi-heart-fill text-danger"></i> Favorite Campaigns</h2>

<div class="row">
    {% for fav in favorites %}
        <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
                {% if fav.campaign.campaign_image %}
                    <img src="{{ fav.campaign.campaign_image.url }}" class="card-img-top">
                {% else %}
                    <div class="card-img-top bg-secondary text-white d-flex align-items-center justify-content-center">No Image</div>
                {% endif %}
                <div class="card-body">
                    <h5 class="card-title">{{ fav.campaign.title }}</h5>
                    <p class="card-text text-muted small">{{ fav.campaign.short_description|truncatechars:80 }}</p>
                    <div class="progress mb-2" style="height: 6px;">
                        <div class="progress-bar bg-success" style="width: {{ fav.campaign.progress_percentage }}%"></div>
                    </div>
                    <div class="d-flex justify-content-between small">
                        <span>${{ fav.campaign.current_amount }} raised</span>
                        <span class="badge bg-{{ fav.campaign.status|lower|default:'primary' }}">{{ fav.campaign.get_status_display }}</span>
                    </div>
                </div>
                <div class="card-footer bg-white border-top-0 d-flex gap-2">
                    <a href="{% url 'campaigns:detail' fav.campaign.slug %}" class="btn btn-sm btn-outline-primary w-100">View</a>
                    <form method="post" action="{% url 'campaigns:favorite' fav.campaign.slug %}" class="w-100">
                        {% csrf_token %}
                        <button type="submit" class="btn btn-sm btn-outline-danger w-100"><i class="bi bi-trash"></i> Remove</button>
                    </form>
                </div>
            </div>
        </div>
    {% empty %}
        <div class="col-12 text-center py-5">
            <h4 class="text-muted">You haven't favorited any campaigns yet.</h4>
            <a href="{% url 'campaigns:list' %}" class="btn btn-primary mt-3">Explore Campaigns</a>
        </div>
    {% endfor %}
</div>
{% endblock %}
"""
write_file('templates/campaigns/favorites.html', campaigns_favorites)

# 5. Create core/contact.html
core_contact = """
{% extends 'base.html' %}
{% block title %}Contact Us{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="text-center mb-4">
            <h2>Contact Us</h2>
            <p class="text-muted">Have a question or need support? Drop us a message.</p>
        </div>
        <div class="card shadow-sm">
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary w-100 mt-2">Send Message</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/core/contact.html', core_contact)

# 6. Public Creator Profile
creator_profile = """
{% extends 'base.html' %}
{% block title %}{{ creator.profile.full_name|default:creator.username }} - Creator Profile{% endblock %}
{% block content %}
<div class="row mb-5">
    <div class="col-md-4 text-center mb-4">
        {% if creator.profile.profile_image %}
            <img src="{{ creator.profile.profile_image.url }}" class="rounded-circle shadow" width="200" height="200" style="object-fit:cover;">
        {% else %}
            <div class="bg-primary text-white rounded-circle shadow d-inline-flex align-items-center justify-content-center" style="width:200px; height:200px; font-size:4rem;">{{ creator.username|make_list|first|upper }}</div>
        {% endif %}
        <h2 class="mt-3 mb-1">{{ creator.profile.full_name|default:creator.username }}</h2>
        <p class="text-muted mb-2"><i class="bi bi-geo-alt"></i> {{ creator.profile.location|default:"Location hidden" }}</p>
        <p class="small text-muted">Joined {{ creator.date_joined|date:"M Y" }}</p>
    </div>
    <div class="col-md-8">
        <div class="card shadow-sm h-100">
            <div class="card-body">
                <h4 class="mb-3">About the Creator</h4>
                <p>{{ creator.profile.bio|default:"This creator hasn't written a bio yet."|linebreaks }}</p>
                <hr>
                <div class="row text-center mt-4">
                    <div class="col">
                        <h3 class="text-primary">{{ campaigns.count }}</h3>
                        <span class="text-muted small">Active Campaigns</span>
                    </div>
                    <div class="col">
                        <h3 class="text-success">{{ completed_count }}</h3>
                        <span class="text-muted small">Successful Projects</span>
                    </div>
                    <div class="col">
                        <h3 class="text-info">${{ total_raised }}</h3>
                        <span class="text-muted small">Total Raised</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<h3 class="mb-4">Active Campaigns by {{ creator.username }}</h3>
<div class="row">
    {% for campaign in campaigns %}
        <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
                {% if campaign.campaign_image %}
                    <img src="{{ campaign.campaign_image.url }}" class="card-img-top">
                {% else %}
                    <div class="card-img-top bg-secondary text-white d-flex align-items-center justify-content-center">No Image</div>
                {% endif %}
                <div class="card-body">
                    <h5 class="card-title">{{ campaign.title }}</h5>
                    <p class="card-text text-muted small">{{ campaign.short_description|truncatechars:80 }}</p>
                    <div class="progress mb-2" style="height: 6px;">
                        <div class="progress-bar bg-success" style="width: {{ campaign.progress_percentage }}%"></div>
                    </div>
                    <div class="d-flex justify-content-between small">
                        <span>${{ campaign.current_amount }} raised</span>
                        <span>{{ campaign.progress_percentage|floatformat:0 }}%</span>
                    </div>
                </div>
                <div class="card-footer bg-white border-top-0">
                    <a href="{% url 'campaigns:detail' campaign.slug %}" class="btn btn-outline-primary w-100">View Campaign</a>
                </div>
            </div>
        </div>
    {% empty %}
        <p class="text-muted">No active campaigns at the moment.</p>
    {% endfor %}
</div>
{% endblock %}
"""
write_file('templates/campaigns/creator_profile.html', creator_profile)

# 7. Update core/about.html
core_about = """
{% extends 'base.html' %}
{% block title %}About Us{% endblock %}
{% block content %}
<div class="row justify-content-center text-center py-5">
    <div class="col-md-8">
        <h1 class="display-4 fw-bold text-primary mb-4">Empowering Innovation</h1>
        <p class="lead text-muted">BackerWave is a community-driven crowdfunding platform built to bring visionary projects to life. We connect passionate creators with backers who believe in the future.</p>
    </div>
</div>
<div class="row mt-4">
    <div class="col-md-4 text-center mb-4">
        <i class="bi bi-lightbulb text-warning" style="font-size: 3rem;"></i>
        <h4 class="mt-3">Discover</h4>
        <p class="text-muted">Find groundbreaking projects across technology, art, education, and social causes.</p>
    </div>
    <div class="col-md-4 text-center mb-4">
        <i class="bi bi-piggy-bank text-success" style="font-size: 3rem;"></i>
        <h4 class="mt-3">Support</h4>
        <p class="text-muted">Back the projects you love securely and transparently. Track their progress directly.</p>
    </div>
    <div class="col-md-4 text-center mb-4">
        <i class="bi bi-rocket text-primary" style="font-size: 3rem;"></i>
        <h4 class="mt-3">Launch</h4>
        <p class="text-muted">Are you a creator? Launch your campaign today and reach thousands of potential backers.</p>
    </div>
</div>
<div class="card bg-primary text-white mt-5 shadow">
    <div class="card-body py-5 text-center">
        <h2 class="mb-4">Platform Impact</h2>
        <div class="row">
            <div class="col-md-4">
                <h1 class="fw-bold">{{ stats.total_campaigns }}</h1>
                <p>Total Campaigns</p>
            </div>
            <div class="col-md-4">
                <h1 class="fw-bold">${{ stats.total_raised }}</h1>
                <p>Funds Raised</p>
            </div>
            <div class="col-md-4">
                <h1 class="fw-bold">{{ stats.total_contributors }}</h1>
                <p>Active Backers</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/core/about.html', core_about)

# 8. Create Error Pages
err_404 = """
{% extends 'base.html' %}
{% block content %}
<div class="text-center py-5">
    <h1 class="display-1 text-primary">404</h1>
    <h2>Page Not Found</h2>
    <p class="text-muted mb-4">The page you are looking for does not exist or has been moved.</p>
    <a href="{% url 'core:home' %}" class="btn btn-primary">Return Home</a>
</div>
{% endblock %}
"""
write_file('templates/404.html', err_404)
write_file('templates/403.html', err_404.replace('404', '403').replace('Page Not Found', 'Forbidden').replace('does not exist or has been moved', 'is restricted and you do not have permission to view it'))
write_file('templates/500.html', err_404.replace('404', '500').replace('Page Not Found', 'Server Error').replace('does not exist or has been moved', 'encountered an internal error. Please try again later'))
