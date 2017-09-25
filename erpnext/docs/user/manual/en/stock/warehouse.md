<<<<<<< HEAD
# Warehouse

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
A warehouse is a commercial building for storage of goods. Warehouses are used
by manufacturers, importers, exporters, wholesalers, transport businesses,
customs, etc. They are usually large plain buildings in industrial areas of
cities, towns, and villages. They mostly have loading docks to load and unload
goods from trucks.

<<<<<<< HEAD
The terminology of 'Warehouse" in ERPNext is a bit broader though and maybe can be 
regarded as "storage locations". For example you can create a sub-Warehouse which 
practically is a shelf inside your actual location. 
This can become quite a detailed Tree like >Warehouse >Room >Row >Shelf >Box

To go to Warehouse, click on Stock and go to Warehouse under Setup.  You
could also switch to 'Tree' View or simply type warehouse tree in the awsone bar.

<img class="screenshot" alt="Warehouse" src="/docs/assets/img/stock/warehouse.png">

In ERPNext, every Warehouse must belong to a specific company, to maintain
company wise stock balance. In order to do so each Warehouse is linked with an 
Account in the Chart of Accounts (by default of the the same name as the Warehouse 
itself) which captures the monetary equivalent of the goods or materials stored 
in that specific warehouse. If you have a more detailed Warehouse Tree as the one 
described above most likely it's a good idea to link the sub-locations (>room >row >Shelf, ...)
to the account of the actual Warehouse (the root Warehouse of that Tree) as most 
scenarios do not require to account for value of stock items per Shelf or Box.

Warehouses are saved with their respective company’s abbreviations. This facilitates 
identifying which Warehouse belongs to which company, at a glance.
=======
To go to Warehouse, click on Stock and go to Warehouse under Masters.  You
could also go to the Setup module and click on Warehouse under Master Data.

> Stock > Warehouse > New Warehouse

<img class="screenshot" alt="Warehouse" src="{{docs_base_url}}/assets/img/stock/warehouse.png">

In ERPNext, every Warehouse must belong to a specific company, to maintain
company wise stock balance. The Warehouses are saved with their respective
company’s abbreviations. This facilitates in identifying which Warehouse
belongs to which company, at a glance.
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

You can include user restrictions for these Warehouses. In case you do not
wish a particular user to operate on a particular Warehouse, you can refrain
the user from accessing that Warehouse.

<<<<<<< HEAD
=======
### Merge Warehouse

In day to day transactions, duplicate entries are done by mistake, resulting
in duplicate Warehouses. Duplicate records can be merged into a single
Warehouse. From the top bar of the system select the File menu. Select Rename
and Enter the correct Warehouse and check the Merge button. The system will
replace all the links of wrong Warehouse with the correct Warehouse, in all
transactions. Also, the available quantity (actual qty, reserved qty, ordered
qty etc) of all items in the duplicate warehouse will be transferred to the
correct warehouse. Once merging is done, delete the duplicate Warehouse.

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
> Note: ERPNext system maintains stock balance for every distinct combination
of Item and Warehouse. Thus you can get stock balance for any specific Item in
a particular Warehouse on any particular date.

{next}
