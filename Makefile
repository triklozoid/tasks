pgpass = 'GA44byBWf8Rgaf30ckiSKMlVNA7YXI9KQAlB+Xe0j14='
first_task:
	echo 'first_task';
	docker run --rm --name testtask-postgres -e POSTGRES_PASSWORD=$(pgpass) -d postgres:9.6.3
	sleep 4
	docker run --rm --link testtask-postgres:postgres -v $(shell pwd):/app -e PGPASSWORD=$(pgpass) postgres psql -h postgres -U postgres -a -f /app/employee.sql
	docker run --rm --link testtask-postgres:postgres -e PGPASSWORD=$(pgpass) postgres psql -h postgres -U postgres -c 'SELECT m.name, m.department, t.mx FROM (SELECT department, max(salary) as mx from employee GROUP BY department) t JOIN employee m on m.department = t.department and t.mx = m.salary;'
	docker run --rm --link testtask-postgres:postgres -e PGPASSWORD=$(pgpass) postgres psql -h postgres -U postgres -c 'SELECT DISTINCT ON (department) department, name, salary from employee ORDER BY department, salary DESC;'
	docker stop testtask-postgres
