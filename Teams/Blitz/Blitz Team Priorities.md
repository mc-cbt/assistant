1. Payments 
	1. Conforma
2. Reconciliation
	1. Plaid
	2. Finicity
3. Back office accounting integration

Blob storage

Data types
1. Client data
2. System data
3. Reference data

IUR data from Sabre stored on a windows server called interface
Every invoice is a separate file

Conferma data comes from ftps

Conferma and Arc data needs to go into existing transactions table

Interface data table - is that the correct format? What does accounting want? Look at Agresso's format

1300 manual interventions per day in accounting. We think we can automate 95% of that. This is what they mean by replacing the travel module in Agresso. 

Potentially we become the travel module for NetSuite or other ERP systems. We use Agresso because it's the only ERP that pulls in travel 

Temporal!!!!

---

- (2026-06-29, see [[Daily/2026-06-29]]) **Virtual cards admin** — [[Kyle Crowther]]'s epic, to be built by [[Peter Welty]] (currently blocked by DevOps). See [[Projects/Virtual Cards/Virtual Cards]].
- (2026-08-20, see [[Teams/Blitz/Standup/2026-08-20]]) **ARC files contain unmasked card numbers** — both the legacy format and the new JSON file, including the new multiple-form-of-payment transactions. ARC offers **no masked-download option**, so the choice is the unmasked file or no file. We need to **mask or truncate at ingestion** (truncation is allowed under PCI); encryption alone isn't the answer since PCI cares about key origin, storage and access. Open question gating the design: **does expense need unmasked card data to match?** Reconciliation today matches on **ticket numbers** and doesn't. Prior art: masking to first-4/last-4 caused **false matches across clients**; first-6/last-4 behaved correctly. Mitigation available today — ARC masks per user in the UI but not in the file download, so **restrict who can download**. Follow-up owner: [[Mike Harris]] + [[James Proctor]] on ARC access.
- (2026-08-20, see [[Teams/Blitz/Standup/2026-08-20]]) **Temporal is live** — namespaces for dev/stage/prod, deployed to prod with schedules per workflow and a successful test run. Old ARC scrape cron schedules to be decommissioned.

### Future priorities

- (2026-06-30, see [[Teams/Blitz/Standup/2026-06-30]]) **Multi-currency support** — show values in different currencies, configurable per client. Driven by signing clients in different countries. Related: duplicating the Agresso exchange-rate storage workflow in Andavo (after the Temporal work) and storing invoice data via workflows. See [[Projects/Foreign Currency/Foreign Currency]].

