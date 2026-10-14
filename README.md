# B2B Lead Prospector & Contact Enrichment

Apify Actor that extracts verified local business leads from Yellow Pages and enriches them with emails and social links.

## Input
- searchQuery: Business category/niche, default Dentists
- location: City and State, default Austin, TX
- maxResults: Max leads to collect, default 10
- extractSocials: Enable website enrichment, default 	rue

## Output
Each lead contains:
- business_name, category, target_location, phone, website, address, rating, email, linkedin, facebook, instagram

## Pricing
Pay-per-event: lead-extracted .0025 per enriched lead.
