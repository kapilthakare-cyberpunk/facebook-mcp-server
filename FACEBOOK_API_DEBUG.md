# Facebook API Permission Troubleshooting Guide

We are encountering a persistent error when trying to post to Facebook:
`(#283) Requires pages_read_engagement permission to manage the object`

This error is confusing because you *did* add this permission. However, Facebook's API is strict, and several subtle issues could be causing this.

## Step 1: Debug Your Current Token (Crucial)

We need to see exactly what Facebook thinks your token can do.

1.  Go to the **[Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)**.
2.  Paste your **Page Access Token** (the one currently in your `.env` file).
3.  Click **Debug**.

**Check the following fields in the report:**

*   **Type:** It MUST say `Page`. (If it says `User`, that's the problem).
*   **Page ID:** It MUST match `119372561536771` (Primes & Zooms).
*   **Scopes:** This list **MUST** include:
    *   `pages_read_engagement`
    *   `pages_manage_posts`
    *   `pages_manage_engagement`
    *   `pages_show_list`
    *   `public_profile`
*   **Expires:** It should say "Never" or a far-future date.
*   **Data Access Expires:** Ensure this hasn't passed.

**Action:**
*   If **Type** is `User`, you skipped the step of selecting your Page in the dropdown.
*   If a **Scope** is missing, you need to add it back in the Explorer and regenerate.

## Step 2: Check App "Live" Mode

*   Go to your [App Dashboard](https://developers.facebook.com/apps/).
*   Look at the top bar. Is the toggle **In Development** or **Live**?
*   **For "In Development" mode:** You (the Admin) can access your own Page, BUT you must be listed as an Administrator in the "Roles" section of the App.
*   **For "Live" mode:** You generally need "Business Verification" or "App Review" for advanced permissions like `pages_read_engagement` to work for *other* users. Since you are the admin, **keep it in Development mode** for now unless you are verified.

## Step 3: Check Page Settings

Sometimes a Page's specific settings block API access.

1.  Go to your Facebook Page Settings.
2.  Look for "Partner Apps" or "Business Integrations".
3.  Ensure your App is listed there and has valid permissions.
4.  **Two-Factor Authentication:** If your Business Manager requires 2FA, and your account doesn't have it, API calls might fail.

## Step 4: The "Chicken and Egg" Problem with Page IDs

We saw an error earlier: `Object with ID '...' does not exist`.
*   We fixed the ID to `119372561536771`.
*   However, if the *Token* was generated for the *User* but not explicitly "Swapped" for the Page, it might not have the right authority *over* that Page ID, even if it has the permissions.

**How to fix (The "Foolproof" Method):**

1.  Go back to **[Graph API Explorer](https://developers.facebook.com/tools/explorer/)**.
2.  Ensure all permissions are in the list on the right.
3.  Click **Generate Access Token** (User Token).
4.  **IMMEDIATELY** look at the "User or Page" dropdown (under the Access Token field).
5.  Click it and select **Primes & Zooms**.
6.  The token string will change. **THIS is the token you need.**
7.  Copy this new token.

## Summary of Next Steps for You

1.  **Run the Debug Tool** (Step 1) and tell me if it says "User" or "Page".
2.  **Regenerate the Token** using the "Foolproof Method" (Step 4) just to be absolutely sure.
3.  **Paste the new token** in the chat (or update `.env` and tell me).

Once we have a confirmed **PAGE** token with `pages_read_engagement`, the error `(#283)` requires...` will disappear.
