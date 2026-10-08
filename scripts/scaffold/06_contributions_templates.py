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

# 1. Update base.html to point to dashboard based on role
replace_in_file('templates/base.html',
    "{% if user.profile.user_type == 'CREATOR' %}\n                            <li class=\"nav-item\"><a class=\"nav-link\" href=\"{% url 'campaigns:my_campaigns' %}\">Dashboard</a></li>\n                        {% endif %}",
    "{% if user.profile.user_type == 'CREATOR' %}\n                            <li class=\"nav-item\"><a class=\"nav-link\" href=\"{% url 'campaigns:my_campaigns' %}\">Dashboard</a></li>\n                        {% else %}\n                            <li class=\"nav-item\"><a class=\"nav-link\" href=\"{% url 'contributions:dashboard' %}\">Dashboard</a></li>\n                        {% endif %}")

# 2. Add updates loop in campaigns/detail.html and connect Support button
replace_in_file('templates/campaigns/detail.html',
    '<button class="btn btn-success btn-lg w-100 mb-3" {% if campaign.status != \'ACTIVE\' %}disabled{% endif %}>Support This Campaign</button>',
    '{% if campaign.status == \'ACTIVE\' %}\n                    <a href="{% url \'contributions:support\' campaign.slug %}" class="btn btn-success btn-lg w-100 mb-3">Support This Campaign</a>\n                {% else %}\n                    <button class="btn btn-secondary btn-lg w-100 mb-3" disabled>Campaign Closed</button>\n                {% endif %}')

replace_in_file('templates/campaigns/detail.html',
    '<h4>About this campaign</h4>',
    '''
    <ul class="nav nav-tabs mb-4" id="campaignTabs" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link active" id="about-tab" data-bs-toggle="tab" data-bs-target="#about" type="button" role="tab">About</button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="updates-tab" data-bs-toggle="tab" data-bs-target="#updates" type="button" role="tab">Updates ({{ campaign.updates.count }})</button>
        </li>
    </ul>
    <div class="tab-content" id="campaignTabsContent">
        <div class="tab-pane fade show active" id="about" role="tabpanel">
            <h4>About this campaign</h4>
    ''')

replace_in_file('templates/campaigns/detail.html',
    '</div>\n        </div>\n    </div>',
    '''</div>\n        </div>
        <div class="tab-pane fade" id="updates" role="tabpanel">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4>Campaign Updates</h4>
                {% if request.user == campaign.creator %}
                <a href="{% url 'campaigns:update_create' campaign.slug %}" class="btn btn-sm btn-primary">Post Update</a>
                {% endif %}
            </div>
            {% for update in campaign.updates.all|dictsortreversed:"created_at" %}
                <div class="card mb-3 shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">{{ update.title }}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">{{ update.created_at|date:"M d, Y" }}</h6>
                        <p class="card-text">{{ update.content|linebreaks }}</p>
                        {% if update.image %}
                        <img src="{{ update.image.url }}" class="img-fluid rounded mt-2" style="max-height:300px;">
                        {% endif %}
                    </div>
                </div>
            {% empty %}
                <p class="text-muted">No updates posted yet.</p>
            {% endfor %}
        </div>
    </div>
    </div>''')

# 3. Creator Dashboard updates (campaigns/my_campaigns.html)
replace_in_file('templates/campaigns/my_campaigns.html',
    '<th>Actions</th>',
    '<th>Contributors</th><th>Actions</th>')

replace_in_file('templates/campaigns/my_campaigns.html',
    '<td>\n                    <div class="btn-group btn-group-sm">',
    '<td><a href="{% url \'campaigns:contributors\' campaign.slug %}" class="btn btn-sm btn-outline-info">{{ campaign.contributions.count }} Backers</a></td>\n                <td>\n                    <div class="btn-group btn-group-sm">')

# 4. Campaign Update Form
campaigns_update_form = """
{% extends 'base.html' %}
{% block title %}Post Update - {{ campaign.title }}{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <h2 class="mb-4">Post Update for {{ campaign.title }}</h2>
        <div class="card shadow-sm">
            <div class="card-body">
                <form method="post" enctype="multipart/form-data">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary">Publish Update</button>
                    <a href="{% url 'campaigns:detail' campaign.slug %}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/campaigns/update_form.html', campaigns_update_form)

# 5. Campaign Contributors View
campaigns_contributors = """
{% extends 'base.html' %}
{% block title %}Contributors - {{ campaign.title }}{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Contributors: {{ campaign.title }}</h2>
    <a href="{% url 'campaigns:my_campaigns' %}" class="btn btn-outline-secondary">Back to Dashboard</a>
</div>
<div class="card shadow-sm">
    <div class="card-body">
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Contributor</th>
                    <th>Amount</th>
                    <th>Transaction Ref</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody>
                {% for contrib in contributions %}
                <tr>
                    <td>{{ contrib.created_at|date:"M d, Y" }}</td>
                    <td>{{ contrib.contributor.profile.full_name|default:contrib.contributor.username }}</td>
                    <td>${{ contrib.amount }}</td>
                    <td>{{ contrib.transaction_reference }}</td>
                    <td><small class="text-muted">{{ contrib.message|default:"-" }}</small></td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="5" class="text-center">No contributions yet.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
"""
write_file('templates/campaigns/contributors.html', campaigns_contributors)

# 6. Contributions templates
contributions_support = """
{% extends 'base.html' %}
{% block title %}Support {{ campaign.title }}{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="text-center mb-4">
            <h2>Support Campaign</h2>
            <h4 class="text-primary">{{ campaign.title }}</h4>
            <p>By {{ campaign.creator.username }}</p>
        </div>
        <div class="card shadow-sm">
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-success w-100 btn-lg mt-3">Continue to Review</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/contributions/support.html', contributions_support)

contributions_review = """
{% extends 'base.html' %}
{% block title %}Review Contribution{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <h2 class="text-center mb-4">Review Contribution</h2>
        <div class="card shadow-sm border-primary">
            <div class="card-body">
                <h5 class="card-title border-bottom pb-2 mb-3">Order Summary</h5>
                <div class="d-flex justify-content-between mb-2">
                    <span>Campaign:</span>
                    <strong>{{ contribution.campaign.title }}</strong>
                </div>
                <div class="d-flex justify-content-between mb-2">
                    <span>Creator:</span>
                    <span>{{ contribution.campaign.creator.username }}</span>
                </div>
                <div class="d-flex justify-content-between mb-2">
                    <span>Message:</span>
                    <span>{{ contribution.message|default:"None" }}</span>
                </div>
                <hr>
                <div class="d-flex justify-content-between mb-3 fs-5">
                    <span>Total Amount:</span>
                    <strong class="text-success">${{ contribution.amount }}</strong>
                </div>
                
                <div class="alert alert-warning text-center small mb-4">
                    <strong>Note:</strong> This is a mock payment for development purposes. No real transaction will occur.
                </div>
                
                <form method="post">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-primary btn-lg w-100">Confirm & Pay Mock</button>
                    <a href="{% url 'campaigns:detail' contribution.campaign.slug %}" class="btn btn-link w-100 mt-2 text-muted">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/contributions/review.html', contributions_review)

contributions_success = """
{% extends 'base.html' %}
{% block title %}Contribution Successful{% endblock %}
{% block content %}
<div class="row justify-content-center text-center mt-5">
    <div class="col-md-8">
        <div class="display-1 text-success mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" fill="currentColor" class="bi bi-check-circle-fill" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
            </svg>
        </div>
        <h2 class="mb-3">Thank you for your support!</h2>
        <p class="lead mb-4">Your contribution of <strong>${{ contribution.amount }}</strong> to <strong>{{ contribution.campaign.title }}</strong> was successful.</p>
        
        <div class="card shadow-sm mx-auto mb-4" style="max-width: 500px;">
            <div class="card-body text-start">
                <p class="mb-1"><strong>Transaction Ref:</strong> {{ contribution.transaction_reference }}</p>
                <p class="mb-1"><strong>Date:</strong> {{ contribution.updated_at|date:"M d, Y H:i" }}</p>
                <p class="mb-0"><strong>Status:</strong> <span class="badge bg-success">Success</span></p>
            </div>
        </div>
        
        <div class="d-flex justify-content-center gap-3">
            <a href="{% url 'contributions:receipt' contribution.id %}" target="_blank" class="btn btn-outline-secondary">View Receipt</a>
            <a href="{% url 'campaigns:detail' contribution.campaign.slug %}" class="btn btn-primary">Return to Campaign</a>
            <a href="{% url 'contributions:dashboard' %}" class="btn btn-outline-primary">My Contributions</a>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/contributions/success.html', contributions_success)

contributions_receipt = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Receipt - {{ contribution.transaction_reference }}</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; color: #333; }
        .header { border-bottom: 2px solid #0d6efd; padding-bottom: 20px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: end; }
        .header h1 { margin: 0; color: #0d6efd; }
        .details-table { width: 100%; border-collapse: collapse; margin-bottom: 40px; }
        .details-table th, .details-table td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        .details-table th { width: 30%; color: #666; }
        .total { font-size: 1.5em; font-weight: bold; text-align: right; margin-top: 20px; color: #198754; }
        .footer { margin-top: 50px; text-align: center; color: #777; font-size: 0.9em; }
        @media print { .no-print { display: none; } }
    </style>
</head>
<body>
    <div class="no-print" style="margin-bottom: 20px; text-align: right;">
        <button onclick="window.print()" style="padding: 10px 20px; background: #0d6efd; color: white; border: none; cursor: pointer;">Print Receipt</button>
    </div>
    
    <div class="header">
        <div>
            <h1>BackerWave</h1>
            <p style="margin:5px 0 0 0;">Official Contribution Receipt</p>
        </div>
        <div style="text-align: right;">
            <strong>Date:</strong> {{ contribution.updated_at|date:"M d, Y" }}<br>
            <strong>Time:</strong> {{ contribution.updated_at|date:"H:i T" }}
        </div>
    </div>
    
    <table class="details-table">
        <tr>
            <th>Transaction Reference</th>
            <td>{{ contribution.transaction_reference }}</td>
        </tr>
        <tr>
            <th>Status</th>
            <td><strong>{{ contribution.get_status_display }}</strong></td>
        </tr>
        <tr>
            <th>Contributor</th>
            <td>{{ contribution.contributor.profile.full_name|default:contribution.contributor.username }} ({{ contribution.contributor.email }})</td>
        </tr>
        <tr>
            <th>Campaign Supported</th>
            <td>{{ contribution.campaign.title }}</td>
        </tr>
        <tr>
            <th>Campaign Creator</th>
            <td>{{ contribution.campaign.creator.username }}</td>
        </tr>
        {% if contribution.message %}
        <tr>
            <th>Message Included</th>
            <td><em>"{{ contribution.message }}"</em></td>
        </tr>
        {% endif %}
    </table>
    
    <div class="total">
        Amount Paid: ${{ contribution.amount }}
    </div>
    
    <div class="footer">
        <p>Thank you for supporting innovative projects on BackerWave.</p>
        <p>This is a computer-generated receipt for a mock transaction.</p>
    </div>
</body>
</html>
"""
write_file('templates/contributions/receipt.html', contributions_receipt)

contributions_dashboard = """
{% extends 'base.html' %}
{% block title %}Contributor Dashboard{% endblock %}
{% block content %}
<h2 class="mb-4">Contributor Dashboard</h2>

<div class="row mb-5">
    <div class="col-md-4">
        <div class="card bg-primary text-white text-center shadow-sm h-100">
            <div class="card-body">
                <h3>{{ total_contributions }}</h3>
                <p class="mb-0">Total Contributions</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card bg-success text-white text-center shadow-sm h-100">
            <div class="card-body">
                <h3>${{ total_amount }}</h3>
                <p class="mb-0">Total Amount Contributed</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card bg-info text-white text-center shadow-sm h-100">
            <div class="card-body">
                <h3>{{ supported_campaigns }}</h3>
                <p class="mb-0">Supported Campaigns</p>
            </div>
        </div>
    </div>
</div>

<h4 class="mb-3">Recent Contributions</h4>
<div class="table-responsive">
    <table class="table table-hover align-middle">
        <thead class="table-light">
            <tr>
                <th>Date</th>
                <th>Campaign</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for contrib in recent_contributions %}
            <tr>
                <td>{{ contrib.created_at|date:"M d, Y" }}</td>
                <td>
                    <a href="{% url 'campaigns:detail' contrib.campaign.slug %}" class="text-decoration-none fw-bold">
                        {{ contrib.campaign.title }}
                    </a>
                </td>
                <td>${{ contrib.amount }}</td>
                <td><span class="badge bg-success">Success</span></td>
                <td>
                    <a href="{% url 'contributions:detail' contrib.id %}" class="btn btn-sm btn-outline-primary">Details</a>
                    <a href="{% url 'contributions:receipt' contrib.id %}" target="_blank" class="btn btn-sm btn-outline-secondary">Receipt</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="5" class="text-center py-4">You haven't made any contributions yet.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% if recent_contributions %}
    <div class="text-end">
        <a href="{% url 'contributions:list' %}" class="btn btn-link">View All History</a>
    </div>
    {% endif %}
</div>
{% endblock %}
"""
write_file('templates/contributions/dashboard.html', contributions_dashboard)

contributions_list = """
{% extends 'base.html' %}
{% block title %}Contribution History{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Contribution History</h2>
    <a href="{% url 'contributions:dashboard' %}" class="btn btn-outline-secondary">Back to Dashboard</a>
</div>
<div class="card shadow-sm">
    <div class="card-body p-0">
        <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
                <tr>
                    <th class="ps-3">Date</th>
                    <th>Campaign</th>
                    <th>Ref ID</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th class="pe-3 text-end">Action</th>
                </tr>
            </thead>
            <tbody>
                {% for contrib in contributions %}
                <tr>
                    <td class="ps-3">{{ contrib.created_at|date:"M d, Y" }}</td>
                    <td><a href="{% url 'campaigns:detail' contrib.campaign.slug %}" class="text-decoration-none fw-bold">{{ contrib.campaign.title }}</a></td>
                    <td><small class="text-muted">{{ contrib.transaction_reference }}</small></td>
                    <td>${{ contrib.amount }}</td>
                    <td><span class="badge bg-{{ contrib.status|lower|default:'secondary' }}">{{ contrib.get_status_display }}</span></td>
                    <td class="pe-3 text-end">
                        <a href="{% url 'contributions:detail' contrib.id %}" class="btn btn-sm btn-outline-primary">View</a>
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="6" class="text-center py-4">No contributions found.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
"""
write_file('templates/contributions/list.html', contributions_list)

contributions_detail = """
{% extends 'base.html' %}
{% block title %}Contribution Details{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>Contribution Details</h2>
            <a href="{% url 'contributions:list' %}" class="btn btn-outline-secondary">Back to History</a>
        </div>
        
        <div class="card shadow-sm">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
                <span class="fw-bold text-muted">ID: {{ contribution.transaction_reference }}</span>
                <span class="badge bg-{{ contribution.status|lower|default:'secondary' }}">{{ contribution.get_status_display }}</span>
            </div>
            <div class="card-body">
                <div class="row mb-4">
                    <div class="col-sm-4 text-muted">Date</div>
                    <div class="col-sm-8">{{ contribution.created_at|date:"F d, Y H:i T" }}</div>
                </div>
                <div class="row mb-4">
                    <div class="col-sm-4 text-muted">Campaign</div>
                    <div class="col-sm-8 fw-bold">
                        <a href="{% url 'campaigns:detail' contribution.campaign.slug %}">{{ contribution.campaign.title }}</a>
                    </div>
                </div>
                <div class="row mb-4">
                    <div class="col-sm-4 text-muted">Amount</div>
                    <div class="col-sm-8 fs-5 text-success fw-bold">${{ contribution.amount }}</div>
                </div>
                <div class="row mb-4">
                    <div class="col-sm-4 text-muted">Message</div>
                    <div class="col-sm-8"><em>{{ contribution.message|default:"No message provided." }}</em></div>
                </div>
                
                {% if contribution.status == 'SUCCESS' %}
                <div class="mt-4 pt-3 border-top text-center">
                    <a href="{% url 'contributions:receipt' contribution.id %}" target="_blank" class="btn btn-outline-primary"><i class="bi bi-receipt"></i> View Receipt</a>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/contributions/detail.html', contributions_detail)
