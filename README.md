# HCL_banking_backend
This project is a HCL hackathon problem statement 

# HCL Hackathon
The objective is to build the Modular Banking Backend System 

## Who are my actors
* Customer
    * User Registration
    * account creation 
    * money Transfer
    * loan application and emi calculation
* Bank Admin
(works on support with customer need to implement simple customer)
    * loan applicaton
        * submit loan type, amount , tenure
        * system calculates the emi.

            ```EMI = (P*r*(1+r)^n)/((1+r)^n-1)```
    * Frade detection
        * a ML/AI model to check for anomalies
        * flag suspicious transactions
        * notify admin 
* Auditor 
 (works on support with customer need to implement simple customer)
    * Reports and Dashboard

> I should be focusing on the simple implementation of customer with simple ui with bank admin where the customer will apply for the loan and admin will approve or reject the loan and  the same is update to the customer


## Tech stack planning to use 
* FastAPI (Python web framework for building APIs)
* PostgreSQL (relational database)
* SQLAlchemy (ORM for database interaction)
* JWT/OAuth2 (authentication, supported by FastAPI)
* Swagger UI (auto-generated API documentation and testing interface from FastAPI)
* pytest (for unit testing)
* bcrypt or passlib (for secure password hashing)

### My plan/ My Focus
*   User Registration & Login:
    *   Customer registration with age validation
    *   Secure password hashing
    *   JWT-based authentication
*   Loan Application Workflow:
    *   Customer submits loan application (type, amount, tenure)
    *   Admin can view, approve, or reject applications
    *   Status updates reflected in the database
*   EMI Calculation:
    *   EMI auto-calculated on approval using the formula in your README
    *   Store EMI in the loan record
*   Database Models:
    *   Customers, Admins, Loans
*   API Endpoints:
    *   Endpoints for registration, login, loan application, admin actions
*   Basic Unit Tests:
    *   For core logic (registration, login, loan application, EMI calculation)
*   Documentation:
    *   FastAPI auto-generates OpenAPI docs (Swagger UI) for all endpoints
*   Fraud Detection (Optional): 
    *   You can add a placeholder endpoint or logic for fraud detection if time permits


### Points to be kept in mind 
> Documenting with the unit test and code coverage is expeted to be 100% and that also has to be written.

> code quality matters so has to have a good code quality.

> I have free to choose which test case/ use case are feasiable to me and use only those

> keep the code modular and clean

Authentication APIs
* POST /auth/token - Login for both customers and admins (returns JWT token)
Customer APIs
* POST /customers/register - Register a new customer
* GET /customers/me - Get current customer's profile (requires authentication)
* POST /customers/loans - Apply for a loan (requires authentication)
* GET /customers/loans - Get customer's loan history (requires authentication)
Admin APIs
* GET /admins/loans - View all pending loans (requires admin authentication)
* PUT /admins/loans/{loan_id} - Approve or reject a loan (requires admin authentication)
General APIs
* GET / - Root endpoint (welcome message)

### Customer Model
Table: customers

* Fields:
    * id (SERIAL, Primary Key)
    * name (VARCHAR(100), Not Null)
    * email (VARCHAR(100), Unique, Not Null)
    * password_hash (VARCHAR(255), Not Null)
    * age (INT, Not Null)
    * phone (VARCHAR(20), Optional)
    * address (VARCHAR(255), Optional)
    * created_at (TIMESTAMP, Default: now())

BankAdmin Model
Table: bank_admins
* Fields:
    * id (SERIAL, Primary Key)
    * username (VARCHAR(100), Unique, Not Null)
    * email (VARCHAR(100), Unique, Not Null)
    * password_hash (VARCHAR(255), Not Null)
    * created_at (TIMESTAMP, Default: now())
Loan Model
Table: loans
* Fields:
    * id (SERIAL, Primary Key)
    * customer_id (INT, Foreign Key to customers.id, Not Null)
    * loan_type (VARCHAR(50), Not Null)
    * amount (NUMERIC(12,2), Not Null)
    * tenure_months (INT, Not Null)
    * interest_rate (NUMERIC(5,2), Not Null)
    * emi (NUMERIC(12,2), Optional - calculated on approval)
    * status (VARCHAR(20), Not Null, Default: 'pending')
    * applied_at (TIMESTAMP, Default: now())
    * updated_at (TIMESTAMP, Optional)
### Relationships
One-to-Many: Customer → Loans (a customer can have multiple loans).

No direct relationship between BankAdmin and Loans (admins manage all loans via queries)


# Startup to start the server
 >  uvicorn app.main:app --reload