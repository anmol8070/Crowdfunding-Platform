import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

# 4. Home Page (core/home.html)
home_html = """
{% extends 'base.html' %}
{% block title %}BackerWave - Fund ideas that matter{% endblock %}

{% block content %}
<!-- Hero Section -->
<section class="bg-surface border-bottom border-subtle">
    <div class="container py-5 py-lg-6">
        <div class="row align-items-center gy-5">
            <div class="col-lg-6 pe-lg-5 text-center text-lg-start">
                <span class="text-primary fw-bold text-small text-uppercase tracking-wider mb-3 d-block">Fund ideas that matter</span>
                <h1 class="display text-primary mb-4 fw-bold">Great ideas deserve a chance to become real.</h1>
                <p class="lead text-secondary mb-5">BackerWave connects passionate creators with backers who believe in the future. Discover, support, and bring visionary projects to life.</p>
                <div class="d-flex flex-column flex-sm-row gap-3 justify-content-center justify-content-lg-start">
                    <a href="{% url 'campaigns:list' %}" class="btn btn-primary btn-lg px-5 shadow-md">Explore Campaigns</a>
                    {% if user.profile.user_type == 'CREATOR' %}
                        <a href="{% url 'campaigns:create' %}" class="btn btn-outline-primary btn-lg px-5">Start a Campaign</a>
                    {% endif %}
                </div>
            </div>
            <div class="col-lg-6">
                {% if featured_campaigns %}
                    {% with campaign=featured_campaigns.first %}
                        <div class="position-relative">
                            <div class="position-absolute top-0 start-0 w-100 h-100 bg-primary rounded-4 opacity-10 ms-4 mt-4 d-none d-lg-block"></div>
                            <div class="card border-0 shadow-lg rounded-4 overflow-hidden position-relative bg-white">
                                {% if campaign.campaign_image %}
                                    <img src="{{ campaign.campaign_image.url }}" class="w-100 object-fit-cover" style="height: 350px;">
                                {% else %}
                                    <div class="w-100 bg-light d-flex align-items-center justify-content-center text-muted" style="height: 350px;">
                                        <i class="bi bi-image fs-1"></i>
                                    </div>
                                {% endif %}
                                <div class="card-body p-4 p-lg-5">
                                    <span class="badge bg-primary-subtle text-primary mb-3 px-3 py-2 rounded-pill fw-medium border border-primary-subtle">{{ campaign.category.name }}</span>
                                    <h3 class="fw-bold mb-2">{{ campaign.title }}</h3>
                                    <p class="text-muted mb-4">{{ campaign.short_description|truncatechars:100 }}</p>
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                            <div class="text-success fw-bold fs-5">${{ campaign.current_amount }}</div>
                                            <div class="text-caption text-muted">funded of ${{ campaign.goal_amount }}</div>
                                        </div>
                                        <a href="{% url 'campaigns:detail' campaign.slug %}" class="btn btn-outline-primary px-4 rounded-pill">View Project</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {% endwith %}
                {% endif %}
            </div>
        </div>
    </div>
</section>

<!-- Stats Section -->
<section class="py-5 bg-white border-bottom border-subtle">
    <div class="container">
        <div class="row text-center gy-4">
            <div class="col-6 col-md-3">
                <h2 class="fw-bold text-primary mb-1">{{ stats.total_campaigns }}</h2>
                <div class="text-muted text-small fw-medium text-uppercase">Total Projects</div>
            </div>
            <div class="col-6 col-md-3">
                <h2 class="fw-bold text-success mb-1">${{ stats.total_raised }}</h2>
                <div class="text-muted text-small fw-medium text-uppercase">Funds Raised</div>
            </div>
            <div class="col-6 col-md-3">
                <h2 class="fw-bold text-info mb-1">{{ stats.total_contributors }}</h2>
                <div class="text-muted text-small fw-medium text-uppercase">Backers</div>
            </div>
            <div class="col-6 col-md-3">
                <h2 class="fw-bold text-warning mb-1">{{ stats.completed_campaigns }}</h2>
                <div class="text-muted text-small fw-medium text-uppercase">Successfully Funded</div>
            </div>
        </div>
    </div>
</section>

<!-- Trending Section -->
<section class="section-padding bg-light">
    <div class="container">
        <div class="d-flex justify-content-between align-items-end mb-5">
            <div>
                <h2 class="fw-bold mb-2">Projects worth backing</h2>
                <p class="text-muted mb-0">Discover campaigns making an impact right now.</p>
            </div>
            <a href="{% url 'campaigns:list' %}" class="btn btn-outline-primary d-none d-md-inline-block">View All</a>
        </div>
        
        <div class="row gy-4">
            {% for campaign in trending_campaigns %}
                <div class="col-md-6 col-lg-4">
                    {% include 'components/campaign_card.html' %}
                </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- How it Works -->
<section class="section-padding bg-white border-top border-subtle">
    <div class="container text-center">
        <h2 class="fw-bold mb-5">How BackerWave Works</h2>
        <div class="row gy-5">
            <div class="col-md-4">
                <div class="bg-primary-subtle text-primary rounded-circle d-inline-flex align-items-center justify-content-center mb-4" style="width: 80px; height: 80px;">
                    <i class="bi bi-search fs-1"></i>
                </div>
                <h4 class="fw-bold mb-3">01. Discover</h4>
                <p class="text-muted px-lg-4">Find innovative projects across tech, art, and community causes that inspire you.</p>
            </div>
            <div class="col-md-4">
                <div class="bg-success-subtle text-success rounded-circle d-inline-flex align-items-center justify-content-center mb-4" style="width: 80px; height: 80px;">
                    <i class="bi bi-credit-card fs-1"></i>
                </div>
                <h4 class="fw-bold mb-3">02. Support</h4>
                <p class="text-muted px-lg-4">Securely pledge funds to help creators reach their goals and bring ideas to life.</p>
            </div>
            <div class="col-md-4">
                <div class="bg-info-subtle text-info rounded-circle d-inline-flex align-items-center justify-content-center mb-4" style="width: 80px; height: 80px;">
                    <i class="bi bi-rocket-takeoff fs-1"></i>
                </div>
                <h4 class="fw-bold mb-3">03. Impact</h4>
                <p class="text-muted px-lg-4">Watch projects grow, receive exclusive updates, and be part of the journey.</p>
            </div>
        </div>
    </div>
</section>

<!-- CTA Section -->
<section class="py-5 bg-primary text-white text-center">
    <div class="container py-4">
        <h2 class="fw-bold mb-3">Have an idea worth backing?</h2>
        <p class="lead mb-4 text-white-50">Join thousands of creators who funded their dreams on BackerWave.</p>
        <a href="{% url 'campaigns:create' %}" class="btn btn-light btn-lg px-5 text-primary fw-bold shadow-md">Start a Campaign</a>
    </div>
</section>
{% endblock %}
"""
write_file('templates/core/home.html', home_html)


# 5. Explore Campaigns Page (campaigns/list.html)
explore_html = """
{% extends 'base.html' %}
{% block title %}Explore Campaigns{% endblock %}

{% block content %}
<div class="bg-surface border-bottom border-subtle py-5">
    <div class="container">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="{% url 'core:home' %}" class="text-muted text-decoration-none">Home</a></li>
                <li class="breadcrumb-item active text-dark fw-medium">Explore</li>
            </ol>
        </nav>
        <h1 class="fw-bold mb-3">Explore Campaigns</h1>
        <p class="text-muted lead mb-0">Discover projects backed by people like you.</p>
    </div>
</div>

<div class="container py-5">
    <div class="row">
        <!-- Sidebar Filters -->
        <div class="col-lg-3 mb-5 mb-lg-0">
            <div class="card border-0 shadow-sm rounded-4 sticky-top" style="top: 100px;">
                <div class="card-body p-4">
                    <h5 class="fw-bold mb-4 d-flex align-items-center gap-2"><i class="bi bi-sliders text-primary"></i> Filters</h5>
                    
                    <form method="get" action="{% url 'campaigns:list' %}">
                        {% if request.GET.q %}
                            <input type="hidden" name="q" value="{{ request.GET.q }}">
                        {% endif %}
                        
                        <!-- Sort -->
                        <div class="mb-4">
                            <label class="form-label text-small fw-bold text-uppercase text-muted">Sort By</label>
                            <select name="sort" class="form-select form-select-sm border-subtle shadow-none">
                                <option value="-created_at" {% if request.GET.sort == '-created_at' %}selected{% endif %}>Newest</option>
                                <option value="created_at" {% if request.GET.sort == 'created_at' %}selected{% endif %}>Oldest</option>
                                <option value="-current_amount" {% if request.GET.sort == '-current_amount' %}selected{% endif %}>Most Funded</option>
                                <option value="end_date" {% if request.GET.sort == 'end_date' %}selected{% endif %}>Ending Soon</option>
                                <option value="-goal_amount" {% if request.GET.sort == '-goal_amount' %}selected{% endif %}>Highest Goal</option>
                            </select>
                        </div>
                        
                        <!-- Category -->
                        <div class="mb-4">
                            <label class="form-label text-small fw-bold text-uppercase text-muted">Category</label>
                            <select name="category" class="form-select form-select-sm border-subtle shadow-none">
                                <option value="">All Categories</option>
                                {% for cat in categories %}
                                    <option value="{{ cat.slug }}" {% if request.GET.category == cat.slug %}selected{% endif %}>{{ cat.name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        
                        <!-- Goal Range -->
                        <div class="mb-4">
                            <label class="form-label text-small fw-bold text-uppercase text-muted">Funding Goal ($)</label>
                            <div class="row g-2">
                                <div class="col-6">
                                    <input type="number" name="min_goal" class="form-control form-control-sm border-subtle" placeholder="Min" value="{{ request.GET.min_goal }}">
                                </div>
                                <div class="col-6">
                                    <input type="number" name="max_goal" class="form-control form-control-sm border-subtle" placeholder="Max" value="{{ request.GET.max_goal }}">
                                </div>
                            </div>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-sm fw-bold">Apply Filters</button>
                            <a href="{% url 'campaigns:list' %}" class="btn btn-light btn-sm text-muted">Clear Filters</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="col-lg-9">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <span class="text-muted fw-medium">{{ page_obj.paginator.count }} campaigns found</span>
            </div>
            
            {% if page_obj %}
                <div class="row gy-4">
                    {% for campaign in page_obj %}
                        <div class="col-md-6 col-xl-4">
                            {% include 'components/campaign_card.html' %}
                        </div>
                    {% endfor %}
                </div>
                
                <!-- Pagination -->
                {% if page_obj.has_other_pages %}
                    <nav class="mt-5">
                        <ul class="pagination justify-content-center">
                            {% if page_obj.has_previous %}
                                <li class="page-item"><a class="page-link shadow-sm border-subtle text-dark" href="?page={{ page_obj.previous_page_number }}{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}"><i class="bi bi-chevron-left"></i></a></li>
                            {% else %}
                                <li class="page-item disabled"><span class="page-link shadow-sm border-subtle text-muted"><i class="bi bi-chevron-left"></i></span></li>
                            {% endif %}
                            
                            {% for i in page_obj.paginator.page_range %}
                                {% if page_obj.number == i %}
                                    <li class="page-item active"><span class="page-link bg-primary border-primary shadow-sm">{{ i }}</span></li>
                                {% else %}
                                    <li class="page-item"><a class="page-link shadow-sm border-subtle text-dark" href="?page={{ i }}{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}">{{ i }}</a></li>
                                {% endif %}
                            {% endfor %}
                            
                            {% if page_obj.has_next %}
                                <li class="page-item"><a class="page-link shadow-sm border-subtle text-dark" href="?page={{ page_obj.next_page_number }}{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}"><i class="bi bi-chevron-right"></i></a></li>
                            {% else %}
                                <li class="page-item disabled"><span class="page-link shadow-sm border-subtle text-muted"><i class="bi bi-chevron-right"></i></span></li>
                            {% endif %}
                        </ul>
                    </nav>
                {% endif %}
            {% else %}
                <div class="card border-0 shadow-sm rounded-4 text-center py-5">
                    <div class="card-body py-5">
                        <i class="bi bi-search fs-1 text-muted mb-3 d-block"></i>
                        <h4 class="fw-bold mb-2">No campaigns found</h4>
                        <p class="text-muted mb-4">We couldn't find any campaigns matching your current filters.</p>
                        <a href="{% url 'campaigns:list' %}" class="btn btn-outline-primary px-4">Clear all filters</a>
                    </div>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/campaigns/list.html', explore_html)

# 6. Campaign Detail Page (campaigns/detail.html)
detail_html = """
{% extends 'base.html' %}
{% block title %}{{ campaign.title }} - BackerWave{% endblock %}

{% block content %}
<div class="bg-surface border-bottom border-subtle pt-4 pb-5">
    <div class="container">
        <!-- Header -->
        <div class="text-center mb-5 max-w-700 mx-auto" style="max-width: 800px;">
            <a href="{% url 'campaigns:list' %}?category={{ campaign.category.slug }}" class="badge bg-primary-subtle text-primary mb-3 px-3 py-2 rounded-pill fw-medium border border-primary-subtle text-decoration-none">{{ campaign.category.name }}</a>
            <h1 class="display-6 fw-bold mb-3">{{ campaign.title }}</h1>
            <p class="lead text-muted">{{ campaign.short_description }}</p>
        </div>

        <div class="row gy-5">
            <!-- Media & Story -->
            <div class="col-lg-7 col-xl-8">
                <div class="card border-0 shadow-sm rounded-4 overflow-hidden mb-4 bg-light">
                    {% if campaign.campaign_image %}
                        <img src="{{ campaign.campaign_image.url }}" class="w-100 object-fit-cover" style="max-height: 500px;" alt="{{ campaign.title }}">
                    {% else %}
                        <div class="w-100 d-flex align-items-center justify-content-center text-muted" style="height: 400px;">
                            <i class="bi bi-image" style="font-size: 5rem;"></i>
                        </div>
                    {% endif %}
                </div>
                
                <ul class="nav nav-pills mb-4 gap-2 border-bottom border-subtle pb-3" id="campaignTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active rounded-pill px-4 fw-medium" id="story-tab" data-bs-toggle="pill" data-bs-target="#story" type="button" role="tab">Story</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link rounded-pill px-4 fw-medium" id="updates-tab" data-bs-toggle="pill" data-bs-target="#updates" type="button" role="tab">Updates <span class="badge bg-secondary ms-1 rounded-pill">{{ campaign.updates.count }}</span></button>
                    </li>
                </ul>
                
                <div class="tab-content" id="campaignTabsContent">
                    <div class="tab-pane fade show active" id="story" role="tabpanel">
                        <div class="content-body" style="font-size: 1.1rem; color: var(--text-secondary); line-height: 1.8;">
                            {{ campaign.description|linebreaks }}
                        </div>
                    </div>
                    <div class="tab-pane fade" id="updates" role="tabpanel">
                        <div class="d-flex justify-content-between align-items-center mb-4">
                            <h4 class="fw-bold mb-0">Project Updates</h4>
                            {% if request.user == campaign.creator %}
                                <a href="{% url 'campaigns:update_create' campaign.slug %}" class="btn btn-outline-primary btn-sm fw-bold px-3">Post Update</a>
                            {% endif %}
                        </div>
                        
                        {% for update in campaign.updates.all|dictsortreversed:"created_at" %}
                            <div class="card border-subtle shadow-sm rounded-4 mb-4">
                                <div class="card-body p-4">
                                    <div class="d-flex align-items-center gap-3 mb-3">
                                        <div class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                                            <i class="bi bi-megaphone"></i>
                                        </div>
                                        <div>
                                            <h5 class="fw-bold mb-0">{{ update.title }}</h5>
                                            <small class="text-muted">{{ update.created_at|date:"F j, Y" }}</small>
                                        </div>
                                    </div>
                                    <p class="text-secondary mb-0">{{ update.content|linebreaks }}</p>
                                    {% if update.image %}
                                        <img src="{{ update.image.url }}" class="img-fluid rounded-3 mt-3 shadow-sm border border-subtle">
                                    {% endif %}
                                </div>
                            </div>
                        {% empty %}
                            <div class="text-center py-5 bg-light rounded-4 border border-subtle">
                                <i class="bi bi-journal-x fs-1 text-muted mb-3 d-block"></i>
                                <h5 class="fw-bold text-muted">No updates yet</h5>
                                <p class="text-muted small mb-0">The creator hasn't posted any updates.</p>
                            </div>
                        {% endfor %}
                    </div>
                </div>
            </div>

            <!-- Funding Widget Sidebar -->
            <div class="col-lg-5 col-xl-4">
                <div class="position-sticky" style="top: 100px;">
                    <div class="card border-subtle shadow-md rounded-4 mb-4">
                        <div class="card-body p-4">
                            <div class="progress mb-4" style="height: 10px;">
                                <div class="progress-bar bg-success rounded-pill" role="progressbar" style="width: {{ campaign.progress_percentage }}%"></div>
                            </div>
                            
                            <h2 class="display-6 fw-bold text-success mb-1">${{ campaign.current_amount }}</h2>
                            <p class="text-muted fw-medium mb-4">raised of ${{ campaign.goal_amount }} goal</p>
                            
                            <div class="row g-3 mb-4">
                                <div class="col-6">
                                    <h4 class="fw-bold mb-1">{{ campaign.contributions.count }}</h4>
                                    <span class="text-muted text-small fw-medium">Backers</span>
                                </div>
                                <div class="col-6">
                                    <h4 class="fw-bold mb-1">{{ campaign.end_date|timeuntil|slice:":3"|default:"0" }}</h4>
                                    <span class="text-muted text-small fw-medium">Days to go</span>
                                </div>
                            </div>
                            
                            {% if campaign.status == 'ACTIVE' %}
                                <a href="{% url 'contributions:support' campaign.slug %}" class="btn btn-success btn-lg w-100 fw-bold shadow-sm mb-3 py-3">Support This Project</a>
                            {% else %}
                                <button class="btn btn-secondary btn-lg w-100 fw-bold shadow-sm mb-3 py-3" disabled>Project Closed</button>
                            {% endif %}
                            
                            <div class="d-flex gap-2">
                                {% if user.is_authenticated %}
                                    <form method="post" action="{% url 'campaigns:favorite' campaign.slug %}" class="w-100">
                                        {% csrf_token %}
                                        <button type="submit" class="btn {% if is_favorited %}btn-danger{% else %}btn-outline-secondary{% endif %} w-100 fw-medium">
                                            <i class="bi {% if is_favorited %}bi-heart-fill{% else %}bi-heart{% endif %} me-2"></i> 
                                            {% if is_favorited %}Saved{% else %}Save{% endif %}
                                        </button>
                                    </form>
                                {% endif %}
                                <button class="btn btn-outline-secondary w-100 fw-medium" onclick="navigator.clipboard.writeText(window.location.href); alert('Link copied!');"><i class="bi bi-share me-2"></i> Share</button>
                            </div>
                            
                            <p class="text-center text-caption text-muted mt-3 mb-0"><i class="bi bi-shield-check text-success"></i> All mock payments are securely simulated.</p>
                        </div>
                    </div>

                    <!-- Creator Card -->
                    <div class="card border-0 bg-light rounded-4">
                        <div class="card-body p-4 text-center">
                            {% if campaign.creator.profile.profile_image %}
                                <img src="{{ campaign.creator.profile.profile_image.url }}" class="rounded-circle shadow-sm mb-3 object-fit-cover" width="80" height="80">
                            {% else %}
                                <div class="rounded-circle bg-primary text-white shadow-sm d-inline-flex align-items-center justify-content-center mb-3" style="width:80px; height:80px; font-size:2rem;">
                                    {{ campaign.creator.username|make_list|first|upper }}
                                </div>
                            {% endif %}
                            <h5 class="fw-bold mb-1">{{ campaign.creator.profile.full_name|default:campaign.creator.username }}</h5>
                            <p class="text-muted text-small mb-3">Creator • Joined {{ campaign.creator.date_joined|date:"M Y" }}</p>
                            <a href="{% url 'campaigns:creator_profile' campaign.creator.username %}" class="btn btn-outline-primary btn-sm rounded-pill px-4 fw-medium">View Profile</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
write_file('templates/campaigns/detail.html', detail_html)
