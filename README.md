# Hospital Management System (HMS)

A robust, full-stack platform engineered for high-integrity data environments. Built with Django and PostgreSQL, it features secure Stripe payment processing, mirroring the reliability and security required in financial systems.

![Main](screenshots/System_Features.png)

---

##   Features

1. **Role-Based Access Control (RBAC)**: Ensures strict hierarchical data access (Admin, Manager, User).
2. **Secure Transaction Processing**: Integrated, PCI-compliant payment gateway for fee and service billing.
3. **Audit-Ready Records Management**: Maintains immutable logs of all transactions and user activities.
4. **Comprehensive Dashboard Analytics**: Provides real-time insights into system operations and financial summaries.
5. **Advanced User Authentication & Session Management**: Implements industry-standard security protocols.

---

##  Tech Stack

1. **Backend Framework**: Django (Python)
2. **Database**: PostgreSQL (Emphasizing ACID compliance and data integrity)
3. **Payment Gateway**: Stripe API
4. **Frontend**: Bootstrap + Django Templates (Responsive UI)
5. **Security**: CSRF protection, ORM-based SQL injection prevention, secure authentication.
6. **Deployment**: Container-ready for secure, scalable deployment (Docker).

---

##   Screenshots

|  Admin Dashboard  |  Doctor Dashboard  |  Patient Dashboard  |
|-------------------|--------------------|---------------------|
| ![Patient](screenshots/Admin_Dash.png) | ![Doctor](screenshots/Doctor_Profile.png) | ![Admin](screenshots/Patient_Profile.png) |

|  Appointment Booking  |  Patient Info  |  Login Page  |
|-----------------------|----------------|--------------|
| ![Patient](screenshots/Appointment_Booking.png) | ![Doctor](screenshots/Patient_Info.png) | ![Admin](screenshots/Login_Page.png) |

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
This project is licensed under the [MIT License](./LICENSE).