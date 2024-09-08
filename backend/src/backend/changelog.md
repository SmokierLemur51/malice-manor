---------------------------------------------------------------------------
## [1.0.1] - 2024/09/

### Working On
- Fixing issue [1], not validating unique usernames.

- Fine tuning the user creation process, creating seed phrases for recovery.

### Added 

### Changed

---------------------------------------------------------------------------
## [1.0.0] - 2024/09/02

### Working on
- Creating and associating new vendor object with a user.

- Displaying vendor secret phrase in most efficient way.

- Desiging the vendor portal

### Added 
- New model, ListingDraft, to fix issue with selecting the SubCategory when a Vendor is 
creating a new Listing. The new process is now split out over two parts, creating a 
listing draft and then approving that new draft in the second and final stage of publishing.

- Added welcome route for a landing page after logging in.

- Added a before request function on the vendor blueprint, it handles if a user is 
authenticated but is not a vendor role, they are sent to the invalid request route.

### Changed
- In the users.login route, if the current user is authenticated, we do not send them to the redirect page, they are now sent to the new users.welcome.

---------------------------------------------------------------------------
