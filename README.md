# MediBook-T

A microservices-based medical appointment booking system.

## Team

| Member | ID | Owns |
| ------ | -- | ---- |
| _TBD_  | _TBD_ | `services/patient`, `database/schema.sql` |
| _TBD_  | _TBD_ | `services/doctor` |
| _TBD_  | _TBD_ | `services/appointment` |
| _TBD_  | _TBD_ | `services/billing` |
| _TBD_  | _TBD_ | `services/notification`, `postman/` |
| _TBD_  | _TBD_ | `webapp/` (JSP/Servlet frontend), `README.md` |

> Replace the rows above with the real team members, their student IDs, and
> clearly assign one owner per area. Every folder should have exactly one owner.

## Architecture

```
          +-----------------+
          |  webapp (JSP)   |
          +--------+--------+
                   | REST (JSON)
   +---------------+----------------+
   |               |                |
patient         doctor         appointment
service         service         service
   |               |                |
   +---------+-----+--------+-------+
             |              |
          billing      notification
```

All services share a single MySQL database (`clinic_system`) defined in `database/`.

## How to run

### 1. Database

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p clinic_system < database/sample_data.sql
```

### 2. Microservices (Flask)

Each service is an independent Flask app. Repeat for every folder in `services/`:

```bash
cd services/patient
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py          # default http://localhost:5001
```

Default ports:

| Service       | Port |
| ------------- | ---- |
| patient       | 5001 |
| doctor        | 5002 |
| appointment   | 5003 |
| billing       | 5004 |
| notification  | 5005 |

Connection settings live in each service's `config.py` (overridable via
environment variables).

### 3. Webapp (JSP/Servlet)

```bash
cd webapp
mvn clean package
# deploy target/medibook-web.war to Tomcat 9+
```

## API / Postman

Import `postman/medibook-T.postman_collection.json` into Postman to exercise
every service endpoint.
