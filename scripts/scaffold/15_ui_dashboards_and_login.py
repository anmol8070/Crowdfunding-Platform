import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

# 7. Creator Dashboard (campaigns/my_campaigns.html)
creator_dashboard_html = """
{% extends 'base.html' %}
{% block title %}Creator Dashboard - BackerWave{% endblock %}

{% block content %}
<div class="bg-surface py-4 border-bottom border-subtle">
    <div class="container d-flex justify-content-between align-items-center">
        <div>
            <h2 class="fw-bold mb-1">Good morning, {{ user.username }}</h2>
            <p class="text-muted mb-0">Here's what's happening with your projects.</p>
        </div>
        <a href="{% url 'campaigns:create' %}" class="btn btn-primary fw-bold shadow-sm d-none d-md-block"><i class="bi bi-plus-lg me-2"></i> Create Campaign</a>
    </div>
</div>

<div class="container py-5">
    <!-- Stat Cards -->
    <div class="row gy-4 mb-5">
        <div class="col-sm-6 col-lg-3">
            <div class="card border-subtle shadow-sm rounded-4 h-100">
                <div class="card-body p-4">
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <h6 class="text-muted fw-bold text-uppercase mb-0">Total Raised</h6>
                        <i class="bi bi-cash-stack text-success fs-4"></i>
                    </div>
                    <h2 class="fw-bold mb-0">${{ total_raised|default:"0" }}</h2>
                </div>
            </div>
        </div>
        <div class="col-sm-6 col-lg-3">
            <div class="card border-subtle shadow-sm rounded-4 h-100">
                <div class="card-body p-4">
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <h6 class="text-muted fw-bold text-uppercase mb-0">Active Projects</h6>
                        <i class="bi bi-rocket-takeoff text-primary fs-4"></i>
                    </div>
                    <h2 class="fw-bold mb-0">{{ active_campaigns|default:"0" }}</h2>
                </div>
            </div>
        </div>
        <div class="col-sm-6 col-lg-3">
            <div class="card border-subtle shadow-sm rounded-4 h-100">
                <div class="card-body p-4">
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <h6 class="text-muted fw-bold text-uppercase mb-0">Total Backers</h6>
                        <i class="bi bi-people text-info fs-4"></i>
                    </div>
                    <h2 class="fw-bold mb-0">{{ total_contributors|default:"0" }}</h2>
                </div>
            </div>
        </div>
        <div class="col-sm-6 col-lg-3">
            <div class="card border-subtle shadow-sm rounded-4 h-100">
                <div class="card-body p-4">
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <h6 class="text-muted fw-bold text-uppercase mb-0">Success Rate</h6>
                        <i class="bi bi-check-circle text-warning fs-4"></i>
                    </div>
                    <h2 class="fw-bold mb-0">{% widthratio completed_campaigns total_campaigns|default:1 100 %}%</h2>
                </div>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="row gy-5">
        <!-- Campaigns List -->
        <div class="col-lg-8">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h4 class="fw-bold mb-0">Your Campaigns</h4>
                <a href="{% url 'campaigns:create' %}" class="btn btn-sm btn-outline-primary d-md-none"><i class="bi bi-plus-lg"></i> Create</a>
            </div>
            
            <div class="card border-subtle shadow-sm rounded-4 overflow-hidden">
                <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="table-light">
                            <tr>
                                <th class="ps-4 text-uppercase text-muted text-small fw-bold">Project</th>
                                <th class="text-uppercase text-muted text-small fw-bold">Status</th>
                                <th class="text-uppercase text-muted text-small fw-bold">Funding</th>
                                <th class="pe-4 text-end text-uppercase text-muted text-small fw-bold">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for campaign in campaigns %}
                            <tr>
                                <td class="ps-4 py-3">
                                    <div class="fw-bold text-dark">{{ campaign.title }}</div>
                                    <div class="text-muted text-small">{{ campaign.contributions.count }} backers</div>
                                </td>
                                <td>
                                    <span class="badge bg-{{ campaign.status|lower|default:'secondary' }} fw-medium rounded-pill px-2 py-1">{{ campaign.get_status_display }}</span>
                                </td>
                                <td>
                                    <div class="fw-medium">${{ campaign.current_amount }}</div>
                                    <div class="progress mt-1" style="height: 4px; width: 100px;">
                                        <div class="progress-bar bg-success" style="width: {{ campaign.progress_percentage }}%"></div>
                                    </div>
                                </td>
                                <td class="pe-4 text-end">
                                    <div class="dropdown">
                                        <button class="btn btn-light btn-sm rounded-circle" type="button" data-bs-toggle="dropdown"><i class="bi bi-three-dots-vertical"></i></button>
                                        <ul class="dropdown-menu dropdown-menu-end shadow-sm border-subtle">
                                            <li><a class="dropdown-item" href="{% url 'campaigns:detail' campaign.slug %}"><i class="bi bi-eye me-2 text-muted"></i> View Page</a></li>
                                            <li><a class="dropdown-item" href="{% url 'campaigns:contributors' campaign.slug %}"><i class="bi bi-people me-2 text-muted"></i> Backers</a></li>
                                            <li><a class="dropdown-item" href="{% url 'campaigns:update_create' campaign.slug %}"><i class="bi bi-megaphone me-2 text-muted"></i> Post Update</a></li>
                                            <li><hr class="dropdown-divider"></li>
                                            <li><a class="dropdown-item" href="{% url 'campaigns:edit' campaign.slug %}"><i class="bi bi-pencil me-2 text-muted"></i> Edit</a></li>
                                            <li><a class="dropdown-item text-danger" href="{% url 'campaigns:delete' campaign.slug %}"><i class="bi bi-trash me-2 text-danger"></i> Delete</a></li>
                                        </ul>
                                    </div>
                                </td>
                            </tr>
                            {% empty %}
                            <tr>
                                <td colspan="4" class="text-center py-5 text-muted">
                                    <i class="bi bi-rocket fs-2 d-block mb-2"></i>
                                    You haven't created any campaigns yet.
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <!-- Recent Contributions -->
        <div class="col-lg-4">
            <h4 class="fw-bold mb-4">Recent Pledges</h4>
            <div class="card border-subtle shadow-sm rounded-4">
                <div class="list-group list-group-flush rounded-4">
                    {% for contrib in recent_contributions %}
                        <div class="list-group-item p-4">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span class="fw-bold">{{ contrib.contributor.username }}</span>
                                <span class="text-success fw-bold">+${{ contrib.amount }}</span>
                            </div>
                            <div class="text-muted text-small">Backed <strong>{{ contrib.campaign.title }}</strong></div>
                            <div class="text-caption text-muted mt-1">{{ contrib.created_at|timesince }} ago</div>
                        </div>
                    {% empty %}
                        <div class="p-5 text-center text-muted">
                            <i class="bi bi-piggy-bank fs-2 d-block mb-2"></i>
                            No contributions yet.
                        </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/campaigns/my_campaigns.html', creator_dashboard_html)


# 8. Contributor Dashboard (contributions/dashboard.html)
contributor_dashboard_html = """
{% extends 'base.html' %}
{% block title %}Contributor Dashboard - BackerWave{% endblock %}

{% block content %}
<div class="bg-surface py-4 border-bottom border-subtle">
    <div class="container">
        <h2 class="fw-bold mb-1">Good morning, {{ user.username }}</h2>
        <p class="text-muted mb-0">Track the impact of your support.</p>
    </div>
</div>

<div class="container py-5">
    <!-- Stat Cards -->
    <div class="row gy-4 mb-5">
        <div class="col-sm-4">
            <div class="card border-subtle shadow-sm rounded-4 h-100">
                <div class="card-body p-4">
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <h6 class="text-muted fw-bold text-uppercase mb-0">Total Contributed</h6>
                        <i class="bi bi-wallet2 text-success fs-4"></i>
                    </div>
                    <h2 class="fw-bold mb-0">${{ total_amount|default:"0" }}</h2>
                </div>
            </div>
        </div>
        <div class="col-sm-4">
            <div class="card border-subtle shadow-sm rounded-4 h-100">
                <div class="card-body p-4">
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <h6 class="text-muted fw-bold text-uppercase mb-0">Projects Backed</h6>
                        <i class="bi bi-box2-heart text-primary fs-4"></i>
                    </div>
                    <h2 class="fw-bold mb-0">{{ supported_campaigns|default:"0" }}</h2>
                </div>
            </div>
        </div>
        <div class="col-sm-4">
            <div class="card border-subtle shadow-sm rounded-4 h-100">
                <div class="card-body p-4">
                    <div class="d-flex align-items-center justify-content-between mb-3">
                        <h6 class="text-muted fw-bold text-uppercase mb-0">Total Contributions</h6>
                        <i class="bi bi-list-check text-info fs-4"></i>
                    </div>
                    <h2 class="fw-bold mb-0">{{ total_contributions|default:"0" }}</h2>
                </div>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h4 class="fw-bold mb-0">Your Pledge History</h4>
        <a href="{% url 'contributions:list' %}" class="btn btn-sm btn-outline-secondary">View All</a>
    </div>
    
    <div class="card border-subtle shadow-sm rounded-4 overflow-hidden">
        <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                    <tr>
                        <th class="ps-4 text-uppercase text-muted text-small fw-bold">Date</th>
                        <th class="text-uppercase text-muted text-small fw-bold">Project</th>
                        <th class="text-uppercase text-muted text-small fw-bold">Amount</th>
                        <th class="text-uppercase text-muted text-small fw-bold">Status</th>
                        <th class="pe-4 text-end text-uppercase text-muted text-small fw-bold">Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for contrib in recent_contributions %}
                    <tr>
                        <td class="ps-4 py-3 text-muted">{{ contrib.created_at|date:"M d, Y" }}</td>
                        <td>
                            <a href="{% url 'campaigns:detail' contrib.campaign.slug %}" class="text-decoration-none fw-bold text-dark">
                                {{ contrib.campaign.title }}
                            </a>
                        </td>
                        <td class="fw-bold text-success">${{ contrib.amount }}</td>
                        <td><span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-2 py-1">Success</span></td>
                        <td class="pe-4 text-end">
                            <a href="{% url 'contributions:detail' contrib.id %}" class="btn btn-sm btn-light fw-medium">Receipt</a>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="text-center py-5 text-muted">
                            <i class="bi bi-clock-history fs-2 d-block mb-2"></i>
                            You haven't made any pledges yet.
                            <br>
                            <a href="{% url 'campaigns:list' %}" class="btn btn-primary mt-3">Find a Project</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/contributions/dashboard.html', contributor_dashboard_html)

# 9. Contribution Flow: Review (contributions/review.html)
review_html = """
{% extends 'base.html' %}
{% block title %}Review Contribution - BackerWave{% endblock %}

{% block content %}
<div class="container py-5 max-w-700" style="max-width: 600px;">
    <div class="text-center mb-4">
        <div class="bg-primary-subtle text-primary rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 60px; height: 60px;">
            <i class="bi bi-shield-check fs-2"></i>
        </div>
        <h2 class="fw-bold">Review Your Pledge</h2>
        <p class="text-muted">You're one step away from bringing this project to life.</p>
    </div>

    <div class="card border-subtle shadow-sm rounded-4 overflow-hidden mb-4">
        <div class="bg-light p-4 border-bottom border-subtle">
            <div class="d-flex align-items-center gap-3">
                {% if contribution.campaign.campaign_image %}
                    <img src="{{ contribution.campaign.campaign_image.url }}" class="rounded-3 object-fit-cover" width="60" height="60">
                {% else %}
                    <div class="rounded-3 bg-secondary d-flex align-items-center justify-content-center text-white" style="width: 60px; height: 60px;">
                        <i class="bi bi-image"></i>
                    </div>
                {% endif %}
                <div>
                    <h5 class="fw-bold mb-1 text-truncate">{{ contribution.campaign.title }}</h5>
                    <span class="text-muted text-small">By {{ contribution.campaign.creator.username }}</span>
                </div>
            </div>
        </div>
        <div class="card-body p-4">
            <h6 class="text-muted text-uppercase fw-bold text-small mb-3">Order Summary</h6>
            <div class="d-flex justify-content-between mb-3">
                <span class="text-secondary">Pledge Amount</span>
                <span class="fw-medium">${{ contribution.amount }}</span>
            </div>
            {% if contribution.message %}
            <div class="mb-4">
                <span class="text-secondary d-block mb-1">Your Message</span>
                <div class="bg-light p-3 rounded-3 text-muted text-small font-italic">"{{ contribution.message }}"</div>
            </div>
            {% endif %}
            
            <hr class="border-subtle my-4">
            
            <div class="d-flex justify-content-between align-items-center">
                <span class="fs-5 fw-bold">Total</span>
                <span class="display-6 fw-bold text-success">${{ contribution.amount }}</span>
            </div>
        </div>
    </div>
    
    <div class="alert alert-info rounded-4 border-info-subtle bg-info-subtle text-info-emphasis d-flex align-items-center gap-3 mb-4">
        <i class="bi bi-info-circle fs-4"></i>
        <div class="text-small"><strong>Note:</strong> This is a secure mock payment simulation for development. No real charges will be made.</div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-primary btn-lg w-100 fw-bold shadow-md py-3 mb-3">Confirm Pledge</button>
        <a href="{% url 'campaigns:detail' contribution.campaign.slug %}" class="btn btn-light w-100 fw-medium">Cancel & Return</a>
    </form>
</div>
{% endblock %}
"""
write_file('templates/contributions/review.html', review_html)

# 10. Forms redesign (auth, etc)
login_html = """
{% extends 'base.html' %}
{% block title %}Log In - BackerWave{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card border-0 shadow-lg rounded-4">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <i class="bi bi-layers-fill text-primary display-4"></i>
                        <h3 class="fw-bold mt-3 mb-1">Welcome back</h3>
                        <p class="text-muted">Log in to continue to BackerWave</p>
                    </div>
                    
                    <form method="post">
                        {% csrf_token %}
                        {% for field in form %}
                            <div class="mb-3">
                                <label class="form-label fw-medium">{{ field.label }}</label>
                                {{ field }}
                                {% if field.help_text %}
                                    <div class="form-text">{{ field.help_text }}</div>
                                {% endif %}
                                {% for error in field.errors %}
                                    <div class="text-danger small mt-1">{{ error }}</div>
                                {% endfor %}
                            </div>
                        {% endfor %}
                        
                        <div class="d-flex justify-content-between align-items-center mb-4">
                            <div class="form-check">
                                <input type="checkbox" class="form-check-input" id="rememberMe">
                                <label class="form-check-label text-small text-muted" for="rememberMe">Remember me</label>
                            </div>
                            <a href="#" class="text-primary text-small text-decoration-none fw-medium">Forgot password?</a>
                        </div>
                        
                        <button type="submit" class="btn btn-primary w-100 btn-lg fw-bold shadow-sm">Log In</button>
                    </form>
                    
                    <div class="text-center mt-4 text-muted text-small">
                        Don't have an account? <a href="{% url 'accounts:register' %}" class="fw-bold text-decoration-none">Sign up</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    document.querySelectorAll('input').forEach(i => {
        if (i.type !== 'checkbox' && i.type !== 'hidden') {
            i.classList.add('form-control', 'p-3', 'bg-light');
        }
    });
</script>
{% endblock %}
"""
write_file('templates/accounts/login.html', login_html)
