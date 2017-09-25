# User Permissions

<<<<<<< HEAD
Along with Role based permissions, you can also set user level permissions that are based on rules that are evaluated against the data containted in the document being accessed. This is particularly useful when you want to restrict based on:

1. Allow user to access data belonging to one Company
1. Allow user to access data related to a specific Customer or Territory

### Creating User Permissions

To create a User Permission, go to Setup > Permission > User Permissions

When you create a new record you will have to specify

1. The user for which the rule has to be applied
1. The type of document which will be allowed (for example "Company")
1. The specific item that you want to allow (the name of the "Company)

<img src="/docs/assets/img/users-and-permissions/user-perms/new-user-permission.png" class="screenshot" alt="Creating a new user permission">

If you want to apply the permissions to all Roles for that user, keep the "Apply Permissions for all Roles of this User" checked. If you check this, it will automatically setup the rules for Roles to check for User Permissions.

### Choosing Which Roles to Apply

You can also manually edit the the roles for which you want the user permissions to apply. To do that go the the **Role Permission Manager** and select the role for which you want to Edit the User Permissions.

Note that the "Apply User Permissions" is already checked for this role. Then click on "Select Document Types"

<img src="/docs/assets/img/users-and-permissions/user-perms/select-document-types.png" class="screenshot" alt="Select Document Types to Edit the Setting">

Here you will see that Company has already been checked. If you want user permissions not be applied for that particular rule, you can un check it.

<img src="/docs/assets/img/users-and-permissions/user-perms/view-selected-documents.png" class="screenshot" alt="Select Document Types to Edit the Setting">

### Ignoring User Permissions on Certain Fields

Another way of allowing documents to be seen that have been restricited by User Permissions is to check "Ignore User Permissions" on a particular field by going to **Customize Form**

For example you don't want Assets to be restricited for any user, then select **Asset** in **Customize Form** and in the Company field, check on "Ignore User Permissions"

<img src="/docs/assets/img/users-and-permissions/user-perms/ignore-user-user-permissions.png" class="screenshot" alt="Ignore User Permissions on specific properties">

### Strict Permisssions

Since User Permissions are applied via Roles, there may be many users belonging to a particular Role. Suppose you have three users belonging to Role "Accounts User" and you have applied **User Permissions** to only one user, then the permissions will only be restricted to that user.

You can change this setting incase you want the user permissions to be assigned to all users, even if they are not assigned any user permissions by going to **System Settings** and checking "Apply Strict User Permissions"

### Checking How User Permissions are Applied

Finally once you have created your air-tight permission model, and you want to check how it applies to various users, you can see it via the **Permitted Documents for User** report. Using this report, you can select the **User** and document type and check how user permissions get applied.

<img src="/docs/assets/img/users-and-permissions/user-perms/permitted-documents.png" class="screenshot" alt="Permitted Documents for User report">
=======
Role Base Permissions define the periphery of document types within which a user with a set of Roles can move around in. However, you can have an even finer control by defining User Permissions for a User. By setting specific documents in User Permissions list, you can limit access for that User to specific documents of a particular DocType, on the condition that "Apply User Permissions" is checked in Role Permissions Manager.

To start with, go to:

> Setup > Permissions > User Permissions Manager

User Permissions Manager displaying how users can access only a specific Company.

#### Example

User 'tom.hagen@riosolutions.com' has Sales User role and we want to limit the user to access records for only a specific Company 'Rio Solutions'.

  1. We add a User Permissions row for Company.
	
	<img src="{{docs_base_url}}/assets/img/users-and-permissions/user-permissions-new.gif" class="screen" alt="User Permissions For Company">

	Add User Permissions row for a combination of User 'tom.hagen@riosolutions.com' and Company 'Rio Solutions'.

  1. Also Role "All" has only Read permission for Company, with 'Apply User Permissions' checked.
	
	<img src="{{docs_base_url}}/assets/img/users-and-permissions/user-permissions-company-role-all.png" class="screen" alt="Role Permissions for All on Company">

	Read Permission with Apply User Permissions checked for DocType Company.

  1. The combined effect of the above two rules lead to User 'tom.hagen@riosolutions.com' having only Read access to Company 'Rio Solutions'.
	
	<img src="{{docs_base_url}}/assets/img/users-and-permissions/user-permission-company.png" class="screen" alt="Effect of Role and User Permissions on Company">
	
	Access is limited to Company 'Rio Solutions'.

  1. We want this User Permission on Company to get applied on other documents like Quotation, Sales Order, etc.
	 
	 These forms have a **Link Field based on Company**. As a result, User Permissions on Company also get applied on these documents, which leads to User 'tom.hagen@riosolutions' to acces these documents having Company 'Rio Solutions'.

    <img class="screen" alt="Sales User Role Permissions for Quotation" src="{{docs_base_url}}/assets/img/users-and-permissions/user-permissions-quotation-sales-user.png" >
	 
	 Users with Sales User Role can Read, Write, Create, Submit and Cancel Quotations based on their User Permissions, since 'Apply User Permissions' is checked.

	<img src="{{docs_base_url}}/assets/img/users-and-permissions/user-permission-quotation.png" class="screenshot" alt="Quotation List limited to results for Company 'Rio Solutions'">

	Quotation List is limited to results for Company 'Rio Solutions' for User 'tom.hagen@riosolutions.com'.

  1. User Permissions get applied automatically based on Link Fields, just like how it worked for Quotation. But, Lead Form has 4 Link fields: Territory, Company, Lead Owner and Next Contact By. Say, you want Leads to limit access to Users based only on Territory, even though you have defined User Permissions for DocTypes User, Territory and Company. You can do this by setting 'Ignore User Permissions' for Link fields: Company, Lead Owner and Next Contact By.  
    
<img src="{{docs_base_url}}/assets/img/users-and-permissions/user-permissions-lead-role-permissions.png" class="screen" alt="Role Permissions on Lead for Sales User Role">

Sales User can Read, Write and Create Leads limited by User Permissions.

<img src="{{docs_base_url}}/assets/img/users-and-permissions/user-permissions-ignore-user-permissions.png" class="screenshot" alt="Set Ingore User Permissions from Setup > Customize > Customize Form">	

Check 'Ingore User Permissions' for Company, Lead Owner and Next Contact By fields using Setup > Customize > Customize Form for Lead.

<img src="{{docs_base_url}}/assets/img/users-and-permissions/permissions-lead-list.png" class="screenshot" alt="Lead List is limited to records with Territory 'United States'">	

Due to the effect of the above combination, User 'tom.hagen@riosolutions.com' can only access Leads with Territory 'United States'.

{next}

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
