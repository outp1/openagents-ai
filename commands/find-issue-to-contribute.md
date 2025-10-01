
**Task:** Identify a suitable issue to resolve and contribute to the target GitHub repository.

**User Input:**
```
$ARGUMENTS
```

**Instructions for the Agent:**

1. Arguments extraction: Determine the target repository from the user input and other request requirements.
2. Issue Selection Criteria:
    - Open issues only.
    - At least **2+ comments** (ensures some discussion/activity).
    - No active Pull Request already awaiting review.
3. Contribution Guide Check: Ensure that fixing this issue will not conflict with the repository’s contribution guidelines (e.g., changes to core modules without prior maintainer discussion).
4. Complexity Assessment: Perform minimal research by reviewing repository code and related documentation to estimate implementation difficulty.
    
**Output Format.** Provide a **table** with the following columns:
- Issue (Title + Link)
- Complexity (Low / Medium / High)
- Suggested Fix / Next Step (if applicable)

Use the **GitHub MCP tool** to fetch repository issues and metadata.
