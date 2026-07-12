# 🚛 TransitOps

> **Smart Transport Operations Platform**\
> A modern, enterprise-grade Fleet & Transport Management System that
> digitizes vehicle operations, driver management, trip dispatching,
> maintenance scheduling, fuel tracking, expense management, and
> business analytics.

------------------------------------------------------------------------

## 📖 Table of Contents

-   Overview
-   Problem Statement
-   Key Features
-   Tech Stack
-   System Architecture
-   Project Workflow
-   User Roles
-   Module Overview
-   Business Rules
-   Database Design
-   Folder Structure
-   Installation
-   Running the Project
-   Backend Integration
-   Future Roadmap
-   Screenshots
-   Contributors
-   License

------------------------------------------------------------------------

# Overview

TransitOps is a centralized transport operations platform designed to
replace manual spreadsheets and logbooks used by logistics companies.
The platform streamlines fleet management by providing a single
interface to manage vehicles, drivers, dispatching, maintenance, fuel
logs, operational expenses, and business analytics.

## Objectives

-   Centralize fleet operations
-   Improve operational visibility
-   Prevent scheduling conflicts
-   Enforce business rules
-   Track maintenance
-   Reduce operational costs
-   Generate business insights

------------------------------------------------------------------------

# Problem Statement

Many logistics organizations still rely on spreadsheets to manage
transport operations.

This results in:

-   Vehicle scheduling conflicts
-   Underutilized fleet
-   Missed maintenance
-   Expired driver licenses
-   Manual fuel tracking
-   Incorrect expense calculations
-   Poor business visibility

**TransitOps** solves these issues through a centralized ERP-style
platform.

------------------------------------------------------------------------

# Key Features

-   Secure Authentication
-   Role Based Access Control (RBAC)
-   Fleet Dashboard
-   Vehicle Registry
-   Driver Management
-   Trip Dispatching
-   Maintenance Workflow
-   Fuel Logging
-   Expense Tracking
-   Analytics Dashboard
-   CSV Export
-   Responsive UI
-   Django Ready Architecture

------------------------------------------------------------------------

# Tech Stack

## Frontend

-   HTML5
-   CSS3
-   Bootstrap 5
-   Vanilla JavaScript
-   Chart.js

## Backend (Planned)

-   Django
-   Python
-   MySQL
-   Django Authentication
-   RBAC

------------------------------------------------------------------------

# System Architecture

``` text
Browser
   │
   ▼
Frontend (HTML + Bootstrap + JS)
   │
   ▼
Django Views
   │
   ▼
Business Logic
   │
   ▼
Django Models
   │
   ▼
MySQL Database
```

------------------------------------------------------------------------

# Complete Workflow

``` text
Login
   │
Authentication
   │
Role Based Access
   │
Dashboard
   │
 ┌───────────────┬────────────────┐
 │               │                │
 ▼               ▼                ▼
Vehicles      Drivers       Reports
 │               │
 └───────┬───────┘
         ▼
   Create Trip
         │
Business Validations
         │
 ┌──────────────────────────────┐
 │ Vehicle Available            │
 │ Driver Available             │
 │ License Valid                │
 │ Capacity Validation          │
 └──────────────────────────────┘
         │
 Dispatch Trip
         │
Vehicle → On Trip
Driver  → On Trip
         │
 Complete Trip
         │
 Fuel Logs
         │
 Expenses
         │
 Maintenance
         │
 Analytics
```

------------------------------------------------------------------------

# User Roles

  Role                Responsibilities
  ------------------- ---------------------------------------
  Fleet Manager       Fleet assets, vehicles, maintenance
  Driver              Trip execution, fuel logs
  Safety Officer      Driver compliance, license monitoring
  Financial Analyst   Expenses, ROI, reports

------------------------------------------------------------------------

# Module Overview

## Authentication

-   Secure Login
-   RBAC
-   Protected Routes

## Dashboard

-   KPI Cards
-   Charts
-   Recent Activities
-   Fleet Overview

## Vehicle Management

-   Register Vehicle
-   Edit Vehicle
-   Vehicle Status
-   Vehicle Details

## Driver Management

-   Driver Profiles
-   License Tracking
-   Safety Score
-   Availability

## Trip Management

-   Create Trip
-   Dispatch
-   Complete Trip
-   Cancel Trip

## Maintenance

-   Maintenance Logs
-   Service History
-   Vehicle Availability

## Fuel & Expenses

-   Fuel Logs
-   Maintenance Cost
-   Toll Expenses
-   Operational Cost

## Reports

-   Fleet Utilization
-   Fuel Efficiency
-   Vehicle ROI
-   Expense Analytics

------------------------------------------------------------------------

# Trip Lifecycle

``` text
Draft
  │
  ▼
Dispatched
  │
  ├─────────────► Cancelled
  │
  ▼
Completed
```

------------------------------------------------------------------------

# Vehicle Status Flow

``` text
Available
   │
   ▼
On Trip
   │
   ▼
Available
   │
   ▼
In Shop
   │
   ▼
Available
   │
   ▼
Retired
```

------------------------------------------------------------------------

# Database Design

``` text
Users
 ├── Roles
 ├── Drivers
 ├── Vehicles
 │     ├── Trips
 │     ├── Maintenance
 │     ├── Fuel Logs
 │     └── Expenses
 └── Reports
```

### Core Entities

-   Users
-   Roles
-   Vehicles
-   Drivers
-   Trips
-   Maintenance Logs
-   Fuel Logs
-   Expenses

------------------------------------------------------------------------

# Business Rules

  Rule                 Description
  -------------------- -----------------------------------------------
  Unique Vehicle       Registration number must be unique
  Vehicle Validation   Retired/In Shop vehicles cannot be dispatched
  Driver Validation    Expired/Suspended drivers cannot be assigned
  Capacity Check       Cargo must not exceed vehicle capacity
  Auto Status          Dispatch changes vehicle & driver to On Trip
  Completion           Completing trip restores availability
  Maintenance          Active maintenance marks vehicle In Shop

------------------------------------------------------------------------

# Folder Structure

``` text
TransitOps/
│
├── assets/
│   ├── css/
│   ├── js/
│   ├── img/
│   ├── icons/
│   └── vectors/
│
├── pages/
│   ├── login.html
│   ├── dashboard.html
│   ├── vehicles.html
│   ├── vehicle-details.html
│   ├── add-vehicle.html
│   ├── drivers.html
│   ├── driver-details.html
│   ├── add-driver.html
│   ├── trips.html
│   ├── create-trip.html
│   ├── trip-details.html
│   ├── maintenance.html
│   ├── fuel.html
│   ├── expenses.html
│   ├── reports.html
│   ├── settings.html
│   └── profile.html
│
└── README.md
```

------------------------------------------------------------------------

# Installation

``` bash
git clone https://github.com/yourusername/TransitOps.git

cd TransitOps
```

------------------------------------------------------------------------

# Running the Frontend

Simply open:

``` text
pages/login.html
```

or use VS Code Live Server.

------------------------------------------------------------------------

# Backend Integration (Future)

``` bash
pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

------------------------------------------------------------------------

# Future Roadmap

-   [x] Responsive UI
-   [x] Dashboard
-   [x] Vehicle Management
-   [x] Driver Management
-   [x] Trip Management
-   [x] Maintenance
-   [x] Fuel Logs
-   [x] Expense Tracking
-   [ ] PDF Reports
-   [ ] GPS Tracking
-   [ ] Predictive Maintenance
-   [ ] AI Route Optimization
-   [ ] Mobile Application
-   [ ] Notifications

------------------------------------------------------------------------

# Screenshots

``` text
screenshots/
├── login.png
├── dashboard.png
├── vehicles.png
├── drivers.png
├── trips.png
├── maintenance.png
└── reports.png
```

------------------------------------------------------------------------

# Contributors

  Name        Role
  ----------- -------------
  Jeet Soni  Team Lead
  
  Dhwanit Mistry Member
  
  Ridham Kothari Member

------------------------------------------------------------------------

# Acknowledgements

Developed for a Transport Operations Hackathon to demonstrate scalable
ERP architecture, clean UI, modular frontend development, and seamless
backend integration.

------------------------------------------------------------------------

