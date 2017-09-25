#Managing Transactions In Multiple Currency

In ERPNext, transactions can be created in the base currency as well as in parties (customer or supplier) currency. If transaction is created in the parties currency, their currency symbol is updated in the print format as well.

Let's consider a Sales Invoice, where your base currency is of a Company is USD and party currency is EUR.

#### Step 1: New Sales Invoice

`Accounts > Documents > Sales Invoice > New`

#### Step 2: Select Party

Select Customer from the Customer master. If default Currency is updated in the Customer master, same will be fetched in the Sales Invoice as well, as Customer Currency.

#### Step 3: Exchange Rate

Currency Exchange between base currency and customer currency will auto-fetch.

<<<<<<< HEAD
<img alt="Accounts Frozen Date" class="screenshot" src="/docs/assets/img/articles/multiple-currency-1.gif">
=======
<img alt="Accounts Frozen Date" class="screenshot" src="{{docs_base_url}}/assets/img/articles/multiple-currency-1.gif">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

#### Step 4: Update Details

Update other details like Item, Taxes, Terms. In the Taxes and other Charges table, charges of type Actual should be updated in the Customer's currency.

#### Step 4: Save and Submit

Save Sales Invoice and then check Print Format. For all the Currency field (rate, amount, totals) Customer's Currency symbol will be updated as well.

<<<<<<< HEAD
<img alt="Accounts Frozen Date" class="screenshot" src="/docs/assets/img/articles/multiple-currency-2.png">
=======
<img alt="Accounts Frozen Date" class="screenshot" src="{{docs_base_url}}/assets/img/articles/multiple-currency-2.png">
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

#### Currency Exchange Masters

If you have come to terms with party to follow standard exchange rate throughout, you can capture it by creating Currency Exchange Rate master. To create new Currency Exchange Rate master, go to:

`Accounts > Setup > Currency Exchange`

 If system find Exchange Rate master for any currency, it is given preference over currency exchange rate.

