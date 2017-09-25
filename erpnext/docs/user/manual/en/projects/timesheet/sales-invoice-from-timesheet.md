#Sales Invoice from Timesheet

Customer can be invoiced based on total no. of hours your Employees has worked for that Customer. Timesheet can be used to track actual no. of hours Employee has worked. For example, in the IT services domain, clients are billed based on man-hour bases, where per hour billing cost is pre-determined.s

###Timesheet

####Step 1: Create new Timesheet

To create new Timesheet, go to:

`Project > Timesheet > New`

#### Step 2: Select Employee

In the Employee field, only ones having ative Salary Structure will be selectable. Further in the Salary Structure , is created for the E on the actual hours worked, Employee can create Timesheet. To be able to create Sales Invoice against this Timesheet, ensure `Billable` field is checked.

<<<<<<< HEAD
<img class="screenshot" alt="Sales Invoice" src="/docs/assets/img/project/timesheet/timesheet-salary-structure.png">
=======
<img class="screenshot" alt="Sales Invoice" src="{{docs_base_url}}/assets/img/project/timesheet/timesheet-salary-structure.png">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

#### Step 3:Activity Type

Employee will have to select an Activity Type (like planning, site visit, repairing etc. ). Costing and Billing Rate for each Activity can be different for each Employee. These cost can be tracked in the Activity Cost. On selection of Activity Type, Activity Cost is fetched from that Employee. Based on total Activity Cost and total no. of hours, Total Billing Amount (to the Customer) is calculated.

<<<<<<< HEAD
To learn more on how to setup Activity Type and Activity Cost, click [here](/docs/user/manual/en/projects/articles/project-costing).

<img class="screenshot" alt="Sales Invoice" src="/docs/assets/img/project/timesheet/timesheet-cost.png">
=======
To learn more on how to setup Activity Type and Activity Cost, click [here]({{docs_base_url}}/user/manual/en/projects/articles/project-costing).

<img class="screenshot" alt="Sales Invoice" src="{{docs_base_url}}/assets/img/project/timesheet/timesheet-cost.png">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

#### Step 4: Enter Actual Time

In the Timesheet Details table, enter actual hours an Employee has worked for. One Timesheet can be used for multiple days as well.

To be able to create Sales Invoice from the Time Sheet, ensure 'Is Billable' field is checked.

<<<<<<< HEAD
<img class="screenshot" alt="Sales Invoice" src="/docs/assets/img/project//timesheet/timesheet-billable.png">
=======
<img class="screenshot" alt="Sales Invoice" src="{{docs_base_url}}/assets/img/project//timesheet/timesheet-billable.png">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

Based on the actual hours worked and Activity Cost of an Employee, Total Billing Amount will be calculated for Timesheet.

#### Step 5: Save and Submit

After submitting Timesheet, you will find buttons to create Sales Invoice and Salary Slip against this Timesheet.

<<<<<<< HEAD
<img class="screenshot" alt="Sales Invoice" src="/docs/assets//img/project/timesheet/timesheet-total.png">
=======
<img class="screenshot" alt="Sales Invoice" src="{{docs_base_url}}/assets//img/project/timesheet/timesheet-total.png">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

###Create Sales Invoice from Timesheet

#### Submitted Timesheet

In the Timesheet, if "Is Billable" is checked, you will find option to create Sales Invoice against it.

<<<<<<< HEAD
<img class="screenshot" alt="Sales Invoice" src="/docs/assets/img/project/timesheet/timesheet-invoice-1.png">

<img class="screenshot" alt="Sales Invoice timesheet" src="{{docs_base_url}}/assets/img/project/timesheet/make_invoice_from_timesheet.gif">
=======
<img class="screenshot" alt="Sales Invoice" src="{{docs_base_url}}/assets/img/project/timesheet/timesheet-invoice-1.png">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

####Sales Invoice

Sales Invoice has dedicated table for the Timesheet table where Timesheet details will be updated. You can select more Timesheets in this table.

<<<<<<< HEAD
<img class="screenshot" alt="Sales Invoice" src="/docs/assets/img/project/timesheet/timesheet-to-invoice.gif">
=======
<img class="screenshot" alt="Sales Invoice" src="{{docs_base_url}}/assets/img/project/timesheet/timesheet-to-invoice.gif">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347


####Select Customer and Item

Select Customer to be billed. Select an Item, and enter rate as the billing amount.

####Save

After enter all required details in the Sales Invoice, Save and Submit it.

On submitting Sales Invoice, status of the Timesheets linked to the Sales Invoice will be updated as Billed.

<<<<<<< HEAD
<img class="screenshot" alt="Sales Invoice" src="/docs/assets/img/project/timesheet/timesheet-billed.png">
=======
<img class="screenshot" alt="Sales Invoice" src="{{docs_base_url}}/assets/img/project/timesheet/timesheet-billed.png">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
