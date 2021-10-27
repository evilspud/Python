Background:
    Code was written using Python 3.9.6 64 bit.

Assumptions:
    I've avoided using packages other than those built in to Python.
    It's assumed that the user may not be have the ability to import the same
        packages for the purpose of this exercise.
    I've avoided calculating variables etc in SQL, as I assumed this was not
        the point of the challenge.

Data Quality observations:
    Y/N flags are not all Y and N.
        Work arounds have been put in place. Please see function for details.
        In reality, it would be best to return an error. However, for the
        purposes of this exercise, I don't know what these values would be
        corrected to.
    Some regular payment amounts are missing or zero.
        This is handled in the function.
    Some customer account positions have two or more customers
        This has been noted but accepted and exported as there are no priority
        criteria on the brief

Set-up:
    Run the database set-up as supplied with the task.
    The user will need to specify the database location in set_parameters.py.

Run:
    bin/run_interview_task.sh

Approach:
    Set_parameters.py:
        Make parameters universal
    functions.py:
        Separate functions into module. If a calculation is repeated or
        complicated, it will be found here.
    database_build_report.py:
        Report developed to give a feel of the tables built, and to observe
        the success of the build process. This was written assuming that CSV
        inputs may not be visible to the user in future.
    data_quality.py:
        A list of SQL queries which better highlight some of the issues.
    create_summary_csv_report.py: (TASK 1)
        This task can be achieved mostly with the SQL query. Connect to
        database, run query and export to CSV.
    create_mortgages_data_json.py: (TASK 2)
        If we attempt to join all the necessary data in SQL, we will end up
        with a table which has duplicate accounts. I did not know a way of then
        exporting a distinct list, so therefore we have the longer approach.

        Account-distinct data and customer-distinct data have been returned
        separately and joined by matching dictionary keys.

        Data has been fed from a list of tuples (SQL) into separate variables
        in order to calculate derived fields.

Style:
    I've deliberately over-commented the code and headers in order to give
        information. 
    
    Variable names are deliberately not the same as their corresponding
        functions.

    In some places I've done the same thing in different ways to highlight that
        it can be done in each way. Normally, consistency would be better.
    i.e. the use of tuple -> variable by 'position', and tuple -> variable by
        index

Critique:
    Due to the list comprehension approach in create_mortgages_data_json.py,
        performance would suffer if the database tables were very large.

Further Development:
    I'm sure there's a way of more simply creating a nested json file from
        database output that does not have a unique primary key.
    If this was the case, I would do all the joining in SQLITE and avoid the
        need to have list comperehensions to join accounts and customers.
    
    It would be useful to add logging, more error handling and pytest testing.

    Parameters could be added to the command line when running.