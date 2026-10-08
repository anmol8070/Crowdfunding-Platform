import os

def replace_in_file(path, old, new):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.replace(old, new))

# Enhance Navbar responsiveness in base.html
replace_in_file('templates/base.html',
"""                <div class="d-flex align-items-center gap-3 flex-wrap">
                    <form action="{% url 'campaigns:list' %}" method="get" class="position-relative d-none d-lg-block">""",
"""                <div class="d-flex flex-lg-row flex-column align-items-lg-center gap-3 mt-3 mt-lg-0">
                    <form action="{% url 'campaigns:list' %}" method="get" class="position-relative d-none d-lg-block">""")

# Make sure the search form shows on mobile too, but stacked
replace_in_file('templates/base.html',
"""<form action="{% url 'campaigns:list' %}" method="get" class="position-relative d-none d-lg-block">
                        <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                        <input type="text" name="q" class="form-control rounded-pill ps-5 bg-light border-0" placeholder="Search projects..." style="width: 250px;">
                    </form>""",
"""<form action="{% url 'campaigns:list' %}" method="get" class="position-relative d-block d-lg-block w-100">
                        <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                        <input type="text" name="q" class="form-control rounded-pill ps-5 bg-light border-0 w-100 w-lg-auto" placeholder="Search projects..." style="max-width: 100%;">
                    </form>""")

# Enhance button responsiveness on mobile
replace_in_file('templates/base.html',
"""<a href="{% url 'campaigns:create' %}" class="btn btn-primary d-none d-lg-block">Start a Campaign</a>""",
"""<a href="{% url 'campaigns:create' %}" class="btn btn-primary d-block d-lg-inline-block w-100 text-center mt-2 mt-lg-0">Start a Campaign</a>""")

# Make notification bell align correctly in mobile column layout
replace_in_file('templates/base.html',
"""<a href="{% url 'core:notifications' %}" class="position-relative text-dark text-decoration-none fs-5">""",
"""<a href="{% url 'core:notifications' %}" class="position-relative text-dark text-decoration-none fs-5 d-inline-block">""")
