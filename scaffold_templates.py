import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}BackerWave{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .hero { background: linear-gradient(135deg, #0d6efd, #0dcaf0); color: white; padding: 100px 0; }
        .card-img-top { height: 200px; object-fit: cover; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'core:home' %}">BackerWave</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item"><a class="nav-link" href="{% url 'core:home' %}">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'campaigns:list' %}">Campaigns</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'core:about' %}">About</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'core:contact' %}">Contact</a></li>
                </ul>
                <ul class="navbar-nav">
                    {% if user.is_authenticated %}
                        {% if user.profile.user_type == 'CREATOR' %}
                            <li class="nav-item"><a class="nav-link" href="{% url 'campaigns:my_campaigns' %}">Dashboard</a></li>
                        {% endif %}
                        <li class="nav-item"><a class="nav-link" href="{% url 'accounts:profile' %}">Profile</a></li>
                        <li class="nav-item">
                            <form method="post" action="{% url 'accounts:logout' %}">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-link nav-link">Logout</button>
                            </form>
                        </li>
                    {% else %}
                        <li class="nav-item"><a class="nav-link" href="{% url 'accounts:login' %}">Login</a></li>
                        <li class="nav-item"><a class="nav-link" href="{% url 'accounts:register' %}">Register</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>

    <footer class="bg-dark text-white text-center py-4 mt-5">
        <p>&copy; 2026 BackerWave. All rights reserved.</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
write_file('templates/base.html', base_html)

core_home = """
{% extends 'base.html' %}

{% block content %}
<div class="hero rounded-3 text-center mb-5">
    <h1 class="display-4 fw-bold">Fund the Future</h1>
    <p class="lead">Join BackerWave to support innovative projects or launch your own.</p>
    <a href="{% url 'campaigns:create' %}" class="btn btn-primary btn-lg mt-3 me-2">Start a Campaign</a>
    <a href="{% url 'campaigns:list' %}" class="btn btn-outline-light btn-lg mt-3">Explore Campaigns</a>
</div>

<h2 class="mb-4">Featured Campaigns</h2>
<div class="row">
    {% for campaign in featured_campaigns %}
        <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
                {% if campaign.campaign_image %}
                    <img src="{{ campaign.campaign_image.url }}" class="card-img-top" alt="{{ campaign.title }}">
                {% else %}
                    <div class="card-img-top bg-secondary text-white d-flex align-items-center justify-content-center">No Image</div>
                {% endif %}
                <div class="card-body">
                    <h5 class="card-title">{{ campaign.title }}</h5>
                    <p class="card-text">{{ campaign.short_description }}</p>
                    <div class="progress mb-2">
                        <div class="progress-bar" role="progressbar" style="width: {{ campaign.progress_percentage }}%"></div>
                    </div>
                    <p class="small text-muted mb-0">${{ campaign.current_amount }} raised of ${{ campaign.goal_amount }}</p>
                </div>
                <div class="card-footer bg-white border-top-0">
                    <a href="{% url 'campaigns:detail' campaign.slug %}" class="btn btn-outline-primary w-100">View Details</a>
                </div>
            </div>
        </div>
    {% empty %}
        <p>No featured campaigns yet.</p>
    {% endfor %}
</div>
{% endblock %}
"""
write_file('templates/core/home.html', core_home)

core_about = "{% extends 'base.html' %}{% block content %}<h1>About Us</h1><p>Welcome to BackerWave.</p>{% endblock %}"
write_file('templates/core/about.html', core_about)
core_contact = "{% extends 'base.html' %}{% block content %}<h1>Contact</h1><p>Contact us here.</p>{% endblock %}"
write_file('templates/core/contact.html', core_contact)

accounts_register = """
{% extends 'base.html' %}
{% block title %}Register - BackerWave{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <h2 class="mb-4">Register</h2>
        <div class="card shadow-sm">
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary w-100">Register</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/accounts/register.html', accounts_register)

accounts_login = """
{% extends 'base.html' %}
{% block title %}Login - BackerWave{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <h2 class="mb-4">Login</h2>
        <div class="card shadow-sm">
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/accounts/login.html', accounts_login)

accounts_profile = """
{% extends 'base.html' %}
{% block title %}My Profile - BackerWave{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-4">
        <div class="card shadow-sm mb-4">
            <div class="card-body text-center">
                {% if user.profile.profile_image %}
                    <img src="{{ user.profile.profile_image.url }}" class="rounded-circle mb-3" width="150" height="150" style="object-fit:cover;">
                {% else %}
                    <div class="bg-secondary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width:150px; height:150px; font-size:3rem;">{{ user.username|make_list|first|upper }}</div>
                {% endif %}
                <h4>{{ user.profile.full_name }}</h4>
                <p class="text-muted">{{ user.profile.get_user_type_display }}</p>
                <a href="{% url 'accounts:edit_profile' %}" class="btn btn-outline-primary btn-sm">Edit Profile</a>
            </div>
        </div>
    </div>
    <div class="col-md-8">
        <div class="card shadow-sm">
            <div class="card-header bg-white"><h5 class="mb-0">Profile Information</h5></div>
            <div class="card-body">
                <p><strong>Username:</strong> {{ user.username }}</p>
                <p><strong>Email:</strong> {{ user.email }}</p>
                <p><strong>Phone:</strong> {{ user.profile.phone }}</p>
                <p><strong>Location:</strong> {{ user.profile.location }}</p>
                <p><strong>Bio:</strong> {{ user.profile.bio }}</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/accounts/profile.html', accounts_profile)

accounts_edit_profile = """
{% extends 'base.html' %}
{% block title %}Edit Profile - BackerWave{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <h2 class="mb-4">Edit Profile</h2>
        <div class="card shadow-sm">
            <div class="card-body">
                <form method="post" enctype="multipart/form-data">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary">Save Changes</button>
                    <a href="{% url 'accounts:profile' %}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/accounts/edit_profile.html', accounts_edit_profile)

campaigns_list = """
{% extends 'base.html' %}
{% block title %}Explore Campaigns - BackerWave{% endblock %}
{% block content %}
<div class="row mb-4">
    <div class="col-md-8">
        <h2>Explore Campaigns</h2>
    </div>
    <div class="col-md-4">
        <form method="get" class="d-flex">
            <input type="text" name="q" class="form-control me-2" placeholder="Search..." value="{{ request.GET.q }}">
            <button class="btn btn-outline-primary" type="submit">Search</button>
        </form>
    </div>
</div>

<div class="row mb-4">
    <div class="col-12">
        <div class="d-flex gap-2 flex-wrap">
            <a href="?{% if request.GET.q %}q={{ request.GET.q }}&{% endif %}" class="btn btn-sm {% if not request.GET.category %}btn-primary{% else %}btn-outline-primary{% endif %}">All</a>
            {% for cat in categories %}
                <a href="?category={{ cat.slug }}{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}" class="btn btn-sm {% if request.GET.category == cat.slug %}btn-primary{% else %}btn-outline-primary{% endif %}">{{ cat.name }}</a>
            {% endfor %}
            <div class="ms-auto d-flex gap-2 align-items-center">
                <span class="small text-muted">Sort by:</span>
                <a href="?-created_at" class="text-decoration-none small">Newest</a> | 
                <a href="?-current_amount" class="text-decoration-none small">Most Funded</a>
            </div>
        </div>
    </div>
</div>

<div class="row">
    {% for campaign in campaigns %}
        <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
                {% if campaign.campaign_image %}
                    <img src="{{ campaign.campaign_image.url }}" class="card-img-top" alt="{{ campaign.title }}">
                {% else %}
                    <div class="card-img-top bg-secondary text-white d-flex align-items-center justify-content-center">No Image</div>
                {% endif %}
                <div class="card-body">
                    <span class="badge bg-info mb-2">{{ campaign.category.name }}</span>
                    <h5 class="card-title">{{ campaign.title }}</h5>
                    <p class="card-text">{{ campaign.short_description|truncatechars:100 }}</p>
                    <div class="progress mb-2">
                        <div class="progress-bar bg-success" role="progressbar" style="width: {{ campaign.progress_percentage }}%"></div>
                    </div>
                    <div class="d-flex justify-content-between small text-muted">
                        <span>${{ campaign.current_amount }} raised</span>
                        <span>{{ campaign.progress_percentage|floatformat:0 }}%</span>
                    </div>
                </div>
                <div class="card-footer bg-white border-top-0 d-flex justify-content-between align-items-center">
                    <small class="text-muted">By {{ campaign.creator.username }}</small>
                    <a href="{% url 'campaigns:detail' campaign.slug %}" class="btn btn-sm btn-outline-primary">View</a>
                </div>
            </div>
        </div>
    {% empty %}
        <div class="col-12"><p class="text-center text-muted py-5">No campaigns found.</p></div>
    {% endfor %}
</div>
{% endblock %}
"""
write_file('templates/campaigns/list.html', campaigns_list)

campaigns_detail = """
{% extends 'base.html' %}
{% block title %}{{ campaign.title }} - BackerWave{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-8">
        <h1 class="mb-3">{{ campaign.title }}</h1>
        <p class="lead text-muted">{{ campaign.short_description }}</p>
        
        {% if campaign.campaign_image %}
            <img src="{{ campaign.campaign_image.url }}" class="img-fluid rounded mb-4 w-100" style="max-height: 400px; object-fit: cover;">
        {% else %}
            <div class="bg-secondary text-white rounded mb-4 d-flex align-items-center justify-content-center w-100" style="height: 400px;">No Image Available</div>
        {% endif %}
        
        <div class="mt-4">
            <h4>About this campaign</h4>
            <div class="mt-3">
                {{ campaign.description|linebreaks }}
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        <div class="card shadow-sm sticky-top" style="top: 20px;">
            <div class="card-body">
                <span class="badge bg-{{ campaign.status|lower|default:'primary' }} mb-2">{{ campaign.get_status_display }}</span>
                <span class="badge bg-info mb-2 ms-1">{{ campaign.category.name }}</span>
                
                <h2 class="mb-0">${{ campaign.current_amount }}</h2>
                <p class="text-muted small">raised of ${{ campaign.goal_amount }} goal</p>
                
                <div class="progress mb-3" style="height: 10px;">
                    <div class="progress-bar bg-success" role="progressbar" style="width: {{ campaign.progress_percentage }}%"></div>
                </div>
                
                <div class="d-flex justify-content-between mb-4">
                    <div class="text-center">
                        <h5 class="mb-0">{{ campaign.progress_percentage|floatformat:0 }}%</h5>
                        <small class="text-muted">Funded</small>
                    </div>
                    <div class="text-center">
                        <h5 class="mb-0">${{ campaign.remaining_amount }}</h5>
                        <small class="text-muted">Remaining</small>
                    </div>
                </div>
                
                <button class="btn btn-success btn-lg w-100 mb-3" {% if campaign.status != 'ACTIVE' %}disabled{% endif %}>Support This Campaign</button>
                
                <hr>
                
                <div class="d-flex align-items-center">
                    {% if campaign.creator.profile.profile_image %}
                        <img src="{{ campaign.creator.profile.profile_image.url }}" class="rounded-circle me-3" width="50" height="50">
                    {% else %}
                        <div class="bg-secondary text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="width:50px; height:50px;">{{ campaign.creator.username|make_list|first|upper }}</div>
                    {% endif %}
                    <div>
                        <p class="mb-0 fw-bold">{{ campaign.creator.profile.full_name|default:campaign.creator.username }}</p>
                        <small class="text-muted">Creator</small>
                    </div>
                </div>
                
                {% if request.user == campaign.creator %}
                <div class="mt-4 pt-3 border-top">
                    <a href="{% url 'campaigns:edit' campaign.slug %}" class="btn btn-outline-secondary btn-sm w-100 mb-2">Edit Campaign</a>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/campaigns/detail.html', campaigns_detail)

campaigns_my_campaigns = """
{% extends 'base.html' %}
{% block title %}Dashboard - BackerWave{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Creator Dashboard</h2>
    <a href="{% url 'campaigns:create' %}" class="btn btn-primary">Create New Campaign</a>
</div>

<div class="row mb-5">
    <div class="col-md-3">
        <div class="card bg-primary text-white text-center shadow-sm h-100">
            <div class="card-body">
                <h3>{{ total_campaigns }}</h3>
                <p class="mb-0">Total Campaigns</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card bg-success text-white text-center shadow-sm h-100">
            <div class="card-body">
                <h3>{{ active_campaigns }}</h3>
                <p class="mb-0">Active Campaigns</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card bg-info text-white text-center shadow-sm h-100">
            <div class="card-body">
                <h3>${{ total_raised }}</h3>
                <p class="mb-0">Total Raised</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card bg-warning text-dark text-center shadow-sm h-100">
            <div class="card-body">
                <h3>{{ total_contributors }}</h3>
                <p class="mb-0">Total Contributors</p>
            </div>
        </div>
    </div>
</div>

<h4 class="mb-3">My Campaigns</h4>
<div class="table-responsive">
    <table class="table table-hover align-middle">
        <thead class="table-light">
            <tr>
                <th>Campaign</th>
                <th>Status</th>
                <th>Goal</th>
                <th>Raised</th>
                <th>Progress</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for campaign in campaigns %}
            <tr>
                <td>
                    <div class="d-flex align-items-center">
                        {% if campaign.campaign_image %}
                            <img src="{{ campaign.campaign_image.url }}" class="rounded me-2" width="40" height="40" style="object-fit:cover;">
                        {% endif %}
                        <div>
                            <div class="fw-bold">{{ campaign.title }}</div>
                            <small class="text-muted">{{ campaign.start_date|date:"M d, Y" }} - {{ campaign.end_date|date:"M d, Y" }}</small>
                        </div>
                    </div>
                </td>
                <td><span class="badge bg-{{ campaign.status|lower|default:'secondary' }}">{{ campaign.get_status_display }}</span></td>
                <td>${{ campaign.goal_amount }}</td>
                <td>${{ campaign.current_amount }}</td>
                <td>
                    <div class="progress" style="width: 80px; height: 10px;">
                        <div class="progress-bar bg-success" style="width: {{ campaign.progress_percentage }}%"></div>
                    </div>
                    <small>{{ campaign.progress_percentage|floatformat:0 }}%</small>
                </td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <a href="{% url 'campaigns:detail' campaign.slug %}" class="btn btn-outline-info">View</a>
                        <a href="{% url 'campaigns:edit' campaign.slug %}" class="btn btn-outline-secondary">Edit</a>
                        <a href="{% url 'campaigns:delete' campaign.slug %}" class="btn btn-outline-danger">Delete</a>
                    </div>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="6" class="text-center py-4">You haven't created any campaigns yet.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
"""
write_file('templates/campaigns/my_campaigns.html', campaigns_my_campaigns)

campaigns_form = """
{% extends 'base.html' %}
{% block title %}{{ title }} - BackerWave{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <h2 class="mb-4">{{ title }}</h2>
        <div class="card shadow-sm">
            <div class="card-body">
                <form method="post" enctype="multipart/form-data">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <div class="d-flex gap-2 mt-4">
                        <button type="submit" class="btn btn-primary">Save Campaign</button>
                        <a href="{% url 'campaigns:my_campaigns' %}" class="btn btn-outline-secondary">Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/campaigns/form.html', campaigns_form)

campaigns_confirm_delete = """
{% extends 'base.html' %}
{% block title %}Delete {{ campaign.title }}{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card border-danger mb-3">
            <div class="card-header bg-danger text-white">Confirm Deletion</div>
            <div class="card-body">
                <h5 class="card-title">Are you sure you want to delete "{{ campaign.title }}"?</h5>
                <p class="card-text text-danger">This action cannot be undone.</p>
                <form method="post">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-danger">Yes, Delete Campaign</button>
                    <a href="{% url 'campaigns:my_campaigns' %}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/campaigns/confirm_delete.html', campaigns_confirm_delete)
