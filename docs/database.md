# Database Schema
## Relationships
- **User** 1:1 **Profile**
- **User** 1:N **Campaigns** (as creator)
- **User** 1:N **Contributions** (as contributor)
- **User** 1:N **FavoriteCampaigns**
- **User** 1:N **Notifications**

- **Category** 1:N **Campaigns**
- **Campaign** 1:N **Contributions**
- **Campaign** 1:N **CampaignUpdates**
- **Campaign** 1:N **FavoriteCampaigns**
