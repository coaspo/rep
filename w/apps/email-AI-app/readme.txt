Set up
1. Open Google Cloud Console
- URL: Google Cloud Console
- Sign in: Google account
- Project: molten-hall-284813 (existing project)
2. Enable Gmail API
- URL: Gmail API
- API: Gmail API
- Action: Enable, if not already enabled
3. Locate OAuth credentials
- URL: APIs & Services → Credentials
- Section: OAuth 2.0 Client IDs
- Existing client: Web client 1
- Action: Reuse existing client
4. Create a new client secret
- Menu: Web client 1
- Action: Add Secret
- Result: New client secret
- Action: Download JSON credentials
- Note: Two secrets now exist; neither deleted
5. Configure OAuth audience
- URL: Google Auth Platform → Audience
- User type: External
- Publishing status: Testing
6. Add test user
- Section: Test users
- Action: + Add users
- Email: cphantzis@gmail.com
- Action: Save
- Result: Saved (listed below filters)
7. Configure OAuth redirect URI
- URL: Google Auth Platform → Clients
- Client: Web client 1
- Section: Authorized redirect URIs
- Added:
  http://localhost:5000/oauth2callback
- Action: Save
