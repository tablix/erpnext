# Point of Sale Invoice

For retail operations, the delivery of goods, accrual of sale and payment all happens in one event, that is usually called the “Point of Sale” (POS).

<iframe width="660" height="371" src="https://www.youtube.com/embed/4WkelWkbP_c" frameborder="0" allowfullscreen></iframe>

###Offline POS

In the retails business, invoicing needs to done very quickly, hence should less dependency. In the ERPNext, you can create POS Invoices, even when not connected to the internet.

POS Invoices created in the offline mode will be saved locally in the browser. If internet connection is lost which creating POS Invoice, you will still be able can proceed forward. Once internet connection is available again, offline invoices will be synced, and pushed onto your ERPNext account. To learn more on how POS Invoices can be created when offline, [check here.](https://frappe.io/blog/blog/erpnext-features/offline-pos-in-erpnext-7)

#### POS Profile

In ERPNext all Sales and Purchase transactions, like Sales Invoice, Quotation, Sales Order, Purchase Order etc. can be edited via the POS. There two steps to Setup POS:

1. Enable POS View via (Setup > Customize > Feature Setup)
<<<<<<< HEAD
2. Create a [POS Profile](/docs/user/manual/en/setting-up/pos-setting.html) record
=======
2. Create a [POS Setting]({{docs_base_url}}/user/manual/en/setting-up/pos-setting.html) record
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

#### Different sections of the POS

  * Update Stock: If this is checked, Stock Ledger Entries will be made when you “Submit” this Sales Invoice thereby eliminating the need for a separate Delivery Note.
  * In your Items table, update inventory information like Warehouse (saved as default), Serial Number, or Batch Number if applicable.
  * Update Payment Details like your Bank / Cash Account, Paid amount etc.
  * If you are writing off certain amount. For example when you receive extra cash as a result of not having exact denomination of change, check on ‘Write off Outstanding Amount’ and set the Account.


### Customer

<<<<<<< HEAD
In POS, user can select the existing customer during making an order or create the new customer. This features works in the offline mode also. User can also add the customer details like contact number, address details etc on the form. The customer which has been created from the POS will be synced when the internet connection is active.

<img class="screenshot" alt="POS Customer" src="/docs/assets/img/accounts/pos-customer.png">
=======
You can select one of the existing Customer from the Customer master. If Customer doesn't exist in the Customer master, enter Customer Name in the POS Invoice view itself. On creation of POS Invoice, Customer will be auto-created in the Customer master.

<img class="screenshot" alt="POS Customer" src="{{docs_base_url}}/assets/img/accounts/pos-customer.png">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

### Adding an Item

At the billing counter, the retailer needs to select Items which the consumer buys. In the POS interface you can select an Item by two methods. One, is by clicking on the Item image and the other, is through the Barcode / Serial No.

**Select Item** \- To select a product click on the Item image and add it into the cart. A cart is an area that prepares a customer for checkout by allowing to edit product information, adjust taxes and add discounts.

**Barcode / Serial No** \- A Barcode / Serial No is an optical machine-readable representation of data relating to the object to which it is attached. Enter Barcode / Serial No in the box as shown in the image below and pause for a second, the item will be automatically added to the cart.

<<<<<<< HEAD
<img class="screenshot" alt="POS Item" src="/docs/assets/img/accounts/pos-item.png">
=======
<img class="screenshot" alt="POS Item" src="{{docs_base_url}}/assets/img/accounts/pos-item.png">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

> Tip: To change the quantity of an Item, enter your desired quantity in the
quantity box. These are mostly used if the same Item is purchased in bulk.

If your product list is very long use the Search field, type the product name
in Search box.

<<<<<<< HEAD
### Removing an Item from the Cart

1. Select row in the cart and clik on delete button in the numeric keypad
  
<img class="screenshot" alt="POS Item" src="/docs/assets/img/accounts/pos_deleted_item.gif">


2. Set Qty as zero to remove Item from the POS invoice. There are two ways to remove an Item.
=======
### Removing an Item

Set Qty as zero to remove Item from the POS invoice. There are two ways to remove an Item.
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

  * If Item's Qty is 1, click on a minus sign to make it zero.

  * Manually enter 0(zero) quantity.

### Make Payment

After all the Items and their quantities are added into the cart, you are
ready to make the Payment. Payment process is divided into 3 steps -

  1. Click on “Make Payment” to get the Payment window.
  2. Select your “Mode of Payment”.
  3. Click on “Pay” button to Save the document.
  
<<<<<<< HEAD
<img class="screenshot" alt="POS Payment" src="/docs/assets/img/accounts/pos-payment.png">
=======
<img class="screenshot" alt="POS Payment" src="{{docs_base_url}}/assets/img/accounts/pos-payment.png">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

Submit the document to finalise the record. After the document is submitted,
you can either print or email it directly to the customer.

<<<<<<< HEAD
### Write off Amount

Outstanding amount can be write off from the POS, user has to enter the amount under write off field on the payment screen.

<img class="screenshot" alt="POS Payment" src="/docs/assets/img/accounts/write-off.png">

System books the write off amount into the ledger which has selected on the POS Profile.

### Change Amount

POS calculate the extra amount paid by the customer, which user can return from the cash account. User has to set the account for the change amount on the POS profile.

<img class="screenshot" alt="POS Payment" src="/docs/assets/img/accounts/change-amount.png">

### Offline Records
All the records from the POS stores into the browser's local storegae and sync submitted records after every minute of the interval if system is connected to internet. User can view the offline records by clicking on Menu > View Offline Records

<img class="screenshot" alt="POS Payment" src="/docs/assets/img/accounts/offline-records.png">

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
#### Accounting entries (GL Entry) for a Point of Sale:

Debits:

  * Customer (grand total) 
  * Bank / Cash (payment)

Credits:

  * Income (net total, minus taxes for each Item) 
  * Taxes (liabilities to be paid to the government)
  * Customer (payment)
  * Write Off (optional)
<<<<<<< HEAD
  * Account for Change Amount (optional)

To see entries after “Submit”, click on “View Ledger”.

### Email
User can send email from the POS, after submission of an order, user has to click on menu > email
<img class="screenshot" alt="POS Payment" src="/docs/assets/img/accounts/pos-email.png">
After sync of an order, email sent to the customer with the print of the bill in the attachment

=======

To see entries after “Submit”, click on “View Ledger”.

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
{next}
