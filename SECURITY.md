# Security policy

## Reporting a problem

If you find a leaked secret, personal data, or a security flaw in this repository, please report it **privately**. Do not open a public issue.

1. Go to the **Security** tab of this repository.
2. Click **Report a vulnerability** and describe what you found and where.

Please include the file path and commit, and do not copy the sensitive value into your report. If the Security tab does not offer private reporting, open a public issue that says only "security contact needed" and contains no details.

I will acknowledge a report as soon as I can and remove or rotate anything that should not be public. This is a personal project, so there is no guaranteed response time.

## What counts

- Credentials, tokens or keys of any kind
- Real personal health data, photos or logs
- Code that could expose a user's data or credentials when run

## Supported versions

Only the latest version on the `main` branch is supported.

## If you use Atlas yourself

- Keep your real data and any credentials outside this repository.
- Store credentials in a git-ignored local file, never in code.
- If a credential is ever committed by mistake, revoke it at its source first, then remove it from the history.
