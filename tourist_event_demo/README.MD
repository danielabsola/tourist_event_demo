# Data Engineering Code Challenge

As part of our future Data Engineering family, you should start getting to know our product as soon as possible.
Therefore, we'll begin with a quick onboarding session. Please visit [feverup.com](https://feverup.com) and click on the
plan that interests
you the most. That's all for now :)

> [!IMPORTANT]
> The answers for all the exercises below **must be delivered within this repository**, either creating a Pull Request (PR) or directly pushing to the `master` branch.

## Exercise 1 (20%)

As a Data Engineer at Fever, you should be able to create **efficient database models** to be used in our **Business
Intelligence tools** to analyze the data we retrieve.
Based on what can be seen on the [Fever](https://feverup.com/) website, our analysts would like to answer the following
questions, among others:

- **Query 1**: What is the ranking of countries based on the number of plans currently being sold?
- **Query 2**: What are the least expensive categories of plans?
- **Query 3**: On which day of the week are more plans available to purchase in each city?
- **Query 4**: Which venues are the most frequently used to host events?
- **Query 5**: Which plan has the worst reviews and what are the comments about it?

### Requirements

- The deliverable must be a **UML diagram** with the necessary tables to answer the provided questions, and extra
  tables you consider useful to **analyze the performance of a ticketing business**.
- Briefly describe the decisions you took that justify the reason for your data model.
- Queries to solve the asked questions and any extra analysis query you consider relevant is not compulsory, but would
  be positively evaluated.

## Exercise 2 (20%)

In this exercise, we aim to analyze a group of people and their ascendance hierarchy. Imagine you have the tables
generated via the file `exercise_2/exercise2.sql`. A parent can have N children (from 0 to any number). Likewise, their
children can also have N more children each, continuing indefinitely.

#### `HIERARCHY` Structure

- **PARENT_PERSON_ID**: Person who is the parent in the relationship.
- **CHILD_PERSON_ID**: Person who is the child in the relationship.

#### `PEOPLE` Structure

This table contains all existing people, regardless of whether they have children or parents.

- **PERSON_ID**: The unique ID of the person.

#### Desired Output

We want to create a table with the following information:

- **PERSON_ID**: The person being analyzed.
- **PARENT_PERSON_ID**: The direct parent of the person, if they have.
- **ANCESTOR_PERSON_ID**: The ancestor of the person, defined as the highest member of the hierarchy.

#### Example of input / output

`HIERARCHY.SQL`

| PARENT_PERSON_ID | CHILD_PERSON_ID |
|------------------|-----------------|
| 1                | 2               |
| 1                | 3               |
| 3                | 4               |

`PEOPLE.SQL`

| PERSON_ID |
|-----------|
| 1         |
| 2         |
| 3         |
| 4         |
| 5         |

`OUTPUT.SQL`

| PERSON_ID | PARENT_PERSON_ID | ANCESTOR_PERSON_ID |
|-----------|------------------|--------------------|
| 1         | NULL             | 1                  |
| 2         | 1                | 1                  |
| 3         | 1                | 1                  |
| 4         | 3                | 1                  |
| 5         | NULL             | 5                  |

### Requirements

1. Provide an SQL script (compatible with Snowflake or PostgreSQL) to create the table and produce the desired results.
2. Include all people in the output, even those without children.
3. Ensure the output table contains only one row per `PERSON_ID` and shows the direct `PARENT_PERSON_ID`, not all
   existing `PARENT_PERSON_ID`.
4. If the person doesn't have any parent, the ancestor will be themselves.
5. Attach screenshots showing the results of the populated table you have created.

## Exercise 3 (60%)

We need to integrate currency exchange rate data into a centralized data storage.
This data will help analysts produce local currency reports for over 22 countries, with $ as the main reference
currency.

This [API](https://apilayer.com/marketplace/currency_data-api?utm_source=apilayermarketplace&utm_medium=featured) for
exchange rates can be used in its free tier.
The process should handle both initial bulk data loading and daily updates. Use Python to develop the solution and
PostgreSQL for storing the data.
The system should store raw data in an initial storage layer, and optionally, have an intermediate layer for processing
before storing the final data in the main storage. Deployment must be done entirely with Docker, using a docker-compose
file. The entire process must run with Docker commands, and direct execution outside Docker is not allowed.
Think of this as a project others will maintain and evolve. The code must be structured, readable, and extensible.

### Requirements

- Workflow Design:
    - Create two distinct workflows:
        - **Daily Updates**: Automatically runs every 24 hours to load incremental data. The hour should be adjustable
          via an environment variable.
        - **Custom Range Processing**: Allows manual execution for specific date ranges.
- Additional Criteria:
    - Follow Object-Oriented Programming (OOP).
    - Include logging to track both successful and failed records.
- Bonus points
    - Use an orchestration tool (e.g., Airflow). You may consider alternatives if justified.
    - Follow a clean architecture pattern.
    - Add tests.

