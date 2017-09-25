<<<<<<< HEAD
# Expense Claim

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
Expense Claim is made when Employee’s make expenses out of their pocket on behalf of the company. For example, if they take a customer out for lunch, they can make a request for reimbursement via the Expense Claim form.

To make a new Expense Claim, go to:

> HR > Expense Claim > New Expense Claim

<<<<<<< HEAD
<img class="screenshot" alt="Expense Claim" src="/docs/assets/img/human-resources/expense_claim.png">
=======
<img class="screenshot" alt="Expense Claim" src="{{docs_base_url}}/assets/img/human-resources/expense_claim.png">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

Set the Employee ID, date and the list of expenses that are to be claimed and
“Submit” the record.

<<<<<<< HEAD
### Set Account for Employee
Set employee's expense account on the employee form, system books an expense amount of an employee under this account.
<img class="screenshot" alt="Expense Claim" src="/docs/assets/img/human-resources/employee_account.png">

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
### Approving Expenses

Approver for the Expense Claim is selected by an Employee himself. Users to whom `Expense Approver` role is assigned will shown in the Expense Claim Approver field.

<<<<<<< HEAD
After saving Expense Claim, Employee should [Assign document to Approver](/docs/user/manual/en/using-eprnext/assignment.html). On assignment, approving user will also receive email notification. To automate email notification, you can also setup [Email Alert](/docs/user/manual/en/setting-up/email/email-alerts.html).
=======
After saving Expense Claim, Employee should [Assign document to Approver]({{docs_base_url}}/user/manual/en/using-eprnext/assignment.html). On assignment, approving user will also receive email notification. To automate email notification, you can also setup [Email Alert]({{docs_base_url}}/user/manual/en/setting-up/email/email-alerts.html).
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

Expense Claim Approver can update the “Sanctioned Amounts” against Claimed Amount of an Employee. If submitting, Approval Status should be submitted to Approved or Rejected. If Approved, then Expense Claim gets submitted. If rejected, then Expen
Comments can be added in the Comments section explaining why the claim was approved or rejected.

<<<<<<< HEAD
### Booking the Expense

On submission of Expense Claim, system books an expense against the expense account and the employee account
<img class="screenshot" alt="Expense Claim" src="/docs/assets/img/human-resources/expense_claim_book.png">

User can view unpaid expense claim using report "Unclaimed Expense Claims"
<img class="screenshot" alt="Expense Claim" src="/docs/assets/img/human-resources/unclaimed_expense_claims.png">

### Payment for Expense Claim

To make payment against the expense claim, user has to click on Make > Bank Entry
#### Expense Claim
<img class="screenshot" alt="Expense Claim" src="/docs/assets/img/human-resources/payment.png">

#### Payment Entry
<img class="screenshot" alt="Expense Claim" src="{{docs_base_url}}/assets/img/human-resources/payment_entry.png">

Note: This amount should not be clubbed with Salary because the amount will then be taxable to the Employee.

Alternatively, a Payment Entry can be made for an employee and all outstanding Expense Claims will be pulled in.

> Accounts > Payment Entry > New Payment Entry

Set the Payment Type to "Pay", the Party Type to Employee, the Party to the employee being paid and the account being paid 
from. All outstanding expense claims will be pulled in and payments amounts can be allocated to each expense.
<img class="screenshot" alt="Expense Claim" src="{{docs_base_url}}/assets/img/human-resources/expense_claim_payment_entry.png">

### Managing Advance Payments

Sometimes an employee requires some advance payment before making expenses on behalf of the organisation. This can be managed from the Expense Claim

First make sure that the Default Advance Account has been set in the Company Master:

> Erpnext > Setup > Company

<img class="screenshot" alt="Expense Claim" src="{{docs_base_url}}/assets/img/human-resources/company_advance_account.png">

When creating the Expense Claim, check the 'Advance Payment Required' option

<img class="screenshot" alt="Expense Claim" src="{{docs_base_url}}/assets/img/human-resources/advance_payment_required.png">

After the Expense Claim is Saved and Approved by the Expense Approver, Journal Entry for Advance Payment can be raised by the accountant or user with appropriate permissions. To do that, just click on:

> Make > Advance Payment

<img class="screenshot" alt="Expense Claim" src="{{docs_base_url}}/assets/img/human-resources/make_advance_payment.png">

Note: Once the Expense Claim is Submitted, the button for making Advance Payment is no longer available. This is because expenses get booked on Submission of the Expense Claim and as such, the next logical step is settlement/reimbursement

Advance Payments are expected to be made 'before' the actual expenditure gets booked and settlement/reimbursement should be done against the Employee's Advance Account after submission of the Expense Claim
=======
### Booking the Expense and Reimbursement

The approved Expense Claim must then be converted into a Journal Entry and a
payment must be made. Note: This amount should not be clubbed with Salary
because the amount will then be taxable to the Employee.
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

### Linking with Task & Project

* To Link Expense Claim with Task or Project specify the Task or the Project while making an Expense Claim

<<<<<<< HEAD
<img class="screenshot" alt="Expense Claim - Project Link" src="/docs/assets/img/project/project_expense_claim_link.png">
=======
<img class="screenshot" alt="Expense Claim - Project Link" src="{{docs_base_url}}/assets/img/project/project_expense_claim_link.png">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

{next}
