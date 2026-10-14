# 🎯 B2B Lead Prospector & Contact Enrichment Engine

Fast, accurate, and cost-effective B2B lead generation. Automatically scrape local business profiles and deeply enrich each result with **verified emails, direct phone numbers, websites, physical addresses, and social media links** (LinkedIn, Facebook, Instagram).

---

## 🚀 Why Use This Actor?

* **⚡ Deep Contact Enrichment**: Extracts direct websites, emails, and company social profiles.
* **🛡️ Built-in Noise Filtering**: Filters out generic domains, invalid phone formats, and bot blockers.
* **💰 Transparent PPE Pricing**: Pay only **$0.0025 per enriched lead** ($2.50 per 1,000 leads). You never pay for empty queries or dead pages.
* **🔌 Automation Ready**: Integrates seamlessly with Make.com, Zapier, n8n, and custom Python/Node.js webhooks.

---

## 📥 Input Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `searchQuery` | String | `"Dentists"` | Business category, trade, or industry niche to target. |
| `location` | String | `"Austin, TX"` | City, State, or Metro region to prospect. |
| `maxResults` | Integer | `50` | Maximum number of verified leads to extract. |
| `extractSocials` | Boolean | `true` | Crawls official websites to extract emails and social profiles. |

---

## 📤 Output Dataset Format

Every record saved to your default dataset includes clean, standardized fields:

```json
{
  "business_name": "Austin Dental Arts",
  "category": "Dentists",
  "target_location": "Austin, TX",
  "phone": "+1 512-555-0199",
  "website": "https://www.austindentalarts.com",
  "address": "123 Congress Ave, Austin, TX 78701",
  "rating": "4.9",
  "email": "contact@austindentalarts.com",
  "linkedin": "https://www.linkedin.com/company/austin-dental-arts",
  "instagram": "https://www.instagram.com/austindentalarts",
  "facebook": "https://www.facebook.com/austindentalarts"
}
```

---

## 💡 Recommended Use Cases

1. **Cold Outreach & Email Campaigns**: Feed verified contact lists directly into Lemlist, Instantly, or Smartlead.
2. **CRM Ingestion**: Bulk-import localized B2B targets into HubSpot, Salesforce, or Pipedrive.
3. **Local Agency Prospecting**: Identify local service businesses lacking websites, social presence, or modern infrastructure.
