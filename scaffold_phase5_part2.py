import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

def append_to_file(path, content):
    with open(path, 'a', encoding='utf-8') as f:
        f.write('\n' + content.strip() + '\n')

def replace_in_file(path, old, new):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.replace(old, new))

# 1. Add .env.example
env_example = """
DEBUG=False
SECRET_KEY=generate-a-secure-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost,yourdomain.com
"""
write_file('.env.example', env_example)

# 2. Add File upload security validators to core/validators.py
validators_py = """
from django.core.exceptions import ValidationError
import os

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only JPG, PNG, and WebP are allowed.')

def validate_file_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:
        raise ValidationError("You cannot upload files larger than 5MB.")
"""
write_file('core/validators.py', validators_py)

# 3. Apply validators to models
replace_in_file('campaigns/models.py', 
    "campaign_image = models.ImageField(upload_to='campaigns/', blank=True, null=True)",
    "campaign_image = models.ImageField(upload_to='campaigns/', blank=True, null=True, validators=[validate_image_extension, validate_file_size])")

replace_in_file('campaigns/models.py', 
    "image = models.ImageField(upload_to='updates/', blank=True, null=True)",
    "image = models.ImageField(upload_to='updates/', blank=True, null=True, validators=[validate_image_extension, validate_file_size])")

replace_in_file('accounts/models.py', 
    "profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)",
    "profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True, validators=[validate_image_extension, validate_file_size])")

# Ensure imports for validators
replace_in_file('campaigns/models.py', "from django.db.models import Q", "from django.db.models import Q\nfrom core.validators import validate_image_extension, validate_file_size")
replace_in_file('accounts/models.py', "from django.db import models", "from django.db import models\nfrom core.validators import validate_image_extension, validate_file_size")

# 4. Add advanced edge case tests
edge_tests = """
    def test_negative_goal_constraint(self):
        from django.db.utils import IntegrityError
        with self.assertRaises(IntegrityError):
            Campaign.objects.create(
                creator=self.creator_user,
                title='Bad Goal',
                category=self.category,
                short_description='Short',
                description='Long',
                goal_amount=-50,
                current_amount=0,
                start_date=date.today(),
                end_date=date.today() + timedelta(days=30),
                status='DRAFT'
            )

    def test_campaign_ownership_enforcement(self):
        self.client.login(username='contributor', password='password123')
        # Contributor tries to edit creator's campaign
        response = self.client.post(reverse('campaigns:edit', args=[self.campaign.slug]), {
            'title': 'Hacked Title'
        })
        self.assertEqual(response.status_code, 302)
        self.campaign.refresh_from_db()
        self.assertNotEqual(self.campaign.title, 'Hacked Title')
"""
append_to_file('campaigns/tests.py', edge_tests)

edge_tests_contrib = """
    def test_negative_contribution_constraint(self):
        from django.db.utils import IntegrityError
        with self.assertRaises(IntegrityError):
            Contribution.objects.create(
                contributor=self.contributor,
                campaign=self.campaign,
                amount=-10,
                status='PENDING',
                transaction_reference='MOCK-123'
            )
"""
append_to_file('contributions/tests.py', edge_tests_contrib)
