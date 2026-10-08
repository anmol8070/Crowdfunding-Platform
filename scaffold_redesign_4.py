import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

# 11. Registration Form
register_html = """
{% extends 'base.html' %}
{% block title %}Sign Up - BackerWave{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-7 col-lg-6">
            <div class="card border-0 shadow-lg rounded-4">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <i class="bi bi-rocket-takeoff text-primary display-4"></i>
                        <h3 class="fw-bold mt-3 mb-1">Create an account</h3>
                        <p class="text-muted">Join the BackerWave community today</p>
                    </div>
                    
                    <form method="post">
                        {% csrf_token %}
                        <div class="row g-3">
                            {% for field in form %}
                                <div class="col-12 {% if field.name == 'first_name' or field.name == 'last_name' %}col-sm-6{% endif %}">
                                    <label class="form-label fw-medium">{{ field.label }}</label>
                                    {{ field }}
                                    {% if field.help_text %}
                                        <div class="form-text small text-muted mt-1">{{ field.help_text }}</div>
                                    {% endif %}
                                    {% for error in field.errors %}
                                        <div class="text-danger small mt-1"><i class="bi bi-exclamation-circle me-1"></i>{{ error }}</div>
                                    {% endfor %}
                                </div>
                            {% endfor %}
                        </div>
                        
                        <div class="mt-4 mb-4 text-muted text-small">
                            By signing up, you agree to our <a href="#" class="text-decoration-none fw-medium">Terms of Service</a> and <a href="#" class="text-decoration-none fw-medium">Privacy Policy</a>.
                        </div>
                        
                        <button type="submit" class="btn btn-primary w-100 btn-lg fw-bold shadow-sm">Create Account</button>
                    </form>
                    
                    <div class="text-center mt-4 text-muted text-small">
                        Already have an account? <a href="{% url 'accounts:login' %}" class="fw-bold text-decoration-none">Log in</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    document.querySelectorAll('input, select').forEach(i => {
        if (i.type !== 'checkbox' && i.type !== 'hidden') {
            i.classList.add('form-control', 'p-3', 'bg-light');
        }
    });
</script>
{% endblock %}
"""
write_file('templates/accounts/register.html', register_html)

# 12. Campaign Form (Create/Edit)
campaign_form_html = """
{% extends 'base.html' %}
{% block title %}{{ title }} - BackerWave{% endblock %}

{% block content %}
<div class="bg-surface border-bottom border-subtle py-4">
    <div class="container max-w-700" style="max-width: 800px;">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb mb-2">
                <li class="breadcrumb-item"><a href="{% url 'campaigns:my_campaigns' %}" class="text-muted text-decoration-none">Dashboard</a></li>
                <li class="breadcrumb-item active text-dark fw-medium">{{ title }}</li>
            </ol>
        </nav>
        <h2 class="fw-bold mb-0">{{ title }}</h2>
    </div>
</div>

<div class="container py-5 max-w-700" style="max-width: 800px;">
    <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
        <div class="card-body p-4 p-lg-5">
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                
                <h5 class="fw-bold mb-4 text-primary"><i class="bi bi-info-circle me-2"></i>1. Basic Information</h5>
                <div class="row g-4 mb-5">
                    {% for field in form %}
                        {% if field.name in 'title,category,short_description' %}
                            <div class="col-12 {% if field.name == 'category' %}col-md-6{% endif %}">
                                <label class="form-label fw-bold">{{ field.label }}</label>
                                {{ field }}
                                {% if field.help_text %}<div class="form-text">{{ field.help_text }}</div>{% endif %}
                                {% for error in field.errors %}<div class="text-danger small mt-1">{{ error }}</div>{% endfor %}
                            </div>
                        {% endif %}
                    {% endfor %}
                </div>
                
                <hr class="border-subtle my-5">
                
                <h5 class="fw-bold mb-4 text-primary"><i class="bi bi-card-text me-2"></i>2. Campaign Story</h5>
                <div class="row g-4 mb-5">
                    {% for field in form %}
                        {% if field.name == 'description' %}
                            <div class="col-12">
                                <label class="form-label fw-bold">{{ field.label }}</label>
                                {{ field }}
                                {% if field.help_text %}<div class="form-text">{{ field.help_text }}</div>{% endif %}
                                {% for error in field.errors %}<div class="text-danger small mt-1">{{ error }}</div>{% endfor %}
                            </div>
                        {% endif %}
                    {% endfor %}
                </div>
                
                <hr class="border-subtle my-5">
                
                <h5 class="fw-bold mb-4 text-primary"><i class="bi bi-piggy-bank me-2"></i>3. Funding & Duration</h5>
                <div class="row g-4 mb-5">
                    {% for field in form %}
                        {% if field.name in 'goal_amount,start_date,end_date' %}
                            <div class="col-12 col-md-4">
                                <label class="form-label fw-bold">{{ field.label }}</label>
                                {{ field }}
                                {% if field.help_text %}<div class="form-text">{{ field.help_text }}</div>{% endif %}
                                {% for error in field.errors %}<div class="text-danger small mt-1">{{ error }}</div>{% endfor %}
                            </div>
                        {% endif %}
                    {% endfor %}
                </div>
                
                <hr class="border-subtle my-5">
                
                <h5 class="fw-bold mb-4 text-primary"><i class="bi bi-image me-2"></i>4. Media & Status</h5>
                <div class="row g-4 mb-5">
                    {% for field in form %}
                        {% if field.name in 'campaign_image,status' %}
                            <div class="col-12 col-md-6">
                                <label class="form-label fw-bold">{{ field.label }}</label>
                                {{ field }}
                                {% if field.help_text %}<div class="form-text">{{ field.help_text }}</div>{% endif %}
                                {% for error in field.errors %}<div class="text-danger small mt-1">{{ error }}</div>{% endfor %}
                            </div>
                        {% endif %}
                    {% endfor %}
                </div>
                
                <div class="d-flex justify-content-end gap-3 pt-3 border-top border-subtle">
                    <a href="{% url 'campaigns:my_campaigns' %}" class="btn btn-light px-4 fw-medium">Cancel</a>
                    <button type="submit" class="btn btn-primary px-5 fw-bold shadow-sm">Save Campaign</button>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
    document.querySelectorAll('input, select, textarea').forEach(i => {
        if (i.type !== 'checkbox' && i.type !== 'hidden' && i.type !== 'file') {
            i.classList.add('form-control', 'bg-light');
        }
        if (i.type === 'file') {
            i.classList.add('form-control');
        }
        if (i.type === 'select-one') {
            i.classList.add('form-select', 'bg-light');
        }
    });
</script>
{% endblock %}
"""
write_file('templates/campaigns/form.html', campaign_form_html)

# 13. Contribution Success (contributions/success.html)
success_html = """
{% extends 'base.html' %}
{% block title %}Contribution Successful{% endblock %}
{% block content %}
<div class="container py-5 text-center max-w-700" style="max-width: 600px;">
    <div class="py-5">
        <div class="bg-success-subtle text-success rounded-circle d-inline-flex align-items-center justify-content-center mb-4 mx-auto" style="width: 100px; height: 100px;">
            <i class="bi bi-check2 fs-1"></i>
        </div>
        
        <h1 class="fw-bold mb-3">You're awesome!</h1>
        <p class="lead text-muted mb-5">Your pledge of <strong class="text-dark">${{ contribution.amount }}</strong> to <strong>{{ contribution.campaign.title }}</strong> was successful. Thank you for helping bring this idea to life.</p>
        
        <div class="card border-subtle shadow-sm rounded-4 mb-5 text-start">
            <div class="card-body p-4">
                <h6 class="text-muted fw-bold text-small text-uppercase border-bottom border-subtle pb-2 mb-3">Transaction Details</h6>
                <div class="d-flex justify-content-between mb-2">
                    <span class="text-secondary">Reference</span>
                    <span class="fw-medium font-monospace">{{ contribution.transaction_reference }}</span>
                </div>
                <div class="d-flex justify-content-between mb-2">
                    <span class="text-secondary">Date</span>
                    <span class="fw-medium">{{ contribution.updated_at|date:"M d, Y H:i" }}</span>
                </div>
                <div class="d-flex justify-content-between">
                    <span class="text-secondary">Status</span>
                    <span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill">Success</span>
                </div>
            </div>
        </div>
        
        <div class="d-flex flex-column flex-sm-row justify-content-center gap-3">
            <a href="{% url 'campaigns:detail' contribution.campaign.slug %}" class="btn btn-primary btn-lg px-4 shadow-sm fw-bold">Return to Project</a>
            <a href="{% url 'contributions:dashboard' %}" class="btn btn-outline-secondary btn-lg px-4 fw-medium">View My Pledges</a>
            <a href="{% url 'contributions:receipt' contribution.id %}" target="_blank" class="btn btn-light btn-lg px-4 fw-medium"><i class="bi bi-printer me-2"></i>Receipt</a>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/contributions/success.html', success_html)

# 14. Support Form (contributions/support.html)
support_html = """
{% extends 'base.html' %}
{% block title %}Support {{ campaign.title }}{% endblock %}

{% block content %}
<div class="container py-5 max-w-700" style="max-width: 600px;">
    <div class="text-center mb-5">
        <h2 class="fw-bold">Support this project</h2>
        <h4 class="text-primary mb-2">{{ campaign.title }}</h4>
        <p class="text-muted">By {{ campaign.creator.username }}</p>
    </div>
    
    <div class="card border-0 shadow-sm rounded-4 overflow-hidden mb-4">
        <div class="card-body p-4 p-md-5">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-4">
                    <label class="form-label fw-bold">Pledge Amount ($)</label>
                    <div class="input-group input-group-lg">
                        <span class="input-group-text bg-light border-end-0 text-muted">$</span>
                        {{ form.amount }}
                    </div>
                    {% if form.amount.errors %}<div class="text-danger small mt-1">{{ form.amount.errors }}</div>{% endif %}
                    <div class="form-text mt-2">Enter the amount you wish to contribute to this campaign.</div>
                </div>
                
                <div class="mb-4">
                    <label class="form-label fw-bold">Leave a Message (Optional)</label>
                    {{ form.message }}
                    <div class="form-text mt-2">Share some words of encouragement with the creator!</div>
                </div>
                
                <hr class="border-subtle my-4">
                
                <button type="submit" class="btn btn-success btn-lg w-100 fw-bold shadow-md py-3">Continue to Review <i class="bi bi-arrow-right ms-2"></i></button>
            </form>
        </div>
    </div>
    
    <p class="text-center text-muted small"><i class="bi bi-shield-lock me-1"></i> Payments are processed securely via mock transaction.</p>
</div>

<script>
    document.querySelector('input[name="amount"]').classList.add('form-control', 'bg-light', 'border-start-0', 'fw-bold', 'fs-4');
    document.querySelector('textarea[name="message"]').classList.add('form-control', 'bg-light');
</script>
{% endblock %}
"""
write_file('templates/contributions/support.html', support_html)
