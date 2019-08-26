# CFauditer.py
Pulls down Cloudflare audit logs via API and outputs to a file or tcp in json format. The json logs are preformatted and easily parsable by Logstash.

## Configuration
1. Put script into /opt/CFauditer folder.
2. Edit the script and update variables **CF_TOKEN**, **CF_EMAIL**, **CF_ORG**, **HOST**, **PORT** with your values.
3. Copy init script to /etc/init.d/ directory.
4. Execute the script (it will run in a constant loop).

## Example dashboard (pending)
