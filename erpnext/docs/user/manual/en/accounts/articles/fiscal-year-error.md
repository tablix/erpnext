# Fixing Fiscal Year Error

While creating any entry, system validates if dates (like Posting Date, Transaction Date etc.) belongs to Fiscal Year selected. If not, system through an error message saying:

`Date ##-##-#### not in fiscal year`

You are more likely to receive this error message if your Fiscal Year has changes, but new Fiscal Year still not set a default. To ensure new Fiscal Year is auto updated in the transactions, you should setup your master as instructed below.

#### Create New Fiscal Year

Only User with System Manager's Role Assigned has permission to create new Fiscal Year. To create new Fiscal Year, go to:

`Accounts > Setup > Fiscal Year`

<<<<<<< HEAD
Click [here](/docs/user/manual/en/accounts/setup/fiscal-year.html) to learn more about Fiscal Year.
=======
Click [here]({{docs_base_url}}/user/manual/en/accounts/setup/fiscal-year.html) to learn more about Fiscal Year.
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

#### Set Fiscal Year as Default

After Fiscal Year is saved, you will find option to set that Fiscal year as Default.

<<<<<<< HEAD
<img alt="Debit Credit Not Equal" class="screenshot" src="/docs/assets/img/articles/fiscal-year-error-1.png">
=======
<img alt="Debit Credit Not Equal" class="screenshot" src="{{docs_base_url}}/assets/img/articles/fiscal-year-error-1.png">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

Default Fiscal Year will be updated in the Global Default setting as well. You can manually update Default Fiscal Year from:

`Setup > Settings > Global Default`

<<<<<<< HEAD
<img alt="Debit Credit Not Equal" class="screenshot" src="/docs/assets/img/articles/fiscal-year-error-2.png">
=======
<img alt="Debit Credit Not Equal" class="screenshot" src="{{docs_base_url}}/assets/img/articles/fiscal-year-error-2.png">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

Save Global Default, and Reload your ERPNext account. Then, default Fiscal Year will be auto-updated in your transactions.

Note: In transactions, you can manually select required Fiscal Year, from More Info section.

<!-- markdown -->